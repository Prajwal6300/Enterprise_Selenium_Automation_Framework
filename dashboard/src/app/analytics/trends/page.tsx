import React from 'react';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import {
  PassRateTrendLine,
  DurationTrendBar,
  FailureTrendLine,
  ModuleDistributionBar,
  BrowserDistributionPie,
} from '@/components/charts/DashboardCharts';
import {
  getAllExecutions,
  getAllTestCases,
  getBrowserAnalytics,
} from '@/lib/result-parser';
import { TrendingUp, Clock, AlertTriangle, Layers, Globe2 } from 'lucide-react';

export const dynamic = 'force-dynamic';
export const revalidate = 0;

export default async function TestTrendsPage() {
  const executions = getAllExecutions();
  const testCases = getAllTestCases();
  const browserMetrics = getBrowserAnalytics();

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

  const browserDistribution = browserMetrics.map((b) => ({
    browser: b.browser,
    count: b.total_tests,
  }));

  return (
    <DashboardLayout>
      <div className="page-header">
        <div className="page-title-group">
          <h1>Test Execution Trends & Performance</h1>
          <p>
            Historical pass rates, run durations, failure patterns, and functional module distributions.
          </p>
        </div>
      </div>

      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(450px, 1fr))',
          gap: '24px',
        }}
      >
        {/* Pass Rate Trend */}
        <div className="card">
          <div className="card-header">
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <TrendingUp size={16} color="#2563eb" />
              <div className="card-title">Pass Rate Trend Across Builds</div>
            </div>
            <span style={{ fontSize: '12px', color: '#64748b' }}>Target &ge; 95%</span>
          </div>
          <PassRateTrendLine labels={trendLabels} rates={passRates} />
        </div>

        {/* Execution Duration Trend */}
        <div className="card">
          <div className="card-header">
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Clock size={16} color="#3b82f6" />
              <div className="card-title">Execution Duration (Speed Regression)</div>
            </div>
            <span style={{ fontSize: '12px', color: '#64748b' }}>Duration in seconds</span>
          </div>
          <DurationTrendBar labels={trendLabels} durations={durations} />
        </div>

        {/* Failure Trend */}
        <div className="card">
          <div className="card-header">
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <AlertTriangle size={16} color="#ef4444" />
              <div className="card-title">Failure Trend Across Builds</div>
            </div>
            <span style={{ fontSize: '12px', color: '#ef4444', fontWeight: '600' }}>Regression Tracker</span>
          </div>
          <FailureTrendLine labels={trendLabels} failures={failureCounts} />
        </div>

        {/* Functional Module Distribution */}
        <div className="card">
          <div className="card-header">
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Layers size={16} color="#10b981" />
              <div className="card-title">Test Distribution by Module</div>
            </div>
            <span style={{ fontSize: '12px', color: '#64748b' }}>{testCases.length} Tests</span>
          </div>
          <ModuleDistributionBar modules={moduleDistribution} />
        </div>

        {/* Browser Breakdown */}
        <div className="card">
          <div className="card-header">
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Globe2 size={16} color="#f59e0b" />
              <div className="card-title">Browser Distribution</div>
            </div>
            <span style={{ fontSize: '12px', color: '#64748b' }}>Cross-browser coverage</span>
          </div>
          <BrowserDistributionPie browsers={browserDistribution} />
        </div>
      </div>
    </DashboardLayout>
  );
}
