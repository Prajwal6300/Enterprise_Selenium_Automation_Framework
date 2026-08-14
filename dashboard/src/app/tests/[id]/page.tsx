import React from 'react';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { StatusBadge } from '@/components/common/StatusBadge';
import { TestDetailViewClient } from './TestDetailViewClient';
import { getTestById } from '@/lib/result-parser';

export const dynamic = 'force-dynamic';
export const revalidate = 0;

export default async function TestDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const data = getTestById(id);

  if (!data) {
    notFound();
  }

  const { test, execution } = data;

  return (
    <DashboardLayout environment={test.environment || execution?.environment || 'QA'}>
      <TestDetailViewClient test={test} execution={execution} />
    </DashboardLayout>
  );
}
