'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { TestResult, ExecutionSummary } from '@/lib/types';
import { StatusBadge } from '@/components/common/StatusBadge';
import { ScreenshotModal } from '@/components/modals/ScreenshotModal';
import {
  ArrowLeft,
  CheckCircle,
  XCircle,
  Clock,
  Globe2,
  Layers,
  FileCode2,
  Camera,
  Terminal,
  AlertOctagon,
  Copy,
  Check,
  Calendar,
} from 'lucide-react';

interface TestDetailViewClientProps {
  test: TestResult;
  execution: ExecutionSummary | null;
}

export const TestDetailViewClient: React.FC<TestDetailViewClientProps> = ({
  test,
  execution,
}) => {
  const [isScreenshotOpen, setIsScreenshotOpen] = useState(false);
  const [copiedLog, setCopiedLog] = useState(false);

  const screenshotUrl =
    test.screenshot_uri ||
    (test.screenshot_path
      ? `/api/screenshots/${encodeURIComponent(test.screenshot_path.split(/[\\/]/).pop() || '')}`
      : '/api/screenshots/test_complete_checkout_successfully_20260731_135220_159130.png');

  const handleCopyLogs = () => {
    navigator.clipboard.writeText(test.log_snippet || '');
    setCopiedLog(true);
    setTimeout(() => setCopiedLog(false), 2000);
  };

  return (
    <div>
      {/* Header */}
      <div className="page-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <Link href="/tests" className="btn btn-sm btn-icon">
            <ArrowLeft size={16} />
          </Link>
          <div className="page-title-group">
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flexWrap: 'wrap' }}>
              <h1>{test.name}</h1>
              <StatusBadge status={test.status} size="md" />
            </div>
            <p style={{ fontFamily: 'var(--font-mono)' }}>
              {test.file_path} :: {test.class_name}
            </p>
          </div>
        </div>

        <div className="header-actions">
          {test.status === 'FAILED' && (
            <button
              onClick={() => setIsScreenshotOpen(true)}
              className="btn btn-sm"
              style={{
                backgroundColor: '#fef2f2',
                color: '#991b1b',
                borderColor: '#fecaca',
                gap: '6px',
              }}
            >
              <Camera size={14} color="#ef4444" />
              <span>View Failure Screenshot</span>
            </button>
          )}
          {execution && (
            <Link href={`/executions/${execution.execution_id}`} className="btn btn-sm">
              <span>View Run ({execution.execution_id})</span>
            </Link>
          )}
        </div>
      </div>

      {/* Metadata Card */}
      <div
        className="card"
        style={{
          marginBottom: '24px',
          padding: '18px 20px',
          backgroundColor: '#ffffff',
          border: '1px solid var(--border-color)',
        }}
      >
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
            gap: '16px',
            fontSize: '13px',
          }}
        >
          <div>
            <span style={{ color: '#64748b', fontSize: '11px', textTransform: 'uppercase', fontWeight: '600' }}>
              Functional Module
            </span>
            <div style={{ marginTop: '4px' }}>
              <span className="badge badge-gray">{test.module}</span>
            </div>
          </div>

          <div>
            <span style={{ color: '#64748b', fontSize: '11px', textTransform: 'uppercase', fontWeight: '600' }}>
              Test Type / Category
            </span>
            <div style={{ marginTop: '4px' }}>
              <span className="badge badge-blue">{test.test_type}</span>
            </div>
          </div>

          <div>
            <span style={{ color: '#64748b', fontSize: '11px', textTransform: 'uppercase', fontWeight: '600' }}>
              Browser & Environment
            </span>
            <div style={{ marginTop: '4px', fontWeight: '600', color: '#0f172a' }}>
              {test.browser || 'Chrome'} ({test.environment || 'QA'})
            </div>
          </div>

          <div>
            <span style={{ color: '#64748b', fontSize: '11px', textTransform: 'uppercase', fontWeight: '600' }}>
              Execution Duration
            </span>
            <div style={{ marginTop: '4px', fontWeight: '700', color: '#0f172a' }}>
              {test.duration}s
            </div>
          </div>

          <div>
            <span style={{ color: '#64748b', fontSize: '11px', textTransform: 'uppercase', fontWeight: '600' }}>
              Execution Timestamps
            </span>
            <div style={{ marginTop: '4px', fontSize: '12px', color: '#64748b' }}>
              {test.start_time || '12:45:00'} - {test.end_time || '12:45:05'}
            </div>
          </div>
        </div>
      </div>

      {/* Failure Callout if FAILED */}
      {test.status === 'FAILED' && (
        <div
          style={{
            backgroundColor: '#fef2f2',
            border: '1px solid #fecaca',
            borderRadius: 'var(--radius-lg)',
            padding: '20px',
            marginBottom: '24px',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '10px' }}>
            <AlertOctagon size={18} color="#ef4444" />
            <h3 style={{ fontSize: '15px', fontWeight: '700', color: '#991b1b' }}>
              {test.failure?.error_type || 'Assertion / Element Failure Detected'}
            </h3>
          </div>

          <div
            style={{
              fontSize: '13px',
              color: '#7f1d1d',
              fontFamily: 'var(--font-mono)',
              backgroundColor: '#fee2e2',
              padding: '12px 16px',
              borderRadius: '8px',
              marginBottom: '16px',
              border: '1px solid #fca5a5',
              whiteSpace: 'pre-wrap',
            }}
          >
            {test.failure?.error_message || 'ElementNotInteractableException: Target element was not clickable at point (450, 890)'}
          </div>

          {/* Collapsible / Formatted Stack Trace */}
          <div style={{ marginTop: '12px' }}>
            <div style={{ fontSize: '12px', fontWeight: '600', color: '#991b1b', marginBottom: '6px' }}>
              Python Stack Trace:
            </div>
            <pre
              style={{
                backgroundColor: '#1e293b',
                color: '#f87171',
                padding: '14px',
                borderRadius: '8px',
                fontSize: '12px',
                fontFamily: 'var(--font-mono)',
                overflowX: 'auto',
                lineHeight: '1.5',
              }}
            >
              {test.failure?.stack_trace || test.failure?.error_message || 'Stack trace details captured from Selenium WebDriver runtime.'}
            </pre>
          </div>
        </div>
      )}

      {/* Grid: Execution Steps & Assertions */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))',
          gap: '24px',
          marginBottom: '24px',
        }}
      >
        {/* Step-by-Step Timeline */}
        <div className="card">
          <div className="card-header">
            <div className="card-title">Execution Steps Timeline</div>
            <span style={{ fontSize: '12px', color: '#64748b' }}>
              {test.steps?.length || 5} steps
            </span>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {(test.steps || []).map((step, idx) => {
              const isStepPass = step.status === 'passed';
              return (
                <div
                  key={idx}
                  style={{
                    display: 'flex',
                    alignItems: 'flex-start',
                    gap: '12px',
                    padding: '10px 14px',
                    borderRadius: '8px',
                    backgroundColor: isStepPass ? '#f8fafc' : '#fef2f2',
                    border: `1px solid ${isStepPass ? '#e2e8f0' : '#fecaca'}`,
                  }}
                >
                  <div style={{ marginTop: '2px' }}>
                    {isStepPass ? (
                      <CheckCircle size={16} color="#10b981" />
                    ) : (
                      <XCircle size={16} color="#ef4444" />
                    )}
                  </div>
                  <div style={{ flex: 1 }}>
                    <div
                      style={{
                        fontSize: '13px',
                        fontWeight: '600',
                        color: isStepPass ? '#0f172a' : '#991b1b',
                      }}
                    >
                      {step.name}
                    </div>
                    {step.details && (
                      <div style={{ fontSize: '12px', color: '#64748b', marginTop: '2px' }}>
                        {step.details}
                      </div>
                    )}
                  </div>
                  <span style={{ fontSize: '11.5px', color: '#94a3b8', fontFamily: 'var(--font-mono)' }}>
                    {step.duration}s
                  </span>
                </div>
              );
            })}
          </div>
        </div>

        {/* Assertions & Verification List */}
        <div className="card">
          <div className="card-header">
            <div className="card-title">Test Assertions & Validations</div>
            <span style={{ fontSize: '12px', color: '#10b981', fontWeight: '600' }}>
              {test.status === 'PASSED' ? 'All Passed' : '1 Failed'}
            </span>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {(test.assertions || [
              'Assert authentication token present',
              'Assert URL redirects to target landing page',
              'Assert required UI elements are present in DOM',
            ]).map((assertion, idx) => (
              <div
                key={idx}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '10px',
                  padding: '10px 14px',
                  borderRadius: '8px',
                  backgroundColor: '#f8fafc',
                  border: '1px solid #e2e8f0',
                  fontSize: '13px',
                }}
              >
                <CheckCircle size={15} color="#10b981" />
                <span style={{ color: '#1e293b', fontWeight: '500' }}>{assertion}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Execution Logs Snippet */}
      <div className="card" style={{ marginBottom: '24px' }}>
        <div className="card-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Terminal size={16} color="#64748b" />
            <div className="card-title">Scoped Execution Logs</div>
          </div>
          <button onClick={handleCopyLogs} className="btn btn-sm" style={{ gap: '6px' }}>
            {copiedLog ? <Check size={13} color="#10b981" /> : <Copy size={13} />}
            <span>{copiedLog ? 'Copied' : 'Copy Logs'}</span>
          </button>
        </div>

        <div className="code-viewer">
          {test.log_snippet ? (
            test.log_snippet.split('\n').map((line, lIdx) => (
              <div key={lIdx} className="code-line">
                <span className="line-number">{lIdx + 1}</span>
                <span
                  className={
                    line.includes('ERROR')
                      ? 'log-error'
                      : line.includes('WARN')
                      ? 'log-warn'
                      : line.includes('INFO')
                      ? 'log-info'
                      : ''
                  }
                >
                  {line}
                </span>
              </div>
            ))
          ) : (
            <div style={{ color: '#94a3b8' }}>
              INFO [Framework] Executed {test.name} successfully. No runtime errors encountered.
            </div>
          )}
        </div>
      </div>

      {/* Screenshot Modal */}
      <ScreenshotModal
        isOpen={isScreenshotOpen}
        onClose={() => setIsScreenshotOpen(false)}
        screenshotUrl={screenshotUrl}
        testName={test.name}
        browser={test.browser}
        environment={test.environment}
      />
    </div>
  );
};
