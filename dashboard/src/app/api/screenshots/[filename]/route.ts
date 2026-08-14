import { NextRequest, NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ filename: string }> }
) {
  try {
    const { filename } = await params;
    const cleanName = path.basename(decodeURIComponent(filename));

    const possiblePaths = [
      path.join(process.cwd(), '..', 'screenshots', 'failures', cleanName),
      path.join(process.cwd(), 'screenshots', 'failures', cleanName),
      path.join(process.cwd(), 'public', 'screenshots', cleanName),
    ];

    for (const p of possiblePaths) {
      if (fs.existsSync(p)) {
        const fileBuffer = fs.readFileSync(p);
        return new NextResponse(fileBuffer, {
          headers: {
            'Content-Type': 'image/png',
            'Cache-Control': 'public, max-age=86400, immutable',
          },
        });
      }
    }

    // Default lightweight placeholder PNG if file not on disk in serverless
    // Return a 1x1 transparent png or svg
    return new NextResponse('Screenshot file not found on local disk', { status: 404 });
  } catch (err: any) {
    return NextResponse.json({ error: 'Failed to serve image', details: err?.message }, { status: 500 });
  }
}
