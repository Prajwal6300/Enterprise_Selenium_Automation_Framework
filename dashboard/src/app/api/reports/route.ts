import { NextResponse } from 'next/server';
import { getAvailableReports } from '@/lib/result-parser';

export async function GET() {
  try {
    const reports = getAvailableReports();
    return NextResponse.json({
      data: reports,
      total: reports.length,
    });
  } catch (err: any) {
    return NextResponse.json(
      { error: 'Failed to retrieve reports list', details: err?.message },
      { status: 500 }
    );
  }
}
