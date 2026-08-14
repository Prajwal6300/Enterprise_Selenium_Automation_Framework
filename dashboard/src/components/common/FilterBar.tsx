'use client';

import React from 'react';

interface FilterOption {
  label: string;
  value: string;
}

interface FilterBarProps {
  filters: {
    id: string;
    label: string;
    options: FilterOption[];
    value: string;
    onChange: (val: string) => void;
  }[];
  onReset?: () => void;
}

export const FilterBar: React.FC<FilterBarProps> = ({ filters, onReset }) => {
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flexWrap: 'wrap' }}>
      {filters.map((f) => (
        <select
          key={f.id}
          className="select-filter"
          value={f.value}
          onChange={(e) => f.onChange(e.target.value)}
        >
          <option value="ALL">{f.label}: All</option>
          {f.options.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      ))}

      {onReset && (
        <button onClick={onReset} className="btn btn-sm" style={{ color: 'var(--text-secondary)' }}>
          Reset
        </button>
      )}
    </div>
  );
};
