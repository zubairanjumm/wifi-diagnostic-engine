import type { BrowserEvidence } from "../types/diagnostic"

interface RequestResult {
  success: boolean
  latencyMs: number | null
}

const DOWNLOAD_SIZE_MB = 3
const UPLOAD_SIZE_MB = 3

function calculateAverage(values: number[]): number | null {
  if (values.length === 0) {
    return null
  }

  return (
    values.reduce((sum, value) => sum + value, 0) /
    values.length
  )
}

function calculateMedian(values: number[]): number | null {
  if (values.length === 0) {
    return null
  }

  const sorted = [...values].sort((a, b) => a - b)
  const middle = Math.floor(sorted.length / 2)

  if (sorted.length % 2 === 0) {
    return (sorted[middle - 1] + sorted[middle]) / 2
  }

  return sorted[middle]
}

function calculatePercentile(
  values: number[],
  percentile: number,
): number | null {
  if (values.length === 0) {
    return null
  }

  const sorted = [...values].sort((a, b) => a - b)

  const index =
    (percentile / 100) * (sorted.length - 1)

  const lower = Math.floor(index)
  const upper = Math.ceil(index)

  if (lower === upper) {
    return sorted[lower]
  }

  const weight = index - lower

  return (
    sorted[lower] +
    (sorted[upper] - sorted[lower]) * weight
  )
}

function calculateJitter(
  values: number[],
): number | null {
  if (values.length < 2) {
    return null
  }

  let totalDifference = 0

  for (let i = 1; i < values.length; i++) {
    totalDifference += Math.abs(
      values[i] - values[i - 1],
    )
  }

  return (
    totalDifference /
    (values.length - 1)
  )
}

async function testRequest(
  url: string,
): Promise<RequestResult> {
  const start = performance.now()

  try {
    const response = await fetch(url, {
      method: "GET",
      cache: "no-store",
    })

    const end = performance.now()

    return {
      success: response.ok,
      latencyMs: response.ok
        ? end - start
        : null,
    }
  } catch {
    return {
      success: false,
      latencyMs: null,
    }
  }
}

async function measureDownloadSpeed(
  endpoint: string,
): Promise<number | null> {
  const start = performance.now()

  try {
    const response = await fetch(
      `${endpoint}?size_mb=${DOWNLOAD_SIZE_MB}&test=${Date.now()}`,
      {
        method: "GET",
        cache: "no-store",
      },
    )

    if (!response.ok || !response.body) {
      return null
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

    if (
      elapsedSeconds <= 0 ||
      totalBytes === 0
    ) {
      return null
    }

    return (
      (totalBytes * 8) /
      elapsedSeconds /
      1_000_000
    )
  } catch {
    return null
  }
}

async function measureUploadSpeed(
  endpoint: string,
): Promise<number | null> {
  const sizeBytes =
    UPLOAD_SIZE_MB * 1024 * 1024

  const payload =
    new Uint8Array(sizeBytes)

  const start = performance.now()

  try {
    const response = await fetch(
      `${endpoint}?test=${Date.now()}`,
      {
        method: "POST",
        headers: {
          "Content-Type":
            "application/octet-stream",
        },
        body: payload,
        cache: "no-store",
      },
    )

    if (!response.ok) {
      return null
    }

    const elapsedSeconds =
      (performance.now() - start) / 1000

    if (elapsedSeconds <= 0) {
      return null
    }

    return (
      (sizeBytes * 8) /
      elapsedSeconds /
      1_000_000
    )
  } catch {
    return null
  }
}

export async function collectBrowserEvidence(
  diagnosticEndpoint: string,
  downloadEndpoint: string,
  uploadEndpoint: string,
  requestCount = 12,
): Promise<BrowserEvidence> {
  const results: RequestResult[] = []

  for (let i = 0; i < requestCount; i++) {
    const url =
      `${diagnosticEndpoint}?test=${Date.now()}-${i}`

    results.push(
      await testRequest(url),
    )
  }

  const successfulRequests =
    results.filter(
      (result) => result.success,
    )

  const successfulLatencies =
    successfulRequests
      .map(
        (result) => result.latencyMs,
      )
      .filter(
        (latency): latency is number =>
          latency !== null,
      )

  const successRate =
    results.length > 0
      ? (successfulRequests.length /
          results.length) *
        100
      : 0

  const failureRate =
    100 - successRate

  const downloadSpeeds: number[] = []
  const uploadSpeeds: number[] = []

  const speedTestCount = 3

  for (
    let i = 0;
    i < speedTestCount;
    i++
  ) {
    const download =
      await measureDownloadSpeed(
        downloadEndpoint,
      )

    if (download !== null) {
      downloadSpeeds.push(download)
    }

    const upload =
      await measureUploadSpeed(
        uploadEndpoint,
      )

    if (upload !== null) {
      uploadSpeeds.push(upload)
    }
  }

  return {
    https_reachable:
      successfulRequests.length > 0,

    request_count: results.length,

    successful_request_count:
      successfulRequests.length,

    failed_request_count:
      results.length -
      successfulRequests.length,

    request_success_rate:
      successRate,

    request_failure_rate:
      failureRate,

    browser_latency_min_ms:
      successfulLatencies.length > 0
        ? Math.min(
            ...successfulLatencies,
          )
        : null,

    browser_latency_average_ms:
      calculateAverage(
        successfulLatencies,
      ),

    browser_latency_median_ms:
      calculateMedian(
        successfulLatencies,
      ),

    browser_latency_p95_ms:
      calculatePercentile(
        successfulLatencies,
        95,
      ),

    browser_latency_max_ms:
      successfulLatencies.length > 0
        ? Math.max(
            ...successfulLatencies,
          )
        : null,

    browser_latency_jitter_ms:
      calculateJitter(
        successfulLatencies,
      ),

    download_mbps:
      calculateAverage(
        downloadSpeeds,
      ),

    upload_mbps:
      calculateAverage(
        uploadSpeeds,
      ),
  }
}
