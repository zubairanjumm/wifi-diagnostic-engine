import type { BrowserEvidence } from "../types/diagnostic"

interface RequestResult {
  success: boolean
  latencyMs: number | null
}

async function testRequest(url: string): Promise<RequestResult> {
  const start = performance.now()

  try {
    const response = await fetch(url, {
      method: "GET",
      cache: "no-store",
    })

    const end = performance.now()

    return {
      success: response.ok,
      latencyMs: end - start,
    }
  } catch {
    return {
      success: false,
      latencyMs: null,
    }
  }
}

function calculateAverage(values: number[]): number | null {
  if (values.length === 0) {
    return null
  }

  return (
    values.reduce((sum, value) => sum + value, 0) /
    values.length
  )
}

function calculateJitter(values: number[]): number | null {
  if (values.length < 2) {
    return null
  }

  let totalDifference = 0

  for (let i = 1; i < values.length; i++) {
    totalDifference += Math.abs(
      values[i] - values[i - 1],
    )
  }

  return totalDifference / (values.length - 1)
}

export async function collectBrowserEvidence(
  endpoint: string,
  requestCount = 10,
): Promise<BrowserEvidence> {
  const results: RequestResult[] = []

  for (let i = 0; i < requestCount; i++) {
    const url = `${endpoint}?test=${Date.now()}-${i}`

    results.push(await testRequest(url))
  }

  const successfulRequests = results.filter(
    (result) => result.success,
  )

  const successfulLatencies = successfulRequests
    .map((result) => result.latencyMs)
    .filter(
      (latency): latency is number =>
        latency !== null,
    )

  const successRate =
    (successfulRequests.length / results.length) * 100

  const failureRate = 100 - successRate

  return {
    https_reachable:
      successfulRequests.length > 0,

    request_success_rate: successRate,
    request_failure_rate: failureRate,

    browser_latency_min_ms:
      successfulLatencies.length > 0
        ? Math.min(...successfulLatencies)
        : null,

    browser_latency_average_ms:
      calculateAverage(successfulLatencies),

    browser_latency_max_ms:
      successfulLatencies.length > 0
        ? Math.max(...successfulLatencies)
        : null,

    browser_latency_jitter_ms:
      calculateJitter(successfulLatencies),

    download_mbps: null,
    upload_mbps: null,
  }
}