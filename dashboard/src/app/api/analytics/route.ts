import { NextResponse } from 'next/server';
import {
  getAllExecutions,
  getAllTestCases,
  getBrowserAnalytics,
  getEnvironmentAnalytics,
  getFailureAnalysis,
} from '@/lib/result-parser';

export async function GET() {
  try {
    const executions = getAllExecutions();
    const testCases = getAllTestCases();
    const browserMetrics = getBrowserAnalytics();
    const envMetrics = getEnvironmentAnalytics();
    const failures = getFailureAnalysis();

    // Pass rate trend (chronological order)
    const reversed = [...executions].reverse();
    const trendLabels = reversed.map((e) => e.execution_id.replace('EXEC-', '#'));
    const passRates = reversed.map((e) => e.pass_rate);
    const durations = reversed.map((e) => e.duration);
    const failureCounts = reversed.map((e) => e.failed);

    // Module distribution
    const moduleCounts: Record<string, number> = {};
    for (const t of testCases) {
      moduleCounts[t.module] = (moduleCounts[t.module] || 0) + 1;
    }
    const moduleDistribution = Object.entries(moduleCounts).map(([module, count]) => ({
      module,
      count,
    }));

    // Test type distribution
    const typeCounts: Record<string, number> = {};
    for (const t of testCases) {
      typeCounts[t.test_type] = (typeCounts[t.test_type] || 0) + 1;
    }
    const typeDistribution = Object.entries(typeCounts).map(([type, count]) => ({
      type,
      count,
    }));

    // Browser distribution
    const browserDistribution = browserMetrics.map((b) => ({
      browser: b.browser,
      count: b.total_tests,
    }));

    return NextResponse.json({
      trends: {
        labels: trendLabels,
        pass_rates: passRates,
        durations: durations,
        failures: failureCounts,
      },
      distributions: {
        modules: moduleDistribution,
        types: typeDistribution,
        browsers: browserDistribution,
      },
      browsers: browserMetrics,
      environments: envMetrics,
      total_executions: executions.length,
      total_test_cases: testCases.length,
      total_failures_recorded: failures.reduce((acc, f) => acc + f.failure_count, 0),
    });
  } catch (err: any) {
    return NextResponse.json(
      { error: 'Failed to compile analytics', details: err?.message },
      { status: 500 }
    );
  }
}
