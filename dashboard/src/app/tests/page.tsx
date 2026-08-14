'use client';

import React, { useState, useEffect, useMemo } from 'react';
import Link from 'next/link';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { StatusBadge } from '@/components/common/StatusBadge';
import { SearchBar } from '@/components/common/SearchBar';
import { FilterBar } from '@/components/common/FilterBar';
import { Pagination } from '@/components/common/Pagination';
import { EmptyState, LoadingState } from '@/components/common/FeedbackStates';
import { TestResult } from '@/lib/types';
import { FlaskConical, RefreshCw, Layers, Globe2 } from 'lucide-react';

export default function TestCasesPage() {
  const [tests, setTests] = useState<TestResult[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [moduleFilter, setModuleFilter] = useState('ALL');
  const [typeFilter, setTypeFilter] = useState('ALL');
  const [statusFilter, setStatusFilter] = useState('ALL');
  const [browserFilter, setBrowserFilter] = useState('ALL');
  const [currentPage, setCurrentPage] = useState(1);
  const pageSize = 12;

  const fetchTests = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/tests');
      const json = await res.json();
      if (json.data) {
        setTests(json.data);
      }
    } catch (err) {
      console.error('Failed to load test cases:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTests();
  }, []);

  const filtered = useMemo(() => {
    return tests.filter((t) => {
      const matchSearch =
        !search ||
        t.name.toLowerCase().includes(search.toLowerCase()) ||
        t.class_name.toLowerCase().includes(search.toLowerCase()) ||
        t.module.toLowerCase().includes(search.toLowerCase()) ||
        t.file_path.toLowerCase().includes(search.toLowerCase());

      const matchModule = moduleFilter === 'ALL' || t.module.toLowerCase() === moduleFilter.toLowerCase();
      const matchType = typeFilter === 'ALL' || t.test_type.toLowerCase() === typeFilter.toLowerCase();
      const matchStatus = statusFilter === 'ALL' || t.status.toUpperCase() === statusFilter.toUpperCase();
      const matchBrowser = browserFilter === 'ALL' || t.browser.toLowerCase() === browserFilter.toLowerCase();

      return matchSearch && matchModule && matchType && matchStatus && matchBrowser;
    });
  }, [tests, search, moduleFilter, typeFilter, statusFilter, browserFilter]);

  const totalPages = Math.ceil(filtered.length / pageSize) || 1;
  const paginated = filtered.slice((currentPage - 1) * pageSize, currentPage * pageSize);

  return (
    <DashboardLayout>
      <div className="page-header">
        <div className="page-title-group">
          <h1>Test Cases Catalog</h1>
          <p>
            Catalog of all {tests.length} automated test cases across UI, REST API, and Database validation suites.
          </p>
        </div>
        <div className="header-actions">
          <button onClick={fetchTests} className="btn btn-sm">
            <RefreshCw size={13} color="#64748b" />
            <span>Refresh</span>
          </button>
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
          placeholder="Search test name, module..."
          width="260px"
        />

        <FilterBar
          filters={[
            {
              id: 'module',
              label: 'Module',
              value: moduleFilter,
              onChange: (v) => {
                setModuleFilter(v);
                setCurrentPage(1);
              },
              options: [
                { label: 'Login', value: 'Login' },
                { label: 'Cart', value: 'Cart' },
                { label: 'Checkout', value: 'Checkout' },
                { label: 'Search', value: 'Search' },
                { label: 'Logout', value: 'Logout' },
                { label: 'API', value: 'API' },
                { label: 'Database', value: 'Database' },
              ],
            },
            {
              id: 'type',
              label: 'Type',
              value: typeFilter,
              onChange: (v) => {
                setTypeFilter(v);
                setCurrentPage(1);
              },
              options: [
                { label: 'UI', value: 'UI' },
                { label: 'API', value: 'API' },
                { label: 'Database', value: 'Database' },
                { label: 'E2E', value: 'E2E' },
                { label: 'Smoke', value: 'Smoke' },
                { label: 'Regression', value: 'Regression' },
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
          ]}
          onReset={() => {
            setSearch('');
            setModuleFilter('ALL');
            setTypeFilter('ALL');
            setStatusFilter('ALL');
            setBrowserFilter('ALL');
            setCurrentPage(1);
          }}
        />
      </div>

      {/* Tests Table */}
      {loading ? (
        <LoadingState message="Loading test cases catalog..." />
      ) : paginated.length === 0 ? (
        <EmptyState
          title="No Test Cases Found"
          message="No tests match your filter parameters."
          actionText="Reset Filters"
          onAction={() => {
            setSearch('');
            setModuleFilter('ALL');
            setTypeFilter('ALL');
            setStatusFilter('ALL');
            setBrowserFilter('ALL');
          }}
        />
      ) : (
        <div className="table-responsive">
          <table className="data-table">
            <thead>
              <tr>
                <th>Status</th>
                <th>Test Name</th>
                <th>Module</th>
                <th>Type</th>
                <th>Browser</th>
                <th>Environment</th>
                <th>Duration</th>
                <th>Last Run</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {paginated.map((test) => (
                <tr key={test.test_id || test.name}>
                  <td>
                    <StatusBadge status={test.status} />
                  </td>
                  <td>
                    <Link
                      href={`/tests/${test.name}`}
                      style={{ fontWeight: '600', color: 'var(--primary)' }}
                    >
                      {test.name}
                    </Link>
                    <div style={{ fontSize: '11px', color: '#94a3b8', fontFamily: 'var(--font-mono)' }}>
                      {test.file_path}
                    </div>
                  </td>
                  <td>
                    <span className="badge badge-gray">{test.module}</span>
                  </td>
                  <td>
                    <span className="badge badge-blue">{test.test_type}</span>
                  </td>
                  <td>{test.browser || 'Chrome'}</td>
                  <td>
                    <span className="badge badge-gray">{test.environment || 'QA'}</span>
                  </td>
                  <td>{test.duration}s</td>
                  <td>
                    <span style={{ fontSize: '12px', color: '#64748b' }}>
                      {test.end_time || '12:45'}
                    </span>
                  </td>
                  <td>
                    <Link
                      href={`/tests/${test.name}`}
                      className="btn btn-sm btn-primary"
                      style={{ padding: '3px 9px' }}
                    >
                      Inspect
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
            totalItems={filtered.length}
            pageSize={pageSize}
          />
        </div>
      )}
    </DashboardLayout>
  );
}
