import type { BrowserEvidence } from "../types/diagnostic"

const DEFAULT_REQUEST_COUNT = 12

function calculateAverage(values: number[]): number {
  if (values.length === 0) {
    return 0
  }

  return (
    values.reduce((sum, value) => sum + value, 0) /
    values.length
  )
}

function calculateMedian(values: number[]): number {
  if (values.length === 0) {
    return 0
  }

  const sorted = [...values].sort((a, b) => a - b)
  const middle = Math.floor(sorted.length / 2)

  if (sorted.length % 2 === 0) {
    return (
      (sorted[middle - 1] + sorted[middle]) /
      2
    )
  }

  return sorted[middle]
}

function calculatePercentile(
  values: number[],
  percentile: number,
): number {
  if (values.length === 0) {
    return 0
  }

  const sorted = [...values].sort((a, b) => a - b)

  const index =
    (percentile / 100) *
    (sorted.length - 1)

  const lower = Math.floor(index)
  const upper = Math.ceil(index)

  if (lower === upper) {
    return sorted[lower]
  }

  const weight = index - lower

  return (
    sorted[lower] +
    (sorted[upper] - sorted[lower]) *
      weight
  )
}

function calculateJitter(values: number[]): number {
  if (values.length < 2) {
    return 0
  }

  const differences: number[] = []

  for (
    let index = 1;
    index < values.length;
    index += 1
  ) {
    differences.push(
      Math.abs(
        values[index] -
          values[index - 1],
      ),
    )
  }

  return calculateAverage(differences)
}

async function testRequest(
  url: string,
): Promise<number> {
  const start = performance.now()

  const response = await fetch(url, {
    method: "GET",
    cache: "no-store",
  })

  if (!response.ok) {
    throw new Error(
      `Diagnostic request failed with status ${response.status}`,
    )
  }

  await response.arrayBuffer()

  return performance.now() - start
}

export async function collectBrowserEvidence(
  diagnosticTestUrl: string,
): Promise<BrowserEvidence> {
  const latencies: number[] = []

  let successfulRequests = 0
  let failedRequests = 0

  for (
    let index = 0;
    index < DEFAULT_REQUEST_COUNT;
    index += 1
  ) {
    try {
      const latency =
        await testRequest(
          `${diagnosticTestUrl}?test=${Date.now()}-${index}`,
        )

      latencies.push(latency)
      successfulRequests += 1
    } catch {
      failedRequests += 1
    }
  }

  const totalRequests =
    successfulRequests +
    failedRequests

  const successRate =
    totalRequests > 0
      ? (successfulRequests /
          totalRequests) *
        100
      : 0

  const failureRate =
    totalRequests > 0
      ? (failedRequests /
          totalRequests) *
        100
      : 0

  return {
    https_reachable:
      successfulRequests > 0,

    request_count:
      totalRequests,

    successful_request_count:
      successfulRequests,

    failed_request_count:
      failedRequests,

    request_success_rate:
      successRate,

    request_failure_rate:
      failureRate,

    browser_latency_min_ms:
      latencies.length > 0
        ? Math.min(...latencies)
        : 0,

    browser_latency_average_ms:
      calculateAverage(latencies),

    browser_latency_median_ms:
      calculateMedian(latencies),

    browser_latency_p95_ms:
      calculatePercentile(
        latencies,
        95,
      ),

    browser_latency_max_ms:
      latencies.length > 0
        ? Math.max(...latencies)
        : 0,

    browser_latency_jitter_ms:
      calculateJitter(latencies),

    download_mbps: null,

    upload_mbps: null,
  }
}
