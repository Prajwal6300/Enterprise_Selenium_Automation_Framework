import React from 'react';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { getAvailableReports } from '@/lib/result-parser';
import {
  FileText,
  Download,
  ExternalLink,
  FileCode2,
  FileSpreadsheet,
  FileBox,
  Calendar,
  HardDrive,
  LayoutDashboard,
} from 'lucide-react';

export const dynamic = 'force-dynamic';
export const revalidate = 0;

export default async function ReportsPage() {
  const reports = getAvailableReports();

  const getReportIcon = (type: string) => {
    switch (type) {
      case 'executive':
        return LayoutDashboard;
      case 'html':
        return FileText;
      case 'allure':
        return FileBox;
      case 'junit':
        return FileCode2;
      case 'excel':
      case 'csv':
        return FileSpreadsheet;
      case 'pdf':
        return FileText;
      default:
        return FileCode2;
    }
  };

  return (
    <DashboardLayout>
      <div className="page-header">
        <div className="page-title-group">
          <h1>Enterprise Reports Hub</h1>
          <p>
            Multi-format test artifacts, executive summaries, compliance reports, and CI/CD data exports.
          </p>
        </div>
      </div>

      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))',
          gap: '20px',
        }}
      >
        {reports.map((report) => {
          const Icon = getReportIcon(report.type);
          return (
            <div
              key={report.id}
              className="card"
              style={{
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between',
              }}
            >
              <div>
                <div style={{ display: 'flex', alignItems: 'flex-start', gap: '14px', marginBottom: '12px' }}>
                  <div
                    style={{
                      width: '40px',
                      height: '40px',
                      borderRadius: '10px',
                      backgroundColor: '#eff6ff',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      flexShrink: 0,
                    }}
                  >
                    <Icon size={20} color="#2563eb" />
                  </div>
                  <div>
                    <h3 style={{ fontSize: '15px', fontWeight: '700', color: '#0f172a' }}>
                      {report.title}
                    </h3>
                    <span
                      style={{
                        fontSize: '11px',
                        fontWeight: '600',
                        color: '#64748b',
                        textTransform: 'uppercase',
                        letterSpacing: '0.04em',
                      }}
                    >
                      {report.type} artifact
                    </span>
                  </div>
                </div>

                <p style={{ fontSize: '13px', color: '#475569', lineHeight: '1.5', marginBottom: '16px' }}>
                  {report.description}
                </p>
              </div>

              <div>
                <div
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    padding: '10px 12px',
                    backgroundColor: '#f8fafc',
                    borderRadius: '8px',
                    fontSize: '12px',
                    color: '#64748b',
                    marginBottom: '16px',
                    border: '1px solid var(--border-color)',
                  }}
                >
                  <span style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                    <Calendar size={13} color="#94a3b8" />
                    <span>{report.generated_at}</span>
                  </span>
                  <span style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                    <HardDrive size={13} color="#94a3b8" />
                    <span>{report.file_size}</span>
                  </span>
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                  {report.view_url && (
                    <a
                      href={report.view_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="btn btn-sm btn-primary"
                      style={{ flex: 1, gap: '6px' }}
                    >
                      <ExternalLink size={13} />
                      <span>View Report</span>
                    </a>
                  )}

                  <a
                    href={report.download_url}
                    download
                    className="btn btn-sm"
                    style={{ flex: report.view_url ? undefined : 1, gap: '6px' }}
                  >
                    <Download size={13} color="#64748b" />
                    <span>Download</span>
                  </a>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </DashboardLayout>
  );
}
