/**
 * Enterprise Dashboard Authentication & Session Management.
 * Supports environment-configured administrative credentials and cookie-based sessions.
 */

import { cookies } from 'next/headers';

const SESSION_COOKIE_NAME = 'enterprise_qa_session';
const DEFAULT_USER = process.env.DASHBOARD_ADMIN_USER || 'admin';
const DEFAULT_PASS = process.env.DASHBOARD_ADMIN_PASSWORD || 'enterprise123';

export interface UserSession {
  username: string;
  role: 'Admin' | 'QA Lead' | 'Viewer';
  isAuthenticated: boolean;
  loginTime: string;
}

export function verifyCredentials(username: string, password: string): boolean {
  if (!username || !password) return false;
  return username.trim() === DEFAULT_USER && password === DEFAULT_PASS;
}

export function createSessionToken(username: string, role: 'Admin' | 'QA Lead' = 'Admin'): string {
  const payload = {
    username,
    role,
    time: new Date().toISOString(),
    sig: 'ent_auth_ok',
  };
  return Buffer.from(JSON.stringify(payload)).toString('base64');
}

export function parseSessionToken(token: string): UserSession | null {
  try {
    const raw = Buffer.from(token, 'base64').toString('utf-8');
    const data = JSON.parse(raw);
    if (data.sig === 'ent_auth_ok' && data.username) {
      return {
        username: data.username,
        role: data.role || 'Admin',
        isAuthenticated: true,
        loginTime: data.time || new Date().toISOString(),
      };
    }
  } catch {
    // ignore
  }
  return null;
}

export async function getCurrentUser(): Promise<UserSession> {
  const cookieStore = await cookies();
  const sessionToken = cookieStore.get(SESSION_COOKIE_NAME)?.value;

  if (sessionToken) {
    const session = parseSessionToken(sessionToken);
    if (session) return session;
  }

  // Default guest session with Viewer access if no strict auth enforced
  return {
    username: 'Demo QA Engineer',
    role: 'Viewer',
    isAuthenticated: false,
    loginTime: new Date().toISOString(),
  };
}
