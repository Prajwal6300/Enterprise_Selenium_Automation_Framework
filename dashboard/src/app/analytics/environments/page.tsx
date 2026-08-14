import React from 'react';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { StatusBadge } from '@/components/common/StatusBadge';
import { getEnvironmentAnalytics } from '@/lib/result-parser';
import { Layers, CheckCircle2, XCircle, Clock, ShieldCheck, Activity } from 'lucide-react';

export const dynamic = 'force-dynamic';
export const revalidate = 0;

export default async function EnvironmentAnalyticsPage() {
  const envs = getEnvironmentAnalytics();

  return (
    <DashboardLayout>
      <div className="page-header">
        <div className="page-title-group">
          <h1>Environment Quality & Stability Analytics</h1>
          <p>
            Multi-tier environment performance across QA (Validation), UAT (Staging), and PROD (Production Smoke).
          </p>
        </div>
      </div>

      {/* Environment KPI Grid */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
          gap: '20px',
          marginBottom: '24px',
        }}
      >
        {envs.map((env) => (
          <div key={env.environment} className="card">
            <div className="card-header">
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <div
                  style={{
                    width: '36px',
                    height: '36px',
                    borderRadius: '8px',
                    backgroundColor: env.environment === 'PROD' ? '#ecfdf5' : '#eff6ff',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                  }}
                >
                  <Layers size={18} color={env.environment === 'PROD' ? '#10b981' : '#2563eb'} />
                </div>
                <div>
                  <h3 style={{ fontSize: '16px', fontWeight: '700', color: '#0f172a' }}>
                    {env.environment} Environment
                  </h3>
                  <span style={{ fontSize: '11px', color: '#64748b' }}>
                    {env.environment === 'PROD'
                      ? 'Production Smoke Verification'
                      : env.environment === 'UAT'
                      ? 'Pre-Release Staging Suite'
                      : 'Active Development & Regression'}
                  </span>
                </div>
              </div>
              <span
                style={{
                  fontSize: '14px',
                  fontWeight: '700',
                  color: env.pass_rate >= 95 ? '#10b981' : '#ef4444',
                }}
              >
                {env.pass_rate}%
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
                <span style={{ color: '#64748b', fontSize: '11px' }}>Total Runs</span>
                <div style={{ fontWeight: '700', fontSize: '16px', color: '#0f172a' }}>
                  {env.total_executions} runs
                </div>
              </div>
              <div>
                <span style={{ color: '#64748b', fontSize: '11px' }}>Tests Verified</span>
                <div style={{ fontWeight: '600', fontSize: '14px', color: '#0f172a' }}>
                  {env.total_tests} tests
                </div>
              </div>
              <div>
                <span style={{ color: '#64748b', fontSize: '11px' }}>Passed / Failed</span>
                <div style={{ fontWeight: '600' }}>
                  <span style={{ color: '#10b981' }}>{env.passed}</span> /{' '}
                  <span style={{ color: env.failed > 0 ? '#ef4444' : '#64748b' }}>{env.failed}</span>
                </div>
              </div>
              <div>
                <span style={{ color: '#64748b', fontSize: '11px' }}>Avg Runtime</span>
                <div style={{ fontWeight: '600', color: '#2563eb' }}>{env.avg_duration}s</div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Environment Matrix Table */}
      <div className="card">
        <div className="card-header">
          <div className="card-title">Environment Stability Ledger</div>
        </div>

        <div className="table-responsive">
          <table className="data-table">
            <thead>
              <tr>
                <th>Environment</th>
                <th>Base URL Target</th>
                <th>Total Runs</th>
                <th>Total Tests</th>
                <th>Passed</th>
                <th>Failures</th>
                <th>Pass Rate</th>
                <th>Avg Duration</th>
                <th>Health</th>
              </tr>
            </thead>
            <tbody>
              {envs.map((env) => (
                <tr key={env.environment}>
                  <td>
                    <span className="badge badge-gray" style={{ fontWeight: '700' }}>
                      {env.environment}
                    </span>
                  </td>
                  <td style={{ fontFamily: 'var(--font-mono)', fontSize: '12px' }}>
                    {env.environment === 'PROD'
                      ? 'https://www.saucedemo.com'
                      : env.environment === 'UAT'
                      ? 'https://uat.saucedemo.com'
                      : 'https://qa.saucedemo.com'}
                  </td>
                  <td>{env.total_executions}</td>
                  <td>{env.total_tests}</td>
                  <td style={{ color: '#10b981', fontWeight: '600' }}>{env.passed}</td>
                  <td style={{ color: env.failed > 0 ? '#ef4444' : '#64748b', fontWeight: '600' }}>
                    {env.failed}
                  </td>
                  <td style={{ fontWeight: '700', color: env.pass_rate >= 95 ? '#10b981' : '#ef4444' }}>
                    {env.pass_rate}%
                  </td>
                  <td>{env.avg_duration}s</td>
                  <td>
                    <StatusBadge status={env.pass_rate >= 95 ? 'PASSED' : 'PASSED'} />
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
