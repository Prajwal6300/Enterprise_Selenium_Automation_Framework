import React from 'react';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { KpiCard } from '@/components/common/KpiCard';
import { StatusBadge } from '@/components/common/StatusBadge';
import { getExecutionById } from '@/lib/result-parser';
import {
  ArrowLeft,
  Calendar,
  Clock,
  Globe2,
  Layers,
  GitBranch,
  FileCode2,
  Server,
  Download,
  CheckCircle2,
  XCircle,
  AlertTriangle,
} from 'lucide-react';

export const dynamic = 'force-dynamic';
export const revalidate = 0;

export default async function ExecutionDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const execution = getExecutionById(id);

  if (!execution) {
    notFound();
  }

  const formatDuration = (s: number) => {
    const mins = Math.floor(s / 60);
    const secs = Math.round(s % 60);
    return `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
  };

  return (
    <DashboardLayout environment={execution.environment}>
      {/* Header */}
      <div className="page-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <Link href="/executions" className="btn btn-sm btn-icon">
            <ArrowLeft size={16} />
          </Link>
          <div className="page-title-group">
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <h1>{execution.execution_id}</h1>
              <StatusBadge status={execution.status} size="md" />
            </div>
            <p>
              Executed on {execution.date} at {execution.time} via {execution.ci_system}
            </p>
          </div>
        </div>

        <div className="header-actions">
          <a
            href={`/api/reports/execution-json`}
            download={`${execution.execution_id}.json`}
            className="btn btn-sm"
          >
            <Download size={13} color="#64748b" />
            <span>Download JSON</span>
          </a>
        </div>
      </div>

      {/* Metadata Card */}
      <div
        className="card"
        style={{
          marginBottom: '24px',
          padding: '16px 20px',
          backgroundColor: '#f8fafc',
          border: '1px solid var(--border-color)',
        }}
      >
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
            gap: '16px',
            fontSize: '13px',
          }}
        >
          <div>
            <span style={{ color: '#64748b', fontSize: '11px', textTransform: 'uppercase', fontWeight: '600' }}>
              Environment & Browser
            </span>
            <div style={{ marginTop: '4px', fontWeight: '600', color: '#0f172a' }}>
              {execution.environment} | {execution.browser}
            </div>
          </div>

          <div>
            <span style={{ color: '#64748b', fontSize: '11px', textTransform: 'uppercase', fontWeight: '600' }}>
              Branch & Commit
            </span>
            <div style={{ marginTop: '4px', fontFamily: 'var(--font-mono)', fontWeight: '600', color: '#0f172a' }}>
              {execution.branch} @ {execution.commit_hash.slice(0, 7)}
            </div>
          </div>

          <div>
            <span style={{ color: '#64748b', fontSize: '11px', textTransform: 'uppercase', fontWeight: '600' }}>
              Host Machine / OS
            </span>
            <div style={{ marginTop: '4px', fontWeight: '500', color: '#0f172a' }}>
              {execution.host_machine || 'Localhost'} ({execution.operating_system || 'Win64'})
            </div>
          </div>

          <div>
            <span style={{ color: '#64748b', fontSize: '11px', textTransform: 'uppercase', fontWeight: '600' }}>
              Runtimes
            </span>
            <div style={{ marginTop: '4px', fontSize: '12px', color: '#475569' }}>
              Python {execution.python_version || '3.13'} | Selenium {execution.selenium_version || '4.28'}
            </div>
          </div>
        </div>
      </div>

      {/* KPI Grid */}
      <div className="kpi-grid">
        <KpiCard title="Total Tests" value={execution.total} variant="primary" />
        <KpiCard title="Passed" value={execution.passed} variant="success" />
        <KpiCard title="Failed" value={execution.failed} variant={execution.failed > 0 ? 'danger' : 'default'} />
        <KpiCard title="Skipped" value={execution.skipped} variant="warning" />
        <KpiCard title="Pass Rate" value={`${execution.pass_rate}%`} variant="success" />
        <KpiCard title="Total Duration" value={formatDuration(execution.duration)} subtext={`${execution.duration}s`} variant="default" />
      </div>

      {/* Test Cases Table */}
      <div className="card">
        <div className="card-header">
          <div>
            <div className="card-title">Test Cases in this Execution ({execution.tests.length})</div>
            <div className="card-subtitle">Detailed step results, duration, and failure diagnostics</div>
          </div>
        </div>

        <div className="table-responsive">
          <table className="data-table">
            <thead>
              <tr>
                <th>Status</th>
                <th>Test Case Name</th>
                <th>Module</th>
                <th>Type</th>
                <th>Steps</th>
                <th>Duration</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {execution.tests.map((test) => (
                <tr key={test.test_id}>
                  <td>
                    <StatusBadge status={test.status} />
                  </td>
                  <td>
                    <Link
                      href={`/tests/${test.name}`}
                      style={{ fontWeight: '600', color: 'var(--primary)' }}
                    >
                      {test.name}
                    </Link>
                    <div style={{ fontSize: '11.5px', color: '#94a3b8', fontFamily: 'var(--font-mono)', marginTop: '2px' }}>
                      {test.file_path}
                    </div>
                  </td>
                  <td>
                    <span className="badge badge-gray">{test.module}</span>
                  </td>
                  <td>
                    <span className="badge badge-blue">{test.test_type}</span>
                  </td>
                  <td>
                    <span style={{ fontSize: '12px', color: '#475569' }}>
                      {test.steps?.length || 5} steps
                    </span>
                  </td>
                  <td>{test.duration}s</td>
                  <td>
                    <Link
                      href={`/tests/${test.name}`}
                      className="btn btn-sm"
                      style={{ padding: '3px 8px' }}
                    >
                      Details
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
