'use client';

import React, { useState, useEffect, useMemo } from 'react';
import Link from 'next/link';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { StatusBadge } from '@/components/common/StatusBadge';
import { SearchBar } from '@/components/common/SearchBar';
import { FilterBar } from '@/components/common/FilterBar';
import { Pagination } from '@/components/common/Pagination';
import { EmptyState, LoadingState } from '@/components/common/FeedbackStates';
import { ExecutionIndexItem } from '@/lib/types';
import { PlaySquare, Download, RefreshCw, ArrowUpDown } from 'lucide-react';

export default function ExecutionsPage() {
  const [executions, setExecutions] = useState<ExecutionIndexItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [envFilter, setEnvFilter] = useState('ALL');
  const [browserFilter, setBrowserFilter] = useState('ALL');
  const [statusFilter, setStatusFilter] = useState('ALL');
  const [currentPage, setCurrentPage] = useState(1);
  const [sortField, setSortField] = useState<keyof ExecutionIndexItem>('timestamp');
  const [sortAsc, setSortAsc] = useState(false);
  const pageSize = 10;

  const fetchExecutions = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/executions?limit=100');
      const json = await res.json();
      if (json.data) {
        setExecutions(json.data);
      }
    } catch (err) {
      console.error('Failed to load executions:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchExecutions();
  }, []);

  const handleSort = (field: keyof ExecutionIndexItem) => {
    if (sortField === field) {
      setSortAsc(!sortAsc);
    } else {
      setSortField(field);
      setSortAsc(false);
    }
  };

  const filtered = useMemo(() => {
    return executions.filter((exec) => {
      const matchSearch =
        !search ||
        exec.execution_id.toLowerCase().includes(search.toLowerCase()) ||
        exec.branch.toLowerCase().includes(search.toLowerCase()) ||
        exec.commit_hash.toLowerCase().includes(search.toLowerCase()) ||
        exec.ci_system.toLowerCase().includes(search.toLowerCase());

      const matchEnv = envFilter === 'ALL' || exec.environment.toUpperCase() === envFilter.toUpperCase();
      const matchBrowser =
        browserFilter === 'ALL' || exec.browser.toLowerCase() === browserFilter.toLowerCase();
      const matchStatus = statusFilter === 'ALL' || exec.status.toUpperCase() === statusFilter.toUpperCase();

      return matchSearch && matchEnv && matchBrowser && matchStatus;
    });
  }, [executions, search, envFilter, browserFilter, statusFilter]);

  const sorted = useMemo(() => {
    return [...filtered].sort((a, b) => {
      const valA = a[sortField];
      const valB = b[sortField];
      if (valA === undefined || valB === undefined) return 0;
      if (typeof valA === 'number' && typeof valB === 'number') {
        return sortAsc ? valA - valB : valB - valA;
      }
      return sortAsc
        ? String(valA).localeCompare(String(valB))
        : String(valB).localeCompare(String(valA));
    });
  }, [filtered, sortField, sortAsc]);

  const totalPages = Math.ceil(sorted.length / pageSize) || 1;
  const paginated = sorted.slice((currentPage - 1) * pageSize, currentPage * pageSize);

  const formatDuration = (s: number) => {
    const mins = Math.floor(s / 60);
    const secs = Math.round(s % 60);
    return `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
  };

  return (
    <DashboardLayout>
      <div className="page-header">
        <div className="page-title-group">
          <h1>Test Executions</h1>
          <p>Complete historical execution ledger across local, Docker, Jenkins, and GitHub Actions runs.</p>
        </div>
        <div className="header-actions">
          <button onClick={fetchExecutions} className="btn btn-sm">
            <RefreshCw size={13} color="#64748b" />
            <span>Refresh</span>
          </button>
          <a href="/api/reports/csv-export" download className="btn btn-sm">
            <Download size={13} color="#64748b" />
            <span>Export CSV</span>
          </a>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div
        className="card"
        style={{
          marginBottom: '16px',
          padding: '14px 20px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexWrap: 'wrap',
          gap: '12px',
        }}
      >
        <SearchBar
          value={search}
          onChange={(v) => {
            setSearch(v);
            setCurrentPage(1);
          }}
          placeholder="Search by ID, branch, commit..."
          width="280px"
        />

        <FilterBar
          filters={[
            {
              id: 'env',
              label: 'Environment',
              value: envFilter,
              onChange: (v) => {
                setEnvFilter(v);
                setCurrentPage(1);
              },
              options: [
                { label: 'QA', value: 'QA' },
                { label: 'UAT', value: 'UAT' },
                { label: 'PROD', value: 'PROD' },
              ],
            },
            {
              id: 'browser',
              label: 'Browser',
              value: browserFilter,
              onChange: (v) => {
                setBrowserFilter(v);
                setCurrentPage(1);
              },
              options: [
                { label: 'Chrome', value: 'chrome' },
                { label: 'Firefox', value: 'firefox' },
                { label: 'Edge', value: 'edge' },
                { label: 'BrowserStack', value: 'browserstack' },
              ],
            },
            {
              id: 'status',
              label: 'Status',
              value: statusFilter,
              onChange: (v) => {
                setStatusFilter(v);
                setCurrentPage(1);
              },
              options: [
                { label: 'PASSED', value: 'PASSED' },
                { label: 'FAILED', value: 'FAILED' },
              ],
            },
          ]}
          onReset={() => {
            setSearch('');
            setEnvFilter('ALL');
            setBrowserFilter('ALL');
            setStatusFilter('ALL');
            setCurrentPage(1);
          }}
        />
      </div>

      {/* Executions Table */}
      {loading ? (
        <LoadingState message="Loading test execution history..." />
      ) : paginated.length === 0 ? (
        <EmptyState
          title="No Executions Found"
          message="No test executions match your selected filters or search terms."
          actionText="Clear Filters"
          onAction={() => {
            setSearch('');
            setEnvFilter('ALL');
            setBrowserFilter('ALL');
            setStatusFilter('ALL');
          }}
        />
      ) : (
        <div className="table-responsive">
          <table className="data-table">
            <thead>
              <tr>
                <th onClick={() => handleSort('execution_id')} style={{ cursor: 'pointer' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                    <span>Execution ID</span>
                    <ArrowUpDown size={12} color="#94a3b8" />
                  </div>
                </th>
                <th>Date & Time</th>
                <th>Branch</th>
                <th>Commit</th>
                <th>Environment</th>
                <th>Browser</th>
                <th>Total</th>
                <th>Passed</th>
                <th>Failed</th>
                <th>Skipped</th>
                <th onClick={() => handleSort('duration')} style={{ cursor: 'pointer' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                    <span>Duration</span>
                    <ArrowUpDown size={12} color="#94a3b8" />
                  </div>
                </th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {paginated.map((exec) => (
                <tr key={exec.execution_id}>
                  <td>
                    <Link
                      href={`/executions/${exec.execution_id}`}
                      style={{ fontWeight: '600', color: 'var(--primary)' }}
                    >
                      {exec.execution_id}
                    </Link>
                  </td>
                  <td>
                    <div style={{ fontWeight: '500' }}>{exec.date}</div>
                    <div style={{ fontSize: '11px', color: '#94a3b8' }}>{exec.time}</div>
                  </td>
                  <td>
                    <span style={{ fontFamily: 'var(--font-mono)', fontSize: '12px' }}>
                      {exec.branch}
                    </span>
                  </td>
                  <td>
                    <span style={{ fontFamily: 'var(--font-mono)', fontSize: '12px', color: '#64748b' }}>
                      {exec.commit_hash.slice(0, 7)}
                    </span>
                  </td>
                  <td>
                    <span className="badge badge-gray">{exec.environment}</span>
                  </td>
                  <td>{exec.browser}</td>
                  <td>{exec.total}</td>
                  <td style={{ color: '#10b981', fontWeight: '600' }}>{exec.passed}</td>
                  <td style={{ color: exec.failed > 0 ? '#ef4444' : '#64748b', fontWeight: '600' }}>
                    {exec.failed}
                  </td>
                  <td style={{ color: '#f59e0b' }}>{exec.skipped}</td>
                  <td>{formatDuration(exec.duration)}</td>
                  <td>
                    <StatusBadge status={exec.status} />
                  </td>
                  <td>
                    <Link
                      href={`/executions/${exec.execution_id}`}
                      className="btn btn-sm btn-primary"
                      style={{ padding: '3px 10px' }}
                    >
                      View
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          <Pagination
            currentPage={currentPage}
            totalPages={totalPages}
            onPageChange={setCurrentPage}
            totalItems={sorted.length}
            pageSize={pageSize}
          />
        </div>
      )}
    </DashboardLayout>
  );
}
