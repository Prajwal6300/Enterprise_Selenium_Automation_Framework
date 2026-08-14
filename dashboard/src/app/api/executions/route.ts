import { NextRequest, NextResponse } from 'next/server';
import { getAllExecutions, getExecutionIndex } from '@/lib/result-parser';
import { saveExecutionToDb } from '@/lib/db';
import { ExecutionSummary } from '@/lib/types';

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const search = searchParams.get('search')?.toLowerCase() || '';
    const env = searchParams.get('env')?.toUpperCase() || 'ALL';
    const browser = searchParams.get('browser')?.toLowerCase() || 'all';
    const status = searchParams.get('status')?.toUpperCase() || 'ALL';
    const page = parseInt(searchParams.get('page') || '1', 10);
    const limit = parseInt(searchParams.get('limit') || '10', 10);

    let executions = getExecutionIndex();

    // Filters
    if (search) {
      executions = executions.filter(
        (e) =>
          e.execution_id.toLowerCase().includes(search) ||
          e.branch.toLowerCase().includes(search) ||
          e.commit_hash.toLowerCase().includes(search) ||
          e.ci_system.toLowerCase().includes(search)
      );
    }

    if (env !== 'ALL') {
      executions = executions.filter((e) => e.environment.toUpperCase() === env);
    }

    if (browser !== 'all') {
      executions = executions.filter((e) => e.browser.toLowerCase() === browser);
    }

    if (status !== 'ALL') {
      executions = executions.filter((e) => e.status.toUpperCase() === status);
    }

    const total = executions.length;
    const totalPages = Math.ceil(total / limit) || 1;
    const paginated = executions.slice((page - 1) * limit, page * limit);

    return NextResponse.json({
      data: paginated,
      pagination: {
        page,
        limit,
        total,
        totalPages,
      },
    });
  } catch (err: any) {
    return NextResponse.json(
      { error: 'Failed to fetch executions', details: err?.message },
      { status: 500 }
    );
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = (await request.json()) as ExecutionSummary;

    if (!body.execution_id || !body.tests) {
      return NextResponse.json(
        { error: 'Invalid execution payload: execution_id and tests required' },
        { status: 400 }
      );
    }

    // Persist to DB if PostgreSQL is active
    await saveExecutionToDb(body);

    return NextResponse.json({
      success: true,
      message: `Execution ${body.execution_id} ingested successfully`,
      execution_id: body.execution_id,
    });
  } catch (err: any) {
    return NextResponse.json(
      { error: 'Failed to ingest execution', details: err?.message },
      { status: 500 }
    );
  }
}
