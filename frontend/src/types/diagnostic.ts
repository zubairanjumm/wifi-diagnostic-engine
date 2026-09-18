export interface BrowserEvidence {
  https_reachable: boolean | null

  request_success_rate: number | null
  request_failure_rate: number | null

  browser_latency_min_ms: number | null
  browser_latency_average_ms: number | null
  browser_latency_max_ms: number | null
  browser_latency_jitter_ms: number | null

  download_mbps: number | null
  upload_mbps: number | null
}