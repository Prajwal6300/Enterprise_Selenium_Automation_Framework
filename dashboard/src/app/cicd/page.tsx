import React from 'react';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { StatusBadge } from '@/components/common/StatusBadge';
import { getCicdStatus } from '@/lib/result-parser';
import {
  GitBranch,
  Play,
  CheckCircle2,
  Clock,
  FileCode2,
  ExternalLink,
  ShieldCheck,
  Server,
  Layers,
  Box,
} from 'lucide-react';

export const dynamic = 'force-dynamic';
export const revalidate = 0;

export default async function CicdPage() {
  const pipelines = getCicdStatus();

  const getProviderIcon = (provider: string) => {
    switch (provider) {
      case 'GitHub Actions':
        return GitBranch;
      case 'Jenkins':
        return Server;
      case 'BrowserStack':
        return Layers;
      case 'Docker':
        return Box;
      default:
        return GitBranch;
    }
  };

  return (
    <DashboardLayout>
      <div className="page-header">
        <div className="page-title-group">
          <h1>Continuous Integration & Cloud Execution Pipelines</h1>
          <p>
            Automated test runners across GitHub Actions, Jenkins Declarative Pipelines, Docker Containers, and BrowserStack Cloud Grid.
          </p>
        </div>
      </div>

      {/* Pipelines Grid */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))',
          gap: '20px',
          marginBottom: '24px',
        }}
      >
        {pipelines.map((p) => {
          const Icon = getProviderIcon(p.provider);
          return (
            <div
              key={p.provider}
              className="card"
              style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}
            >
              <div>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '14px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <div
                      style={{
                        width: '38px',
                        height: '38px',
                        borderRadius: '8px',
                        backgroundColor: '#eff6ff',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                      }}
                    >
                      <Icon size={18} color="#2563eb" />
                    </div>
                    <div>
                      <h3 style={{ fontSize: '15px', fontWeight: '700', color: '#0f172a' }}>
                        {p.provider}
                      </h3>
                      <span style={{ fontSize: '11px', color: '#64748b' }}>{p.name}</span>
                    </div>
                  </div>
                  <StatusBadge status={p.status} />
                </div>

                <p style={{ fontSize: '13px', color: '#475569', lineHeight: '1.5', marginBottom: '16px' }}>
                  {p.details}
                </p>
              </div>

              <div>
                <div
                  style={{
                    backgroundColor: '#f8fafc',
                    padding: '12px 14px',
                    borderRadius: '8px',
                    border: '1px solid var(--border-color)',
                    fontSize: '12px',
                    marginBottom: '14px',
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '6px',
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span style={{ color: '#64748b' }}>Last Run:</span>
                    <strong>{p.last_run}</strong>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span style={{ color: '#64748b' }}>Duration:</span>
                    <strong>{p.duration}</strong>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span style={{ color: '#64748b' }}>Target Branch:</span>
                    <strong style={{ fontFamily: 'var(--font-mono)' }}>{p.branch}</strong>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span style={{ color: '#64748b' }}>Commit:</span>
                    <code style={{ fontFamily: 'var(--font-mono)', color: '#2563eb' }}>
                      {p.commit_hash.slice(0, 7)}
                    </code>
                  </div>
                  {p.workflow_file && (
                    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                      <span style={{ color: '#64748b' }}>Config File:</span>
                      <code style={{ fontFamily: 'var(--font-mono)' }}>{p.workflow_file}</code>
                    </div>
                  )}
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <span
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '5px',
                      fontSize: '12px',
                      color: '#10b981',
                      fontWeight: '600',
                    }}
                  >
                    <ShieldCheck size={14} />
                    <span>Pipeline Active</span>
                  </span>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </DashboardLayout>
  );
}
