import React from 'react';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { getSystemHealth } from '@/lib/result-parser';
import { Activity, CheckCircle2, AlertTriangle, Server, Database, GitBranch, RefreshCw } from 'lucide-react';

export const dynamic = 'force-dynamic';
export const revalidate = 0;

export default async function HealthPage() {
  const health = getSystemHealth();

  return (
    <DashboardLayout>
      <div className="page-header">
        <div className="page-title-group">
          <h1>System Health & Infrastructure Diagnostics</h1>
          <p>
            Real-time operational status of the QA Dashboard API, telemetry storage, and CI/CD connectors.
          </p>
        </div>
      </div>

      {/* Overall Health Card */}
      <div
        className="card"
        style={{
          marginBottom: '24px',
          padding: '20px',
          backgroundColor: health.status === 'HEALTHY' ? '#ecfdf5' : '#fffbeb',
          border: `1px solid ${health.status === 'HEALTHY' ? '#a7f3d0' : '#fde68a'}`,
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '12px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div
              style={{
                width: '40px',
                height: '40px',
                borderRadius: '50%',
                backgroundColor: health.status === 'HEALTHY' ? '#d1fae5' : '#fef3c7',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              <Activity size={20} color={health.status === 'HEALTHY' ? '#059669' : '#d97706'} />
            </div>
            <div>
              <h2 style={{ fontSize: '17px', fontWeight: '700', color: health.status === 'HEALTHY' ? '#065f46' : '#92400e' }}>
                All Systems Operational ({health.status})
              </h2>
              <div style={{ fontSize: '12px', color: '#64748b' }}>
                Framework version {health.version} | Uptime: {Math.round(health.uptime_seconds / 60)} minutes
              </div>
            </div>
          </div>

          <div style={{ fontSize: '12px', color: '#64748b' }}>
            Last Diagnostic Check: <strong>{new Date(health.timestamp).toLocaleTimeString()}</strong>
          </div>
        </div>
      </div>

      {/* Component Status Grid */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))',
          gap: '20px',
        }}
      >
        {/* Dashboard API */}
        <div className="card">
          <div className="card-header">
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <Server size={18} color="#2563eb" />
              <div className="card-title">Dashboard REST API</div>
            </div>
            <span className="badge badge-passed">✓ Healthy</span>
          </div>
          <p style={{ fontSize: '13px', color: '#475569', lineHeight: '1.5' }}>
            {health.components.dashboard_api.message}
          </p>
          <div style={{ marginTop: '12px', fontSize: '12px', color: '#94a3b8' }}>
            Endpoint: <code>/api/health</code>
          </div>
        </div>

        {/* Database */}
        <div className="card">
          <div className="card-header">
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <Database size={18} color="#06b6d4" />
              <div className="card-title">Data Storage Layer</div>
            </div>
            <span className="badge badge-passed">✓ Healthy</span>
          </div>
          <p style={{ fontSize: '13px', color: '#475569', lineHeight: '1.5' }}>
            {health.components.database.message}
          </p>
          <div style={{ marginTop: '12px', fontSize: '12px', color: '#64748b' }}>
            Active Mode: <strong>{health.components.database.type}</strong>
          </div>
        </div>

        {/* Test Results */}
        <div className="card">
          <div className="card-header">
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <CheckCircle2 size={18} color="#10b981" />
              <div className="card-title">Test Telemetry Store</div>
            </div>
            <span className="badge badge-passed">✓ Available</span>
          </div>
          <p style={{ fontSize: '13px', color: '#475569', lineHeight: '1.5' }}>
            {health.components.test_results.total_executions} historical test execution records loaded.
          </p>
          <div style={{ marginTop: '12px', fontSize: '12px', color: '#64748b' }}>
            Latest: <strong>{health.components.test_results.latest_execution}</strong>
          </div>
        </div>

        {/* GitHub Actions */}
        <div className="card">
          <div className="card-header">
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <GitBranch size={18} color="#f59e0b" />
              <div className="card-title">GitHub Actions CI</div>
            </div>
            <span className="badge badge-passed">✓ Connected</span>
          </div>
          <p style={{ fontSize: '13px', color: '#475569', lineHeight: '1.5' }}>
            {health.components.github_actions.message}
          </p>
        </div>

        {/* Jenkins */}
        <div className="card">
          <div className="card-header">
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <Server size={18} color="#8b5cf6" />
              <div className="card-title">Jenkins Automation Server</div>
            </div>
            <span className="badge badge-passed">✓ Configured</span>
          </div>
          <p style={{ fontSize: '13px', color: '#475569', lineHeight: '1.5' }}>
            {health.components.jenkins.message}
          </p>
        </div>

        {/* BrowserStack */}
        <div className="card">
          <div className="card-header">
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <Activity size={18} color="#ec4899" />
              <div className="card-title">BrowserStack Cloud Grid</div>
            </div>
            <span className="badge badge-passed">✓ Configured</span>
          </div>
          <p style={{ fontSize: '13px', color: '#475569', lineHeight: '1.5' }}>
            {health.components.browserstack.message}
          </p>
        </div>
      </div>
    </DashboardLayout>
  );
}
