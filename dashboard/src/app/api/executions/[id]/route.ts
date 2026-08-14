import { NextRequest, NextResponse } from 'next/server';
import { getExecutionById } from '@/lib/result-parser';

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params;
    const execution = getExecutionById(id);

    if (!execution) {
      return NextResponse.json({ error: `Execution ${id} not found` }, { status: 404 });
    }

    return NextResponse.json(execution, { status: 200 });
  } catch (err: any) {
    return NextResponse.json(
      { error: 'Failed to retrieve execution', details: err?.message },
      { status: 500 }
    );
  }
}
