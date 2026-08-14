'use client';

import React from 'react';
import { LucideIcon } from 'lucide-react';

interface KpiCardProps {
  title: string;
  value: string | number;
  subtext?: string;
  icon?: LucideIcon;
  variant?: 'default' | 'success' | 'danger' | 'warning' | 'primary';
  trend?: string;
}

export const KpiCard: React.FC<KpiCardProps> = ({
  title,
  value,
  subtext,
  icon: Icon,
  variant = 'default',
}) => {
  const getAccentColor = () => {
    switch (variant) {
      case 'success':
        return '#10b981';
      case 'danger':
        return '#ef4444';
      case 'warning':
        return '#f59e0b';
      case 'primary':
        return '#2563eb';
      default:
        return '#64748b';
    }
  };

  const getBgLight = () => {
    switch (variant) {
      case 'success':
        return '#ecfdf5';
      case 'danger':
        return '#fef2f2';
      case 'warning':
        return '#fffbeb';
      case 'primary':
        return '#eff6ff';
      default:
        return '#f8fafc';
    }
  };

  return (
    <div className="kpi-card">
      <div className="kpi-card-header">
        <span>{title}</span>
        {Icon && (
          <div
            style={{
              width: '32px',
              height: '32px',
              borderRadius: '8px',
              backgroundColor: getBgLight(),
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            <Icon size={16} color={getAccentColor()} />
          </div>
        )}
      </div>
      <div
        className="kpi-value"
        style={{
          color: variant !== 'default' ? getAccentColor() : 'var(--text-primary)',
        }}
      >
        {value}
      </div>
      {subtext && <div className="kpi-subtext">{subtext}</div>}
    </div>
  );
};
