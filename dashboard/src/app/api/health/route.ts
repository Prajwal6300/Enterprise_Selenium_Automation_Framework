import { NextResponse } from 'next/server';
import { getSystemHealth } from '@/lib/result-parser';

export async function GET() {
  try {
    const health = getSystemHealth();
    return NextResponse.json(health, { status: 200 });
  } catch (err: any) {
    return NextResponse.json(
      {
        status: 'UNHEALTHY',
        error: err?.message || 'Health check failed',
        timestamp: new Date().toISOString(),
      },
      { status: 500 }
    );
  }
}
