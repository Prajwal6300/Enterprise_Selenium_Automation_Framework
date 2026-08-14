'use client';

import React from 'react';
import { Sidebar } from './Sidebar';
import { TopNavbar } from './TopNavbar';

interface DashboardLayoutProps {
  children: React.ReactNode;
  environment?: string;
}

export const DashboardLayout: React.FC<DashboardLayoutProps> = ({
  children,
  environment = 'QA',
}) => {
  return (
    <div className="app-container">
      <Sidebar />
      <div className="main-content">
        <TopNavbar environment={environment} />
        <main className="page-container">{children}</main>
      </div>
    </div>
  );
};
