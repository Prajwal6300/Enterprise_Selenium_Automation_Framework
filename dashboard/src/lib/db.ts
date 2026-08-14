/**
 * Enterprise QA Database Adapter.
 * Supports PostgreSQL when DATABASE_URL is configured, and falls back to
 * high-performance JSON File Storage when running locally or in standalone mode.
 */

import { Pool } from 'pg';
import { ExecutionSummary } from './types';
import { getAllExecutions } from './result-parser';

let pool: Pool | null = null;

export function getDbPool(): Pool | null {
  const connectionString = process.env.DATABASE_URL;
  if (!connectionString) return null;

  if (!pool) {
    pool = new Pool({
      connectionString,
      ssl: connectionString.includes('localhost') ? false : { rejectUnauthorized: false },
      max: 10,
      idleTimeoutMillis: 30000,
    });
  }
  return pool;
}

export async function initializeDatabase(): Promise<boolean> {
  const db = getDbPool();
  if (!db) return false;

  try {
    const client = await db.connect();
    try {
      await client.query(`
        CREATE TABLE IF NOT EXISTS executions (
          execution_id VARCHAR(64) PRIMARY KEY,
          timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
          date VARCHAR(32),
          time VARCHAR(16),
          environment VARCHAR(16),
          browser VARCHAR(32),
          branch VARCHAR(64),
          commit_hash VARCHAR(64),
          ci_system VARCHAR(64),
          status VARCHAR(16),
          duration NUMERIC(8, 2),
          total INT,
          passed INT,
          failed INT,
          skipped INT,
          pass_rate NUMERIC(5, 2),
          data JSONB,
          created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
      `);
      return true;
    } finally {
      client.release();
    }
  } catch (err) {
    console.error('Failed to initialize PostgreSQL schema:', err);
    return false;
  }
}

export async function saveExecutionToDb(exec: ExecutionSummary): Promise<boolean> {
  const db = getDbPool();
  if (!db) return false;

  try {
    const client = await db.connect();
    try {
      await client.query(
        `
        INSERT INTO executions (
          execution_id, timestamp, date, time, environment, browser,
          branch, commit_hash, ci_system, status, duration,
          total, passed, failed, skipped, pass_rate, data
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17)
        ON CONFLICT (execution_id) DO UPDATE SET
          status = EXCLUDED.status,
          duration = EXCLUDED.duration,
          passed = EXCLUDED.passed,
          failed = EXCLUDED.failed,
          pass_rate = EXCLUDED.pass_rate,
          data = EXCLUDED.data;
      `,
        [
          exec.execution_id,
          exec.timestamp,
          exec.date,
          exec.time,
          exec.environment,
          exec.browser,
          exec.branch,
          exec.commit_hash,
          exec.ci_system,
          exec.status,
          exec.duration,
          exec.total,
          exec.passed,
          exec.failed,
          exec.skipped,
          exec.pass_rate,
          JSON.stringify(exec),
        ]
      );
      return true;
    } finally {
      client.release();
    }
  } catch (err) {
    console.error('Error saving execution to PostgreSQL:', err);
    return false;
  }
}
