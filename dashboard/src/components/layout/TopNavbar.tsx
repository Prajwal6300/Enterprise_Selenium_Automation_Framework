'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import {
  Search,
  RefreshCw,
  Bell,
  User,
  ShieldCheck,
  Radio,
  ExternalLink,
  LogOut,
} from 'lucide-react';

interface TopNavbarProps {
  environment?: string;
  onRefresh?: () => void;
  isRefreshing?: boolean;
}

export const TopNavbar: React.FC<TopNavbarProps> = ({
  environment = 'QA',
  onRefresh,
  isRefreshing = false,
}) => {
  const [searchOpen, setSearchOpen] = useState(false);
  const [searchVal, setSearchVal] = useState('');

  const handleSearchKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && searchVal.trim()) {
      window.location.href = `/tests?search=${encodeURIComponent(searchVal.trim())}`;
    }
  };

  return (
    <header style={navbarStyles.header}>
      {/* Left side: Environment & Live Status */}
      <div style={navbarStyles.leftGroup}>
        <div style={navbarStyles.envBadge}>
          <span style={navbarStyles.envLabel}>ENV:</span>
          <span style={navbarStyles.envVal}>{environment.toUpperCase()}</span>
        </div>

        <div style={navbarStyles.liveStatusContainer}>
          <span className="live-dot" style={{ backgroundColor: '#10b981' }} />
          <span style={navbarStyles.liveStatusText}>
            QA Platform Online
          </span>
        </div>
      </div>

      {/* Center: Search input */}
      <div style={navbarStyles.centerGroup}>
        <div className="input-search" style={{ width: '320px' }}>
          <Search size={15} color="#94a3b8" />
          <input
            type="text"
            placeholder="Search tests, modules, errors..."
            value={searchVal}
            onChange={(e) => setSearchVal(e.target.value)}
            onKeyDown={handleSearchKeyDown}
          />
        </div>
      </div>

      {/* Right side: Actions & User */}
      <div style={navbarStyles.rightGroup}>
        <button
          onClick={onRefresh || (() => window.location.reload())}
          className="btn btn-icon"
          title="Refresh dashboard data"
          style={{ backgroundColor: '#ffffff' }}
        >
          <RefreshCw size={15} className={isRefreshing ? 'spin-animation' : ''} color="#64748b" />
        </button>

        <Link href="/reports" className="btn btn-sm" style={{ gap: '6px' }}>
          <span>Reports</span>
          <ExternalLink size={13} color="#64748b" />
        </Link>

        {/* User Badge */}
        <div style={navbarStyles.userBadge}>
          <div style={navbarStyles.avatar}>
            <User size={14} color="#2563eb" />
          </div>
          <div style={navbarStyles.userInfo}>
            <span style={navbarStyles.userName}>QA Engineer</span>
            <span style={navbarStyles.userRole}>Lead Tester</span>
          </div>
          <Link href="/login" title="Logout" style={navbarStyles.logoutBtn}>
            <LogOut size={14} color="#94a3b8" />
          </Link>
        </div>
      </div>
    </header>
  );
};

const navbarStyles: Record<string, React.CSSProperties> = {
  header: {
    height: 'var(--navbar-height)',
    backgroundColor: '#ffffff',
    borderBottom: '1px solid var(--border-color)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: '0 28px',
    position: 'sticky',
    top: 0,
    zIndex: 30,
  },
  leftGroup: {
    display: 'flex',
    alignItems: 'center',
    gap: '14px',
  },
  envBadge: {
    display: 'inline-flex',
    alignItems: 'center',
    gap: '5px',
    padding: '4px 10px',
    backgroundColor: '#eff6ff',
    border: '1px solid #bfdbfe',
    borderRadius: '6px',
    fontSize: '12px',
  },
  envLabel: {
    color: '#64748b',
    fontWeight: '500',
  },
  envVal: {
    color: '#1d4ed8',
    fontWeight: '700',
  },
  liveStatusContainer: {
    display: 'flex',
    alignItems: 'center',
    gap: '6px',
    fontSize: '12px',
    color: '#64748b',
    fontWeight: '500',
    backgroundColor: '#f8fafc',
    padding: '4px 10px',
    borderRadius: '6px',
    border: '1px solid #e2e8f0',
  },
  liveStatusText: {
    fontSize: '12px',
  },
  centerGroup: {
    display: 'flex',
    alignItems: 'center',
  },
  rightGroup: {
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
  },
  userBadge: {
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    padding: '4px 8px 4px 6px',
    borderRadius: '8px',
    border: '1px solid #e2e8f0',
    backgroundColor: '#f8fafc',
  },
  avatar: {
    width: '28px',
    height: '28px',
    borderRadius: '50%',
    backgroundColor: '#dbeafe',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  userInfo: {
    display: 'flex',
    flexDirection: 'column',
    lineHeight: '1.2',
  },
  userName: {
    fontSize: '12px',
    fontWeight: '600',
    color: '#0f172a',
  },
  userRole: {
    fontSize: '10.5px',
    color: '#64748b',
  },
  logoutBtn: {
    marginLeft: '4px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    cursor: 'pointer',
  },
};
