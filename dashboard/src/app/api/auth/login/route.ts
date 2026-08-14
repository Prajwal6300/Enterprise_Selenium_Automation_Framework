import { NextRequest, NextResponse } from 'next/server';
import { verifyCredentials, createSessionToken } from '@/lib/auth';

export async function POST(request: NextRequest) {
  try {
    const { username, password } = await request.json();

    if (!verifyCredentials(username, password)) {
      return NextResponse.json(
        { error: 'Invalid username or password' },
        { status: 401 }
      );
    }

    const token = createSessionToken(username, 'Admin');
    const response = NextResponse.json({
      success: true,
      user: { username, role: 'Admin' },
    });

    response.cookies.set('enterprise_qa_session', token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'lax',
      maxAge: 60 * 60 * 24 * 7, // 7 days
      path: '/',
    });

    return response;
  } catch (err: any) {
    return NextResponse.json({ error: 'Authentication failed', details: err?.message }, { status: 500 });
  }
}
