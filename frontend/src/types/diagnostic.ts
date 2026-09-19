export interface BrowserEvidence {
  https_reachable: boolean | null

  request_count: number
  successful_request_count: number
  failed_request_count: number

  request_success_rate: number | null
  request_failure_rate: number | null

  browser_latency_min_ms: number | null
  browser_latency_average_ms: number | null
  browser_latency_median_ms: number | null
  browser_latency_p95_ms: number | null
  browser_latency_max_ms: number | null
  browser_latency_jitter_ms: number | null

  download_mbps: number | null
  upload_mbps: number | null
}

export interface DiagnosticResponse {
  diagnosis: string
  title: string
  message: string
  next_action: string
}