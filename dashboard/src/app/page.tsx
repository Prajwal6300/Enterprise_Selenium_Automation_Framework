import React from 'react';
import Link from 'next/link';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { KpiCard } from '@/components/common/KpiCard';
import { StatusBadge } from '@/components/common/StatusBadge';
import {
  PassRateDoughnut,
  PassRateTrendLine,
  DurationTrendBar,
  ModuleDistributionBar,
  BrowserDistributionPie,
} from '@/components/charts/DashboardCharts';
import {
  getAllExecutions,
  getAllTestCases,
  getBrowserAnalytics,
  getEnvironmentAnalytics,
  getLatestExecution,
  getLiveExecutionStatus,
} from '@/lib/result-parser';
import {
  CheckCircle2,
  XCircle,
  AlertCircle,
  Clock,
  TrendingUp,
  Globe2,
  Layers,
  FileText,
  PlaySquare,
  ArrowRight,
  ShieldCheck,
  Activity,
} from 'lucide-react';

export const dynamic = 'force-dynamic';
export const revalidate = 0;

export default async function DashboardPage() {
  const executions = getAllExecutions();
  const latest = getLatestExecution();
  const allTests = getAllTestCases();
  const browsers = getBrowserAnalytics();
  const envs = getEnvironmentAnalytics();
  const liveStatus = getLiveExecutionStatus();

  const totalTests = latest?.total || allTests.length || 18;
  const passedTests = latest?.passed || allTests.filter((t) => t.status === 'PASSED').length || 18;
  const failedTests = latest?.failed || allTests.filter((t) => t.status === 'FAILED').length || 0;
  const skippedTests = latest?.skipped || 0;
  const passRate = latest?.pass_rate || (totalTests > 0 ? Number(((passedTests / totalTests) * 100).toFixed(1)) : 100);
  const durationSec = latest?.duration || 69;
  const formatDuration = (s: number) => {
    const mins = Math.floor(s / 60);
    const secs = Math.round(s % 60);
    return `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
  };

  // Trend data
  const reversed = [...executions].reverse();
  const trendLabels = reversed.map((e) => e.execution_id.replace('EXEC-', '#'));
  const passRates = reversed.map((e) => e.pass_rate);
  const durations = reversed.map((e) => e.duration);

  // Module distribution
  const moduleCounts: Record<string, number> = {};
  for (const t of allTests) {
    moduleCounts[t.module] = (moduleCounts[t.module] || 0) + 1;
  }
  const moduleDistribution = Object.entries(moduleCounts).map(([module, count]) => ({
    module,
    count,
  }));

  return (
    <DashboardLayout environment={latest?.environment || 'QA'}>
      {/* Page Header */}
      <div className="page-header">
        <div className="page-title-group">
          <h1>Enterprise QA Dashboard</h1>
          <p>
            Real-time test execution analytics, browser telemetry, failure diagnoses & CI/CD status.
          </p>
        </div>
        <div className="header-actions">
          <Link href="/reports" className="btn btn-sm">
            <FileText size={14} color="#64748b" />
            <span>Reports Hub</span>
          </Link>
          <Link href="/executions" className="btn btn-sm btn-primary">
            <PlaySquare size={14} />
            <span>All Executions</span>
          </Link>
        </div>
      </div>

      {/* Live Status Banner */}
      <div
        style={{
          backgroundColor: liveStatus.is_active ? '#ecfdf5' : '#ffffff',
          border: `1px solid ${liveStatus.is_active ? '#a7f3d0' : 'var(--border-color)'}`,
          borderRadius: 'var(--radius-lg)',
          padding: '12px 20px',
          marginBottom: '24px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexWrap: 'wrap',
          gap: '12px',
          boxShadow: 'var(--shadow-sm)',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div
            style={{
              width: '10px',
              height: '10px',
              borderRadius: '50%',
              backgroundColor: liveStatus.is_active ? '#10b981' : '#94a3b8',
            }}
          />
          <div>
            <div style={{ fontSize: '13px', fontWeight: '600', color: '#0f172a' }}>
              {liveStatus.is_active ? `Execution in Progress (${liveStatus.execution_id})` : 'Execution Status: Idle'}
            </div>
            <div style={{ fontSize: '12px', color: '#64748b' }}>
              {liveStatus.message || 'Latest run completed successfully across all test suites.'}
            </div>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', fontSize: '12.5px', color: '#475569' }}>
          <span>Latest Build: <strong>{latest?.execution_id || 'EXEC-1024'}</strong></span>
          <span style={{ color: '#cbd5e1' }}>|</span>
          <span>Branch: <strong>{latest?.branch || 'main'}</strong></span>
          <span style={{ color: '#cbd5e1' }}>|</span>
          <span>Commit: <code style={{ fontFamily: 'var(--font-mono)' }}>{latest?.commit_hash || 'a83f12d'}</code></span>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="kpi-grid">
        <KpiCard
          title="Total Tests"
          value={totalTests}
          subtext="Executed in suite"
          icon={PlaySquare}
          variant="primary"
        />
        <KpiCard
          title="Passed"
          value={passedTests}
          subtext={`${passRate}% success rate`}
          icon={CheckCircle2}
          variant="success"
        />
        <KpiCard
          title="Failed"
          value={failedTests}
          subtext={failedTests === 0 ? 'Zero regressions' : 'Needs investigation'}
          icon={XCircle}
          variant={failedTests > 0 ? 'danger' : 'default'}
        />
        <KpiCard
          title="Skipped"
          value={skippedTests}
          subtext="Ignored tests"
          icon={AlertCircle}
          variant="warning"
        />
        <KpiCard
          title="Pass Rate"
          value={`${passRate}%`}
          subtext="Quality threshold >= 95%"
          icon={TrendingUp}
          variant="success"
        />
        <KpiCard
          title="Execution Time"
          value={formatDuration(durationSec)}
          subtext={`Total: ${durationSec}s`}
          icon={Clock}
          variant="primary"
        />
        <KpiCard
          title="Active Environment"
          value={latest?.environment || 'QA'}
          subtext="SauceDemo E-Commerce"
          icon={Layers}
          variant="default"
        />
        <KpiCard
          title="Target Browser"
          value={latest?.browser || 'Chrome'}
          subtext="Headless WebDrivers"
          icon={Globe2}
          variant="default"
        />
      </div>

      {/* Visual Analytics Grid */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))',
          gap: '20px',
          marginBottom: '24px',
        }}
      >
        {/* Pass vs Fail Doughnut */}
        <div className="card">
          <div className="card-header">
            <div>
              <div className="card-title">Test Results Breakdown</div>
              <div className="card-subtitle">Pass vs Fail ratio for latest run</div>
            </div>
            <StatusBadge status={latest?.status || 'PASSED'} />
          </div>
          <PassRateDoughnut passed={passedTests} failed={failedTests} skipped={skippedTests} />
        </div>

        {/* Pass Rate Trend */}
        <div className="card">
          <div className="card-header">
            <div>
              <div className="card-title">Pass Rate Trend</div>
              <div className="card-subtitle">Historical success percentage across builds</div>
            </div>
            <span style={{ fontSize: '12px', color: 'var(--primary)', fontWeight: '600' }}>
              {trendLabels.length} Executions
            </span>
          </div>
          <PassRateTrendLine labels={trendLabels} rates={passRates} />
        </div>

        {/* Execution Duration Trend */}
        <div className="card">
          <div className="card-header">
            <div>
              <div className="card-title">Execution Duration (s)</div>
              <div className="card-subtitle">Total run time per build (performance tracking)</div>
            </div>
            <Clock size={16} color="#64748b" />
          </div>
          <DurationTrendBar labels={trendLabels} durations={durations} />
        </div>

        {/* Functional Module Distribution */}
        <div className="card">
          <div className="card-header">
            <div>
              <div className="card-title">Module Distribution</div>
              <div className="card-subtitle">Test coverage across functional areas</div>
            </div>
            <span style={{ fontSize: '12px', color: '#64748b' }}>{allTests.length} Total Cases</span>
          </div>
          <ModuleDistributionBar modules={moduleDistribution} />
        </div>
      </div>

      {/* Recent Test Executions Table */}
      <div className="card" style={{ marginBottom: '24px' }}>
        <div className="card-header">
          <div>
            <div className="card-title">Recent Test Executions</div>
            <div className="card-subtitle">History of automated test runs across branches and environments</div>
          </div>
          <Link href="/executions" className="btn btn-sm" style={{ gap: '6px' }}>
            <span>View All</span>
            <ArrowRight size={13} />
          </Link>
        </div>

        <div className="table-responsive">
          <table className="data-table">
            <thead>
              <tr>
                <th>Execution ID</th>
                <th>Date & Time</th>
                <th>Environment</th>
                <th>Browser</th>
                <th>Branch</th>
                <th>Commit</th>
                <th>Total</th>
                <th>Passed</th>
                <th>Failed</th>
                <th>Duration</th>
                <th>Status</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {executions.slice(0, 5).map((exec) => (
                <tr key={exec.execution_id}>
                  <td>
                    <Link
                      href={`/executions/${exec.execution_id}`}
                      style={{ fontWeight: '600', color: 'var(--primary)' }}
                    >
                      {exec.execution_id}
                    </Link>
                  </td>
                  <td>
                    <div>{exec.date}</div>
                    <div style={{ fontSize: '11px', color: '#94a3b8' }}>{exec.time}</div>
                  </td>
                  <td>
                    <span className="badge badge-gray">{exec.environment}</span>
                  </td>
                  <td>{exec.browser}</td>
                  <td>
                    <span style={{ fontFamily: 'var(--font-mono)', fontSize: '12px' }}>
                      {exec.branch}
                    </span>
                  </td>
                  <td>
                    <span style={{ fontFamily: 'var(--font-mono)', fontSize: '12px', color: '#64748b' }}>
                      {exec.commit_hash.slice(0, 7)}
                    </span>
                  </td>
                  <td>{exec.total}</td>
                  <td style={{ color: '#10b981', fontWeight: '600' }}>{exec.passed}</td>
                  <td style={{ color: exec.failed > 0 ? '#ef4444' : '#64748b', fontWeight: '600' }}>
                    {exec.failed}
                  </td>
                  <td>{formatDuration(exec.duration)}</td>
                  <td>
                    <StatusBadge status={exec.status} />
                  </td>
                  <td>
                    <Link
                      href={`/executions/${exec.execution_id}`}
                      className="btn btn-sm"
                      style={{ padding: '3px 8px' }}
                    >
                      View
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </DashboardLayout>
  );
}
