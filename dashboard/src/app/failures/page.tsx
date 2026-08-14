import React from 'react';
import Link from 'next/link';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { StatusBadge } from '@/components/common/StatusBadge';
import { FailureTrendLine } from '@/components/charts/DashboardCharts';
import { getFailureAnalysis, getAllExecutions } from '@/lib/result-parser';
import {
  AlertOctagon,
  Camera,
  Layers,
  Globe2,
  Calendar,
  ArrowRight,
  TrendingDown,
} from 'lucide-react';
import { FailureAnalysisClient } from './FailureAnalysisClient';

export const dynamic = 'force-dynamic';
export const revalidate = 0;

export default async function FailuresPage() {
  const failures = getFailureAnalysis();
  const executions = getAllExecutions();

  const reversed = [...executions].reverse();
  const trendLabels = reversed.map((e) => e.execution_id.replace('EXEC-', '#'));
  const failureCounts = reversed.map((e) => e.failed);

  return (
    <DashboardLayout>
      <div className="page-header">
        <div className="page-title-group">
          <h1>Failure Analysis & Diagnostic Engine</h1>
          <p>
            Automated clustering and historical recurrence tracking for test regressions and UI exceptions.
          </p>
        </div>
      </div>

      {/* Failure Trend Chart */}
      <div className="card" style={{ marginBottom: '24px' }}>
        <div className="card-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <TrendingDown size={16} color="#ef4444" />
            <div className="card-title">Failure Rate Trend</div>
          </div>
          <span style={{ fontSize: '12px', color: '#64748b' }}>
            {failures.length} unique failed test signatures recorded
          </span>
        </div>
        <FailureTrendLine labels={trendLabels} failures={failureCounts} />
      </div>

      {/* Failure Groups Table */}
      <FailureAnalysisClient failures={failures} />
    </DashboardLayout>
  );
}
