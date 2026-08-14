import React from 'react';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { Settings, ShieldCheck, Database, Key, Globe2, Save } from 'lucide-react';

export const revalidate = 0;

export default function SettingsPage() {
  const hasPg = !!process.env.DATABASE_URL;

  return (
    <DashboardLayout>
      <div className="page-header">
        <div className="page-title-group">
          <h1>Platform Settings & Configuration</h1>
          <p>Manage telemetry storage engines, authentication policies, and CI/CD ingestion endpoints.</p>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(450px, 1fr))', gap: '24px' }}>
        {/* Database & Storage */}
        <div className="card">
          <div className="card-header">
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <Database size={18} color="#2563eb" />
              <div className="card-title">Data Storage Configuration</div>
            </div>
            <span className="badge badge-gray">{hasPg ? 'PostgreSQL' : 'JSON File Store'}</span>
          </div>

          <div style={{ fontSize: '13px', color: '#475569', lineHeight: '1.6', marginBottom: '16px' }}>
            {hasPg ? (
              <p>The dashboard is currently connected to remote PostgreSQL via <code>DATABASE_URL</code>.</p>
            ) : (
              <p>
                The dashboard is running in <strong>Local High-Performance JSON File Store</strong> mode. Test
                results from <code>reports/executions/*.json</code> and <code>reports/junit/results.xml</code> are
                loaded directly.
              </p>
            )}
          </div>

          <div style={{ padding: '12px', backgroundColor: '#f8fafc', borderRadius: '8px', border: '1px solid var(--border-color)', fontSize: '12px' }}>
            <div style={{ color: '#64748b', marginBottom: '4px' }}>Target PostgreSQL Connection String:</div>
            <code style={{ fontFamily: 'var(--font-mono)', color: '#0f172a' }}>
              {hasPg ? 'postgresql://***:***@postgres-host:5432/qa_telemetry' : 'DATABASE_URL not set (using file storage)'}
            </code>
          </div>
        </div>

        {/* Security & Secrets */}
        <div className="card">
          <div className="card-header">
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <ShieldCheck size={18} color="#10b981" />
              <div className="card-title">Security & Secret Redaction</div>
            </div>
            <span className="badge badge-passed">Active</span>
          </div>

          <p style={{ fontSize: '13px', color: '#475569', lineHeight: '1.6', marginBottom: '14px' }}>
            Automatic secret masking is enforced across all API responses, log streams, and screenshot metadata.
          </p>

          <ul style={{ paddingLeft: '20px', fontSize: '12.5px', color: '#475569', lineHeight: '1.8' }}>
            <li>Passwords & credentials automatically redacted</li>
            <li>BrowserStack access keys masked</li>
            <li>Database connection passwords masked</li>
            <li>Bearer & authorization tokens replaced with <code>***REDACTED***</code></li>
          </ul>
        </div>

        {/* CI/CD Ingestion API */}
        <div className="card">
          <div className="card-header">
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <Key size={18} color="#f59e0b" />
              <div className="card-title">Telemetry Ingestion Webhook</div>
            </div>
          </div>

          <p style={{ fontSize: '13px', color: '#475569', lineHeight: '1.6', marginBottom: '14px' }}>
            CI/CD runners (GitHub Actions & Jenkins) can push test run results to this dashboard via HTTP POST:
          </p>

          <div style={{ padding: '12px', backgroundColor: '#0f172a', color: '#38bdf8', borderRadius: '8px', fontSize: '12px', fontFamily: 'var(--font-mono)' }}>
            POST /api/executions<br />
            Content-Type: application/json<br />
            X-API-Key: ***REDACTED***
          </div>
        </div>

        {/* Quality Thresholds */}
        <div className="card">
          <div className="card-header">
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <Globe2 size={18} color="#8b5cf6" />
              <div className="card-title">Quality Gate Thresholds</div>
            </div>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', fontSize: '13px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 12px', backgroundColor: '#f8fafc', borderRadius: '6px' }}>
              <span>Minimum Pass Rate:</span>
              <strong style={{ color: '#10b981' }}>95.0%</strong>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 12px', backgroundColor: '#f8fafc', borderRadius: '6px' }}>
              <span>Max Allowable Flakiness:</span>
              <strong style={{ color: '#f59e0b' }}>2.0%</strong>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 12px', backgroundColor: '#f8fafc', borderRadius: '6px' }}>
              <span>Max Suite Duration:</span>
              <strong style={{ color: '#2563eb' }}>120 seconds</strong>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
