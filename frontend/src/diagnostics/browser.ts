import type { BrowserEvidence } from "../types/diagnostic"

const DEFAULT_REQUEST_COUNT = 12
const DOWNLOAD_SIZE_MB = 3
const UPLOAD_SIZE_MB = 3

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

async function measureDownloadSpeed(
  url: string,
): Promise<number> {
  const start = performance.now()

  const response = await fetch(
    `${url}?size_mb=${DOWNLOAD_SIZE_MB}&t=${Date.now()}`,
    {
      method: "GET",
      cache: "no-store",
    },
  )

  if (!response.ok) {
    throw new Error(
      `Download test failed with status ${response.status}`,
    )
  }

  if (!response.body) {
    throw new Error(
      "Download response does not contain a readable body",
    )
  }

  const reader =
    response.body.getReader()

  let totalBytes = 0

  while (true) {
    const { done, value } =
      await reader.read()

    if (done) {
      break
    }

    if (value) {
      totalBytes += value.byteLength
    }
  }

  const elapsedSeconds =
    (performance.now() - start) / 1000

  if (elapsedSeconds <= 0) {
    return 0
  }

  return (
    (totalBytes * 8) /
    elapsedSeconds /
    1_000_000
  )
}

async function measureUploadSpeed(
  url: string,
): Promise<number> {
  const payload =
    new Uint8Array(
      UPLOAD_SIZE_MB *
        1024 *
        1024,
    )

  const start = performance.now()

  const response = await fetch(
    `${url}?t=${Date.now()}`,
    {
      method: "POST",
      headers: {
        "Content-Type":
          "application/octet-stream",
      },
      body: payload,
    },
  )

  if (!response.ok) {
    throw new Error(
      `Upload test failed with status ${response.status}`,
    )
  }

  await response.arrayBuffer()

  const elapsedSeconds =
    (performance.now() - start) / 1000

  if (elapsedSeconds <= 0) {
    return 0
  }

  return (
    (payload.byteLength * 8) /
    elapsedSeconds /
    1_000_000
  )
}

export async function collectBrowserEvidence(
  diagnosticTestUrl: string,
  downloadUrl: string,
  uploadUrl: string,
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

  const downloadSamples: number[] = []
  const uploadSamples: number[] = []

  for (
    let index = 0;
    index < 3;
    index += 1
  ) {
    try {
      downloadSamples.push(
        await measureDownloadSpeed(
          downloadUrl,
        ),
      )
    } catch {
      // Keep the remaining diagnostic measurements usable.
    }
  }

  for (
    let index = 0;
    index < 3;
    index += 1
  ) {
    try {
      uploadSamples.push(
        await measureUploadSpeed(
          uploadUrl,
        ),
      )
    } catch {
      // Keep the remaining diagnostic measurements usable.
    }
  }

  const downloadSpeed =
    downloadSamples.length > 0
      ? calculateAverage(
          downloadSamples,
        )
      : 0

  const uploadSpeed =
    uploadSamples.length > 0
      ? calculateAverage(
          uploadSamples,
        )
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

    download_mbps:
      downloadSpeed,

    upload_mbps:
      uploadSpeed,
  }
}