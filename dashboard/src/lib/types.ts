export type TestStatus = 'PASSED' | 'FAILED' | 'SKIPPED' | 'RUNNING' | 'CANCELLED';
export type TestModule = 'Login' | 'Cart' | 'Checkout' | 'Search' | 'Logout' | 'API' | 'Database' | 'Core';
export type TestType = 'UI' | 'API' | 'Database' | 'E2E' | 'Regression' | 'Smoke';
export type BrowserType = 'Chrome' | 'Firefox' | 'Edge' | 'BrowserStack';
export type EnvironmentType = 'QA' | 'UAT' | 'PROD';

export interface TestStep {
  name: string;
  status: 'passed' | 'failed' | 'skipped' | 'running';
  duration: number;
  timestamp: string;
  details?: string;
}

export interface FailureDetail {
  error_type: string;
  error_message: string;
  stack_trace: string;
  failure_category: string;
  screenshot_path?: string | null;
  screenshot_uri?: string | null;
}

export interface TestResult {
  test_id: string;
  name: string;
  class_name: string;
  module: string;
  file_path: string;
  test_type: string;
  browser: string;
  environment: string;
  status: TestStatus;
  duration: number;
  start_time: string;
  end_time: string;
  steps: TestStep[];
  assertions: string[];
  failure?: FailureDetail | null;
  log_snippet: string;
  screenshot_path?: string | null;
  screenshot_uri?: string | null;
  categories: string[];
  parameters?: Record<string, any>;
}

export interface ExecutionSummary {
  execution_id: string;
  timestamp: string;
  date: string;
  time: string;
  environment: string;
  browser: string;
  branch: string;
  commit_hash: string;
  ci_system: string;
  host_machine?: string;
  operating_system?: string;
  python_version?: string;
  selenium_version?: string;
  status: TestStatus;
  duration: number;
  total: number;
  passed: number;
  failed: number;
  skipped: number;
  pass_rate: number;
  tests: TestResult[];
}

export interface ExecutionIndexItem {
  execution_id: string;
  timestamp: string;
  date: string;
  time: string;
  environment: string;
  browser: string;
  branch: string;
  commit_hash: string;
  ci_system: string;
  status: TestStatus;
  duration: number;
  total: number;
  passed: number;
  failed: number;
  skipped: number;
  pass_rate: number;
}

export interface FailureGroup {
  test_name: string;
  error_message: string;
  module: string;
  browser: string;
  environment: string;
  failure_category: string;
  first_seen: string;
  last_seen: string;
  failure_count: number;
  screenshot_path?: string | null;
  screenshot_uri?: string | null;
  stack_trace: string;
  latest_execution_id: string;
}

export interface BrowserMetric {
  browser: string;
  total_tests: number;
  passed: number;
  failed: number;
  skipped: number;
  pass_rate: number;
  avg_duration: number;
}

export interface EnvironmentMetric {
  environment: string;
  total_executions: number;
  total_tests: number;
  passed: number;
  failed: number;
  pass_rate: number;
  avg_duration: number;
}

export interface ReportItem {
  id: string;
  title: string;
  type: 'html' | 'allure' | 'junit' | 'json' | 'csv' | 'excel' | 'pdf' | 'executive';
  description: string;
  generated_at: string;
  file_size: string;
  file_path: string;
  download_url: string;
  view_url?: string;
}

export interface CicdPipeline {
  name: string;
  provider: 'GitHub Actions' | 'Jenkins' | 'BrowserStack' | 'Docker';
  status: 'PASSED' | 'FAILED' | 'RUNNING' | 'CONFIGURED' | 'IDLE';
  last_run: string;
  duration: string;
  branch: string;
  commit_hash: string;
  workflow_file?: string;
  details?: string;
  url?: string;
}

export interface SystemHealth {
  status: 'HEALTHY' | 'DEGRADED' | 'UNHEALTHY';
  uptime_seconds: number;
  timestamp: string;
  version: string;
  components: {
    dashboard_api: { status: 'healthy' | 'unhealthy'; message: string };
    database: { status: 'healthy' | 'degraded'; type: 'PostgreSQL' | 'Local File Storage'; message: string };
    test_results: { status: 'available' | 'unavailable'; total_executions: number; latest_execution: string };
    github_actions: { status: 'connected' | 'configured' | 'unavailable'; message: string };
    jenkins: { status: 'connected' | 'configured' | 'unavailable'; message: string };
    browserstack: { status: 'configured' | 'not_configured'; message: string };
  };
}

export interface LiveExecutionStatus {
  is_active: boolean;
  status: 'QUEUED' | 'RUNNING' | 'PASSED' | 'FAILED' | 'CANCELLED' | 'IDLE';
  execution_id?: string;
  total?: number;
  completed?: number;
  passed?: number;
  failed?: number;
  remaining?: number;
  current_test?: string;
  message?: string;
}
