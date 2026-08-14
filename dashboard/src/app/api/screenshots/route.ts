import { NextResponse } from 'next/server';
import { getFailureScreenshots } from '@/lib/result-parser';

export async function GET() {
  try {
    const screenshots = getFailureScreenshots();
    return NextResponse.json({
      data: screenshots,
      total: screenshots.length,
    });
  } catch (err: any) {
    return NextResponse.json(
      { error: 'Failed to list failure screenshots', details: err?.message },
      { status: 500 }
    );
  }
}
