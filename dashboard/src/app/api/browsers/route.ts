import { NextResponse } from 'next/server';
import { getBrowserAnalytics } from '@/lib/result-parser';

export async function GET() {
  try {
    const browsers = getBrowserAnalytics();
    return NextResponse.json({ data: browsers });
  } catch (err: any) {
    return NextResponse.json({ error: 'Failed to fetch browser metrics', details: err?.message }, { status: 500 });
  }
}
