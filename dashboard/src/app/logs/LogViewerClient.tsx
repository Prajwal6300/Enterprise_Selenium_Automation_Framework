'use client';

import React, { useState, useMemo } from 'react';
import { SearchBar } from '@/components/common/SearchBar';
import { Terminal, Download, Copy, Check, Filter, ShieldCheck, RefreshCw } from 'lucide-react';

interface LogViewerClientProps {
  initialLines: string[];
  totalLines: number;
}

export const LogViewerClient: React.FC<LogViewerClientProps> = ({
  initialLines,
  totalLines,
}) => {
  const [lines, setLines] = useState<string[]>(initialLines);
  const [search, setSearch] = useState('');
  const [selectedLevel, setSelectedLevel] = useState('ALL');
  const [copied, setCopied] = useState(false);
  const [isRefreshing, setIsRefreshing] = useState(false);

  const fetchLogs = async () => {
    setIsRefreshing(true);
    try {
      const res = await fetch(`/api/logs?level=${selectedLevel}&search=${encodeURIComponent(search)}`);
      const json = await res.json();
      if (json.data) {
        setLines(json.data);
      }
    } catch (err) {
      console.error('Failed to refresh logs:', err);
    } finally {
      setIsRefreshing(false);
    }
  };

  const filteredLines = useMemo(() => {
    return lines.filter((l) => {
      const matchSearch = !search || l.toLowerCase().includes(search.toLowerCase());
      const matchLevel = selectedLevel === 'ALL' || l.toUpperCase().includes(selectedLevel.toUpperCase());
      return matchSearch && matchLevel;
    });
  }, [lines, search, selectedLevel]);

  const handleCopy = () => {
    navigator.clipboard.writeText(filteredLines.join('\n'));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="card" style={{ padding: '0', overflow: 'hidden' }}>
      {/* Control Toolbar */}
      <div
        style={{
          padding: '14px 20px',
          borderBottom: '1px solid var(--border-color)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexWrap: 'wrap',
          gap: '12px',
          backgroundColor: '#f8fafc',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flexWrap: 'wrap' }}>
          <SearchBar
            value={search}
            onChange={setSearch}
            placeholder="Search log messages..."
            width="280px"
          />

          <select
            className="select-filter"
            value={selectedLevel}
            onChange={(e) => setSelectedLevel(e.target.value)}
          >
            <option value="ALL">Level: All Levels</option>
            <option value="INFO">INFO</option>
            <option value="WARN">WARNING</option>
            <option value="ERROR">ERROR</option>
            <option value="DEBUG">DEBUG</option>
          </select>

          <button onClick={fetchLogs} className="btn btn-sm btn-icon" title="Reload logs">
            <RefreshCw size={13} className={isRefreshing ? 'spin-animation' : ''} color="#64748b" />
          </button>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <span
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '5px',
              fontSize: '12px',
              color: '#10b981',
              fontWeight: '600',
              marginRight: '8px',
            }}
          >
            <ShieldCheck size={14} />
            <span>Credentials Redacted</span>
          </span>

          <button onClick={handleCopy} className="btn btn-sm" style={{ gap: '6px' }}>
            {copied ? <Check size={13} color="#10b981" /> : <Copy size={13} />}
            <span>{copied ? 'Copied' : 'Copy'}</span>
          </button>

          <a href="/api/logs?download=true" download className="btn btn-sm" style={{ gap: '6px' }}>
            <Download size={13} />
            <span>Download</span>
          </a>
        </div>
      </div>

      {/* Code Viewer */}
      <div
        className="code-viewer"
        style={{
          maxHeight: '650px',
          minHeight: '400px',
          borderRadius: 0,
          border: 'none',
        }}
      >
        {filteredLines.length === 0 ? (
          <div style={{ color: '#64748b', padding: '20px', textAlign: 'center' }}>
            No log entries match your filter.
          </div>
        ) : (
          filteredLines.map((line, idx) => {
            const isError = line.includes('ERROR');
            const isWarn = line.includes('WARN');
            const isInfo = line.includes('INFO');
            const isPass = line.includes('passed') || line.includes('PASSED');

            return (
              <div key={idx} className="code-line">
                <span className="line-number">{idx + 1}</span>
                <span
                  className={
                    isError
                      ? 'log-error'
                      : isWarn
                      ? 'log-warn'
                      : isPass
                      ? 'log-pass'
                      : isInfo
                      ? 'log-info'
                      : ''
                  }
                >
                  {line}
                </span>
              </div>
            );
          })
        )}
      </div>

      {/* Footer Info */}
      <div
        style={{
          padding: '10px 20px',
          backgroundColor: '#f8fafc',
          borderTop: '1px solid var(--border-color)',
          fontSize: '12px',
          color: '#64748b',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
        }}
      >
        <span>
          Showing {filteredLines.length} of {totalLines} log entries
        </span>
        <span>Storage: logs/framework.log</span>
      </div>
    </div>
  );
};
