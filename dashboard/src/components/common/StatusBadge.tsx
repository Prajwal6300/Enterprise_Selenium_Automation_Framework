'use client';

import React from 'react';
import { CheckCircle2, XCircle, AlertCircle, Clock, Check } from 'lucide-react';
import { TestStatus } from '@/lib/types';

interface StatusBadgeProps {
  status: TestStatus | string;
  size?: 'sm' | 'md';
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status, size = 'sm' }) => {
  const norm = (status || 'PASSED').toUpperCase();

  const getStyle = () => {
    switch (norm) {
      case 'PASSED':
      case 'PASS':
        return {
          className: 'badge badge-passed',
          icon: <Check size={size === 'sm' ? 12 : 14} />,
          text: 'PASSED',
        };
      case 'FAILED':
      case 'FAIL':
        return {
          className: 'badge badge-failed',
          icon: <XCircle size={size === 'sm' ? 12 : 14} />,
          text: 'FAILED',
        };
      case 'SKIPPED':
      case 'SKIP':
        return {
          className: 'badge badge-skipped',
          icon: <AlertCircle size={size === 'sm' ? 12 : 14} />,
          text: 'SKIPPED',
        };
      case 'RUNNING':
        return {
          className: 'badge badge-running',
          icon: <Clock size={size === 'sm' ? 12 : 14} />,
          text: 'RUNNING',
        };
      default:
        return {
          className: 'badge badge-gray',
          icon: null,
          text: norm,
        };
    }
  };

  const config = getStyle();

  return (
    <span
      className={config.className}
      style={{
        fontSize: size === 'sm' ? '11px' : '12.5px',
        padding: size === 'sm' ? '2px 8px' : '4px 10px',
      }}
    >
      {config.icon}
      <span>{config.text}</span>
    </span>
  );
};
