import { NextResponse } from 'next/server';
import { getEnvironmentAnalytics } from '@/lib/result-parser';

export async function GET() {
  try {
    const envs = getEnvironmentAnalytics();
    return NextResponse.json({ data: envs });
  } catch (err: any) {
    return NextResponse.json({ error: 'Failed to fetch environment metrics', details: err?.message }, { status: 500 });
  }
}
