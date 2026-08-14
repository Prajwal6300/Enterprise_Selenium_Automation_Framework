/**
 * Enterprise Secret and Credential Masking Utility.
 * Automatically redacts passwords, tokens, API keys, BrowserStack keys, and DB credentials.
 */

export function maskSecrets(input: string): string {
  if (!input) return '';

  let output = input;

  // Mask key-value secrets (e.g. password=secret123, access_key: "xyz")
  output = output.replace(
    /(password|passwd|secret|access_key|api_key|token|auth_token)\s*[:=]\s*["']?([^"'\s,;]+)["']?/gi,
    (_match, key) => `${key}=***REDACTED***`
  );

  // Mask bearer tokens
  output = output.replace(
    /(bearer\s+)([A-Za-z0-9\-_=.]+)/gi,
    '$1***REDACTED_TOKEN***'
  );

  // Mask basic auth URLs: https://user:pass@host
  output = output.replace(
    /(https?:\/\/)([^:]+):([^@]+)@/gi,
    '$1***:***@'
  );

  // Mask PostgreSQL connection strings
  output = output.replace(
    /(postgres(?:ql)?:\/\/)([^:]+):([^@]+)@/gi,
    '$1***:***@'
  );

  return output;
}
