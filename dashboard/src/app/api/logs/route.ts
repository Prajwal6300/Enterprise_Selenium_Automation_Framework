import { NextRequest, NextResponse } from 'next/server';
import { getFrameworkLogs } from '@/lib/result-parser';

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const search = searchParams.get('search') || '';
    const level = searchParams.get('level') || 'ALL';
    const isDownload = searchParams.get('download') === 'true';

    const { lines, total } = getFrameworkLogs(search, level);

    if (isDownload) {
      const textContent = lines.join('\n');
      return new NextResponse(textContent, {
        headers: {
          'Content-Type': 'text/plain; charset=utf-8',
          'Content-Disposition': 'attachment; filename="framework_execution.log"',
        },
      });
    }

    return NextResponse.json({
      data: lines,
      total_lines: total,
      returned_lines: lines.length,
    });
  } catch (err: any) {
    return NextResponse.json(
      { error: 'Failed to read logs', details: err?.message },
      { status: 500 }
    );
  }
}
