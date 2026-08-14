import { NextRequest, NextResponse } from 'next/server';
import { getTestById } from '@/lib/result-parser';

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params;
    const testData = getTestById(id);

    if (!testData) {
      return NextResponse.json({ error: `Test case ${id} not found` }, { status: 404 });
    }

    return NextResponse.json(testData, { status: 200 });
  } catch (err: any) {
    return NextResponse.json(
      { error: 'Failed to retrieve test case', details: err?.message },
      { status: 500 }
    );
  }
}
