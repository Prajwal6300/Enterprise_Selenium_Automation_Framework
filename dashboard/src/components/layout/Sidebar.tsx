'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  LayoutDashboard,
  FlaskConical,
  PlaySquare,
  AlertOctagon,
  TrendingUp,
  Globe2,
  Layers,
  FileText,
  Camera,
  Terminal,
  GitBranch,
  Activity,
  Settings,
  ShieldCheck,
  ChevronRight,
} from 'lucide-react';

interface SidebarProps {
  collapsed?: boolean;
  onToggleCollapse?: () => void;
}

export const Sidebar: React.FC<SidebarProps> = () => {
  const pathname = usePathname();

  const navSections = [
    {
      title: 'OVERVIEW',
      items: [
        { href: '/', label: 'Dashboard', icon: LayoutDashboard },
      ],
    },
    {
      title: 'TEST MANAGEMENT',
      items: [
        { href: '/tests', label: 'Test Cases', icon: FlaskConical },
        { href: '/executions', label: 'Test Executions', icon: PlaySquare },
        { href: '/failures', label: 'Failures Analysis', icon: AlertOctagon },
      ],
    },
    {
      title: 'ANALYTICS',
      items: [
        { href: '/analytics/trends', label: 'Test Trends', icon: TrendingUp },
        { href: '/analytics/browsers', label: 'Browser Analytics', icon: Globe2 },
        { href: '/analytics/environments', label: 'Environment Analytics', icon: Layers },
      ],
    },
    {
      title: 'REPORTS & ASSETS',
      items: [
        { href: '/reports', label: 'Reports Hub', icon: FileText },
        { href: '/screenshots', label: 'Screenshots', icon: Camera },
        { href: '/logs', label: 'Execution Logs', icon: Terminal },
      ],
    },
    {
      title: 'CI / CD PIPELINES',
      items: [
        { href: '/cicd', label: 'CI/CD Pipelines', icon: GitBranch },
      ],
    },
    {
      title: 'SYSTEM',
      items: [
        { href: '/health', label: 'System Health', icon: Activity },
        { href: '/settings', label: 'Settings', icon: Settings },
      ],
    },
  ];

  return (
    <aside style={sidebarStyles.container}>
      {/* Brand Header */}
      <div style={sidebarStyles.brandHeader}>
        <div style={sidebarStyles.logoBadge}>
          <ShieldCheck size={20} color="#ffffff" />
        </div>
        <div style={sidebarStyles.brandText}>
          <div style={sidebarStyles.brandTitle}>Enterprise QA</div>
          <div style={sidebarStyles.brandSub}>Selenium Automation</div>
        </div>
      </div>

      {/* Navigation Sections */}
      <div style={sidebarStyles.navScroll}>
        {navSections.map((section, sIdx) => (
          <div key={sIdx} style={sidebarStyles.sectionBlock}>
            <div style={sidebarStyles.sectionHeader}>{section.title}</div>
            <div style={sidebarStyles.itemList}>
              {section.items.map((item, iIdx) => {
                const isActive =
                  item.href === '/'
                    ? pathname === '/'
                    : pathname === item.href || pathname.startsWith(`${item.href}/`);
                const Icon = item.icon;

                return (
                  <Link
                    key={iIdx}
                    href={item.href}
                    style={{
                      ...sidebarStyles.navItem,
                      ...(isActive ? sidebarStyles.navItemActive : {}),
                    }}
                  >
                    <Icon
                      size={17}
                      style={{
                        color: isActive ? 'var(--primary)' : 'var(--text-secondary)',
                        flexShrink: 0,
                      }}
                    />
                    <span style={sidebarStyles.itemLabel}>{item.label}</span>
                    {isActive && <ChevronRight size={14} style={{ marginLeft: 'auto', color: 'var(--primary)' }} />}
                  </Link>
                );
              })}
            </div>
          </div>
        ))}
      </div>

      {/* Footer / Status */}
      <div style={sidebarStyles.footer}>
        <div style={sidebarStyles.frameworkTag}>
          <span style={sidebarStyles.statusDot} />
          <span>v2.5.0-Enterprise</span>
        </div>
      </div>
    </aside>
  );
};

const sidebarStyles: Record<string, React.CSSProperties> = {
  container: {
    width: 'var(--sidebar-width)',
    height: '100vh',
    position: 'fixed',
    top: 0,
    left: 0,
    backgroundColor: '#ffffff',
    borderRight: '1px solid var(--border-color)',
    display: 'flex',
    flexDirection: 'column',
    zIndex: 40,
  },
  brandHeader: {
    height: 'var(--navbar-height)',
    display: 'flex',
    alignItems: 'center',
    padding: '0 20px',
    borderBottom: '1px solid var(--border-color)',
    gap: '12px',
  },
  logoBadge: {
    width: '34px',
    height: '34px',
    borderRadius: '8px',
    backgroundColor: '#2563eb',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    boxShadow: '0 2px 4px rgba(37, 99, 235, 0.25)',
  },
  brandText: {
    display: 'flex',
    flexDirection: 'column',
  },
  brandTitle: {
    fontSize: '15px',
    fontWeight: '700',
    color: '#0f172a',
    letterSpacing: '-0.01em',
    lineHeight: '1.2',
  },
  brandSub: {
    fontSize: '11px',
    color: '#64748b',
    fontWeight: '500',
  },
  navScroll: {
    flex: 1,
    overflowY: 'auto',
    padding: '16px 12px',
  },
  sectionBlock: {
    marginBottom: '20px',
  },
  sectionHeader: {
    fontSize: '11px',
    fontWeight: '700',
    color: '#94a3b8',
    letterSpacing: '0.05em',
    padding: '0 10px',
    marginBottom: '6px',
  },
  itemList: {
    display: 'flex',
    flexDirection: 'column',
    gap: '2px',
  },
  navItem: {
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    padding: '8px 12px',
    borderRadius: '8px',
    fontSize: '13px',
    fontWeight: '500',
    color: '#475569',
    transition: 'all 0.15s ease',
  },
  navItemActive: {
    backgroundColor: '#eff6ff',
    color: '#1d4ed8',
    fontWeight: '600',
  },
  itemLabel: {
    whiteSpace: 'nowrap',
    overflow: 'hidden',
    textOverflow: 'ellipsis',
  },
  footer: {
    padding: '12px 16px',
    borderTop: '1px solid var(--border-color)',
    backgroundColor: '#f8fafc',
  },
  frameworkTag: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    fontSize: '12px',
    color: '#64748b',
    fontWeight: '500',
  },
  statusDot: {
    width: '7px',
    height: '7px',
    borderRadius: '50%',
    backgroundColor: '#10b981',
  },
};
