'use client';

import React from 'react';
import { FolderSearch, AlertTriangle, Loader2 } from 'lucide-react';

export const EmptyState: React.FC<{
  title?: string;
  message?: string;
  actionText?: string;
  onAction?: () => void;
}> = ({
  title = 'No records found',
  message = 'Try adjusting your search criteria or filters.',
  actionText,
  onAction,
}) => {
  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '48px 24px',
        textAlign: 'center',
        backgroundColor: '#ffffff',
        borderRadius: '12px',
        border: '1px dashed #cbd5e1',
        margin: '16px 0',
      }}
    >
      <div
        style={{
          width: '48px',
          height: '48px',
          borderRadius: '50%',
          backgroundColor: '#f1f5f9',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          marginBottom: '14px',
        }}
      >
        <FolderSearch size={22} color="#64748b" />
      </div>
      <h3 style={{ fontSize: '15px', fontWeight: '600', color: '#0f172a' }}>{title}</h3>
      <p style={{ fontSize: '13px', color: '#64748b', marginTop: '4px', maxWidth: '360px' }}>
        {message}
      </p>
      {actionText && onAction && (
        <button onClick={onAction} className="btn btn-sm btn-primary" style={{ marginTop: '16px' }}>
          {actionText}
        </button>
      )}
    </div>
  );
};

export const LoadingState: React.FC<{ message?: string }> = ({
  message = 'Loading execution telemetry...',
}) => {
  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '64px 24px',
        gap: '12px',
      }}
    >
      <Loader2 size={26} color="#2563eb" className="spin-animation" />
      <span style={{ fontSize: '13px', color: '#64748b', fontWeight: '500' }}>{message}</span>
    </div>
  );
};

export const ErrorState: React.FC<{
  title?: string;
  message?: string;
  onRetry?: () => void;
}> = ({
  title = 'Service Unavailable',
  message = 'Unable to connect to telemetry provider. Please verify API health.',
  onRetry,
}) => {
  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '48px 24px',
        textAlign: 'center',
        backgroundColor: '#fef2f2',
        borderRadius: '12px',
        border: '1px solid #fecaca',
      }}
    >
      <div
        style={{
          width: '44px',
          height: '44px',
          borderRadius: '50%',
          backgroundColor: '#fee2e2',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          marginBottom: '12px',
        }}
      >
        <AlertTriangle size={22} color="#ef4444" />
      </div>
      <h3 style={{ fontSize: '15px', fontWeight: '600', color: '#991b1b' }}>{title}</h3>
      <p style={{ fontSize: '13px', color: '#b91c1c', marginTop: '4px', maxWidth: '400px' }}>
        {message}
      </p>
      {onRetry && (
        <button onClick={onRetry} className="btn btn-sm" style={{ marginTop: '16px', backgroundColor: '#ffffff' }}>
          Try Again
        </button>
      )}
    </div>
  );
};
