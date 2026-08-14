import React from 'react';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { KpiCard } from '@/components/common/KpiCard';
import { StatusBadge } from '@/components/common/StatusBadge';
import { getBrowserAnalytics } from '@/lib/result-parser';
import { Globe2, Chrome, CheckCircle2, XCircle, Clock, TrendingUp } from 'lucide-react';

export const dynamic = 'force-dynamic';
export const revalidate = 0;

export default async function BrowserAnalyticsPage() {
  const browsers = getBrowserAnalytics();

  return (
    <DashboardLayout>
      <div className="page-header">
        <div className="page-title-group">
          <h1>Browser Analytics & Compatibility Matrix</h1>
          <p>
            Cross-browser reliability, execution durations, and stability metrics across WebDrivers and BrowserStack.
          </p>
        </div>
      </div>

      {/* Browser Comparison Cards */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))',
          gap: '20px',
          marginBottom: '24px',
        }}
      >
        {browsers.map((b) => (
          <div key={b.browser} className="card">
            <div className="card-header">
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <div
                  style={{
                    width: '36px',
                    height: '36px',
                    borderRadius: '8px',
                    backgroundColor: '#eff6ff',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                  }}
                >
                  <Globe2 size={18} color="#2563eb" />
                </div>
                <div>
                  <h3 style={{ fontSize: '16px', fontWeight: '700', color: '#0f172a' }}>
                    {b.browser}
                  </h3>
                  <span style={{ fontSize: '11px', color: '#64748b' }}>
                    {b.browser === 'BrowserStack' ? 'Cloud Automation' : 'Headless WebDriver'}
                  </span>
                </div>
              </div>
              <span
                style={{
                  fontSize: '14px',
                  fontWeight: '700',
                  color: b.pass_rate >= 95 ? '#10b981' : '#ef4444',
                }}
              >
                {b.pass_rate}%
              </span>
            </div>

            <div
              style={{
                display: 'grid',
                gridTemplateColumns: '1fr 1fr',
                gap: '12px',
                marginTop: '12px',
                paddingTop: '12px',
                borderTop: '1px solid var(--border-color)',
                fontSize: '13px',
              }}
            >
              <div>
                <span style={{ color: '#64748b', fontSize: '11px' }}>Total Tests</span>
                <div style={{ fontWeight: '700', fontSize: '16px', color: '#0f172a' }}>{b.total_tests}</div>
              </div>
              <div>
                <span style={{ color: '#64748b', fontSize: '11px' }}>Passed / Failed</span>
                <div style={{ fontWeight: '600', fontSize: '14px' }}>
                  <span style={{ color: '#10b981' }}>{b.passed}</span> / <span style={{ color: b.failed > 0 ? '#ef4444' : '#64748b' }}>{b.failed}</span>
                </div>
              </div>
              <div style={{ gridColumn: 'span 2' }}>
                <span style={{ color: '#64748b', fontSize: '11px' }}>Avg Duration</span>
                <div style={{ fontWeight: '600', color: '#2563eb' }}>{b.avg_duration}s per test suite</div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Deep Comparison Table */}
      <div className="card">
        <div className="card-header">
          <div className="card-title">Cross-Browser Execution Matrix</div>
        </div>

        <div className="table-responsive">
          <table className="data-table">
            <thead>
              <tr>
                <th>Browser</th>
                <th>Target Platform</th>
                <th>Total Executions</th>
                <th>Passed</th>
                <th>Failed</th>
                <th>Pass Rate</th>
                <th>Avg Duration</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {browsers.map((b) => (
                <tr key={b.browser}>
                  <td style={{ fontWeight: '600', color: 'var(--text-primary)' }}>{b.browser}</td>
                  <td>
                    {b.browser === 'BrowserStack' ? 'Windows 11 / macOS Sonoma' : 'Local / CI Headless (Linux/Win)'}
                  </td>
                  <td>{b.total_tests}</td>
                  <td style={{ color: '#10b981', fontWeight: '600' }}>{b.passed}</td>
                  <td style={{ color: b.failed > 0 ? '#ef4444' : '#64748b', fontWeight: '600' }}>
                    {b.failed}
                  </td>
                  <td style={{ fontWeight: '700', color: b.pass_rate >= 95 ? '#10b981' : '#ef4444' }}>
                    {b.pass_rate}%
                  </td>
                  <td>{b.avg_duration}s</td>
                  <td>
                    <StatusBadge status={b.failed === 0 ? 'PASSED' : 'PASSED'} />
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
