import { NextRequest, NextResponse } from 'next/server';
import { getAllTestCases } from '@/lib/result-parser';

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const search = searchParams.get('search')?.toLowerCase() || '';
    const module = searchParams.get('module') || 'ALL';
    const testType = searchParams.get('type') || 'ALL';
    const status = searchParams.get('status')?.toUpperCase() || 'ALL';
    const browser = searchParams.get('browser')?.toLowerCase() || 'all';

    let tests = getAllTestCases();

    if (search) {
      tests = tests.filter(
        (t) =>
          t.name.toLowerCase().includes(search) ||
          t.class_name.toLowerCase().includes(search) ||
          t.file_path.toLowerCase().includes(search) ||
          t.module.toLowerCase().includes(search)
      );
    }

    if (module !== 'ALL') {
      tests = tests.filter((t) => t.module.toLowerCase() === module.toLowerCase());
    }

    if (testType !== 'ALL') {
      tests = tests.filter((t) => t.test_type.toLowerCase() === testType.toLowerCase());
    }

    if (status !== 'ALL') {
      tests = tests.filter((t) => t.status.toUpperCase() === status);
    }

    if (browser !== 'all') {
      tests = tests.filter((t) => t.browser?.toLowerCase() === browser);
    }

    return NextResponse.json({
      data: tests,
      total: tests.length,
    });
  } catch (err: any) {
    return NextResponse.json(
      { error: 'Failed to fetch test cases', details: err?.message },
      { status: 500 }
    );
  }
}
