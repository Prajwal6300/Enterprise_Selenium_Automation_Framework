'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { FailureGroup } from '@/lib/types';
import { ScreenshotModal } from '@/components/modals/ScreenshotModal';
import { EmptyState } from '@/components/common/FeedbackStates';
import { Camera, AlertOctagon, ArrowRight, Layers, Globe2 } from 'lucide-react';

interface FailureAnalysisClientProps {
  failures: FailureGroup[];
}

export const FailureAnalysisClient: React.FC<FailureAnalysisClientProps> = ({
  failures,
}) => {
  const [selectedScreenshot, setSelectedScreenshot] = useState<{
    url: string;
    testName: string;
    browser: string;
    environment: string;
  } | null>(null);

  if (failures.length === 0) {
    return (
      <EmptyState
        title="Zero Test Failures Recorded"
        message="All executed test suites across environments have achieved 100% pass rate."
      />
    );
  }

  return (
    <div className="card">
      <div className="card-header">
        <div className="card-title">Recurring Failure Signatures</div>
        <span style={{ fontSize: '12px', color: '#64748b' }}>
          Sorted by recurrence count
        </span>
      </div>

      <div className="table-responsive">
        <table className="data-table">
          <thead>
            <tr>
              <th>Failed Test</th>
              <th>Exception / Error Type</th>
              <th>Module</th>
              <th>Browser</th>
              <th>Environment</th>
              <th>Recurrence</th>
              <th>First / Last Seen</th>
              <th>Screenshot</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {failures.map((f, idx) => {
              const screenshotUrl =
                f.screenshot_uri ||
                (f.screenshot_path
                  ? `/api/screenshots/${encodeURIComponent(f.screenshot_path.split(/[\\/]/).pop() || '')}`
                  : '/api/screenshots/test_complete_checkout_successfully_20260731_135220_159130.png');

              return (
                <tr key={idx}>
                  <td>
                    <Link
                      href={`/tests/${f.test_name}`}
                      style={{ fontWeight: '600', color: 'var(--primary)' }}
                    >
                      {f.test_name}
                    </Link>
                  </td>
                  <td>
                    <div style={{ fontWeight: '600', color: '#991b1b', fontSize: '12.5px' }}>
                      {f.failure_category}
                    </div>
                    <div
                      style={{
                        fontSize: '11.5px',
                        color: '#64748b',
                        maxWidth: '280px',
                        overflow: 'hidden',
                        textOverflow: 'ellipsis',
                        whiteSpace: 'nowrap',
                      }}
                    >
                      {f.error_message}
                    </div>
                  </td>
                  <td>
                    <span className="badge badge-gray">{f.module}</span>
                  </td>
                  <td>{f.browser}</td>
                  <td>
                    <span className="badge badge-gray">{f.environment}</span>
                  </td>
                  <td>
                    <span
                      style={{
                        display: 'inline-block',
                        padding: '2px 8px',
                        borderRadius: '4px',
                        backgroundColor: '#fee2e2',
                        color: '#991b1b',
                        fontWeight: '700',
                        fontSize: '12px',
                      }}
                    >
                      {f.failure_count} failures
                    </span>
                  </td>
                  <td>
                    <div style={{ fontSize: '12px', color: '#0f172a' }}>{f.last_seen}</div>
                    <div style={{ fontSize: '11px', color: '#94a3b8' }}>First: {f.first_seen}</div>
                  </td>
                  <td>
                    <button
                      onClick={() =>
                        setSelectedScreenshot({
                          url: screenshotUrl,
                          testName: f.test_name,
                          browser: f.browser,
                          environment: f.environment,
                        })
                      }
                      className="btn btn-sm btn-icon"
                      title="Inspect failure screenshot"
                      style={{ backgroundColor: '#fef2f2', borderColor: '#fecaca' }}
                    >
                      <Camera size={14} color="#ef4444" />
                    </button>
                  </td>
                  <td>
                    <Link
                      href={`/tests/${f.test_name}`}
                      className="btn btn-sm"
                      style={{ padding: '3px 8px' }}
                    >
                      Diagnose
                    </Link>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {selectedScreenshot && (
        <ScreenshotModal
          isOpen={true}
          onClose={() => setSelectedScreenshot(null)}
          screenshotUrl={selectedScreenshot.url}
          testName={selectedScreenshot.testName}
          browser={selectedScreenshot.browser}
          environment={selectedScreenshot.environment}
        />
      )}
    </div>
  );
};
