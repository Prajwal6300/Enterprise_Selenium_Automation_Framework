import { NextResponse } from 'next/server';
import { getFailureAnalysis } from '@/lib/result-parser';

export async function GET() {
  try {
    const failures = getFailureAnalysis();
    return NextResponse.json({
      data: failures,
      total_failures: failures.reduce((acc, f) => acc + f.failure_count, 0),
      unique_failed_tests: failures.length,
    });
  } catch (err: any) {
    return NextResponse.json(
      { error: 'Failed to aggregate failures', details: err?.message },
      { status: 500 }
    );
  }
}
