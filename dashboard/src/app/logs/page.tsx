import React from 'react';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { getFrameworkLogs } from '@/lib/result-parser';
import { LogViewerClient } from './LogViewerClient';

export const dynamic = 'force-dynamic';
export const revalidate = 0;

export default async function LogsPage() {
  const { lines, total } = getFrameworkLogs();

  return (
    <DashboardLayout>
      <div className="page-header">
        <div className="page-title-group">
          <h1>Execution Logs</h1>
          <p>
            Real-time framework and Selenium WebDriver execution streams with automatic secret redaction.
          </p>
        </div>
      </div>

      <LogViewerClient initialLines={lines} totalLines={total} />
    </DashboardLayout>
  );
}
