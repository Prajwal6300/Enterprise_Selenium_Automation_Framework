import { NextResponse } from 'next/server';
import { getLiveExecutionStatus } from '@/lib/result-parser';

export async function GET() {
  try {
    const liveStatus = getLiveExecutionStatus();
    return NextResponse.json(liveStatus, { status: 200 });
  } catch (err: any) {
    return NextResponse.json(
      {
        is_active: false,
        status: 'IDLE',
        message: 'Live execution service unavailable',
      },
      { status: 200 }
    );
  }
}
