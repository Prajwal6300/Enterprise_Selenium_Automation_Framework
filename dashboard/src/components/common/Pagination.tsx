'use client';

import React from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';

interface PaginationProps {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
  totalItems?: number;
  pageSize?: number;
}

export const Pagination: React.FC<PaginationProps> = ({
  currentPage,
  totalPages,
  onPageChange,
  totalItems,
  pageSize = 10,
}) => {
  if (totalPages <= 1) return null;

  const startIdx = (currentPage - 1) * pageSize + 1;
  const endIdx = Math.min(currentPage * pageSize, totalItems || currentPage * pageSize);

  return (
    <div
      style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '12px 16px',
        borderTop: '1px solid var(--border-color)',
        fontSize: '13px',
        color: 'var(--text-secondary)',
      }}
    >
      <div>
        {totalItems ? (
          <span>
            Showing <strong style={{ color: 'var(--text-primary)' }}>{startIdx}</strong> to{' '}
            <strong style={{ color: 'var(--text-primary)' }}>{endIdx}</strong> of{' '}
            <strong style={{ color: 'var(--text-primary)' }}>{totalItems}</strong> entries
          </span>
        ) : (
          <span>
            Page <strong style={{ color: 'var(--text-primary)' }}>{currentPage}</strong> of{' '}
            <strong style={{ color: 'var(--text-primary)' }}>{totalPages}</strong>
          </span>
        )}
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
        <button
          className="btn btn-sm btn-icon"
          disabled={currentPage <= 1}
          onClick={() => onPageChange(currentPage - 1)}
          style={{ opacity: currentPage <= 1 ? 0.5 : 1 }}
        >
          <ChevronLeft size={14} />
        </button>

        {Array.from({ length: totalPages }, (_, i) => i + 1).map((p) => {
          // Display current, first, last and nearby
          if (p === 1 || p === totalPages || (p >= currentPage - 1 && p <= currentPage + 1)) {
            const isCurrent = p === currentPage;
            return (
              <button
                key={p}
                onClick={() => onPageChange(p)}
                className={`btn btn-sm ${isCurrent ? 'btn-primary' : ''}`}
                style={{
                  minWidth: '28px',
                  height: '28px',
                  padding: '0 6px',
                  fontWeight: isCurrent ? '700' : '500',
                }}
              >
                {p}
              </button>
            );
          }
          if (p === currentPage - 2 || p === currentPage + 2) {
            return <span key={p} style={{ padding: '0 4px', color: '#94a3b8' }}>...</span>;
          }
          return null;
        })}

        <button
          className="btn btn-sm btn-icon"
          disabled={currentPage >= totalPages}
          onClick={() => onPageChange(currentPage + 1)}
          style={{ opacity: currentPage >= totalPages ? 0.5 : 1 }}
        >
          <ChevronRight size={14} />
        </button>
      </div>
    </div>
  );
};
