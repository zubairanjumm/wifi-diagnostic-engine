const API_URL =
  import.meta.env.VITE_DIAGNOSTIC_API_URL ||
  "http://127.0.0.1:8000"

type BrowserEvidence = {
  https_reachable: boolean
  request_success_rate: number
  request_failure_rate: number
  browser_latency_min_ms: number | null
  browser_latency_average_ms: number | null
  browser_latency_max_ms: number | null
  browser_latency_jitter_ms: number | null
}

export async function collectBrowserEvidence(
  endpoint: string,
  requestCount: number = 10,
): Promise<BrowserEvidence> {
  const latencies: number[] = []
  let successfulRequests = 0
  let failedRequests = 0

  for (let i = 0; i < requestCount; i++) {
    const start = performance.now()

    try {
      await fetch(`${endpoint}?test=${Date.now()}-${i}`, {
        method: "GET",
        cache: "no-store",
      })

      const end = performance.now()
      const latency = end - start

      latencies.push(latency)
      successfulRequests++
    } catch {
      failedRequests++
    }
  }

  const totalRequests = successfulRequests + failedRequests

  if (totalRequests === 0) {
    return {
      https_reachable: false,
      request_success_rate: 0,
      request_failure_rate: 100,
      browser_latency_min_ms: null,
      browser_latency_average_ms: null,
      browser_latency_max_ms: null,
      browser_latency_jitter_ms: null,
    }
  }

  const successRate = (successfulRequests / totalRequests) * 100
  const failureRate = (failedRequests / totalRequests) * 100

  if (latencies.length === 0) {
    return {
      https_reachable: true,
      request_success_rate: successRate,
      request_failure_rate: failureRate,
      browser_latency_min_ms: null,
      browser_latency_average_ms: null,
      browser_latency_max_ms: null,
      browser_latency_jitter_ms: null,
    }
  }

  const min = Math.min(...latencies)
  const max = Math.max(...latencies)
  const average =
    latencies.reduce((sum, value) => sum + value, 0) / latencies.length

  const jitterValues = []

  for (let i = 1; i < latencies.length; i++) {
    jitterValues.push(Math.abs(latencies[i] - latencies[i - 1]))
  }

  const jitter =
    jitterValues.length > 0
      ? jitterValues.reduce((sum, value) => sum + value, 0) /
        jitterValues.length
      : 0

  return {
    https_reachable: true,
    request_success_rate: successRate,
    request_failure_rate: failureRate,
    browser_latency_min_ms: min,
    browser_latency_average_ms: average,
    browser_latency_max_ms: max,
    browser_latency_jitter_ms: jitter,
  }
}