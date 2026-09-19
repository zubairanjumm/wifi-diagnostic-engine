import type {
  BrowserEvidence,
  DiagnosticResponse,
} from "../types/diagnostic"

interface ResultPageProps {
  result: DiagnosticResponse
  evidence: BrowserEvidence | null
  onRunAgain: () => void
  onHome: () => void
}

function Metric({
  label,
  value,
}: {
  label: string
  value: string
}) {
  return (
    <div className="rounded-lg border border-gray-200 p-4">
      <p className="text-sm text-gray-500">{label}</p>

      <p className="mt-1 text-lg font-medium text-black">
        {value}
      </p>
    </div>
  )
}

function formatValue(
  value: number | null,
  unit = "",
): string {
  if (value === null) {
    return "Unavailable"
  }

  return `${value.toFixed(1)}${unit}`
}

export function ResultPage({
  result,
  evidence,
  onRunAgain,
  onHome,
}: ResultPageProps) {
  return (
    <main className="min-h-screen bg-white px-6 py-12 text-black">
      <div className="mx-auto max-w-3xl">
        <div className="text-center">
          <p className="text-sm font-medium uppercase tracking-wide text-gray-500">
            Diagnostic result
          </p>

          <h1 className="mt-3 text-3xl font-semibold tracking-tight">
            {result.title}
          </h1>

          <p className="mx-auto mt-4 max-w-2xl text-gray-600">
            {result.message}
          </p>
        </div>

        <div className="mt-8 rounded-xl border border-gray-200 p-6">
          <p className="text-sm font-medium text-gray-500">
            Recommended next step
          </p>

          <p className="mt-2 text-lg text-black">
            {result.next_action}
          </p>
        </div>

        {evidence && (
          <div className="mt-8">
            <h2 className="text-xl font-semibold">
              Network evidence
            </h2>

            <p className="mt-2 text-sm text-gray-500">
              These measurements were collected by your browser
              during the diagnostic.
            </p>

            <div className="mt-6 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
              <Metric
                label="Request success"
                value={formatValue(
                  evidence.request_success_rate,
                  "%",
                )}
              />

              <Metric
                label="Average latency"
                value={formatValue(
                  evidence.browser_latency_average_ms,
                  " ms",
                )}
              />

              <Metric
                label="Jitter"
                value={formatValue(
                  evidence.browser_latency_jitter_ms,
                  " ms",
                )}
              />

              <Metric
                label="Minimum latency"
                value={formatValue(
                  evidence.browser_latency_min_ms,
                  " ms",
                )}
              />

              <Metric
                label="Maximum latency"
                value={formatValue(
                  evidence.browser_latency_max_ms,
                  " ms",
                )}
              />

              <Metric
                label="Request failures"
                value={formatValue(
                  evidence.request_failure_rate,
                  "%",
                )}
              />

              <Metric
                label="Median latency"
                value={formatValue(
                  evidence.browser_latency_median_ms,
                  " ms",
                )}
              />

              <Metric
                label="95th percentile latency"
                value={formatValue(
                  evidence.browser_latency_p95_ms,
                  " ms",
                )}
              />

              <Metric
                label="Download speed"
                value={formatValue(
                  evidence.download_mbps,
                  " Mbps",
                )}
              />

              <Metric
                label="Upload speed"
                value={formatValue(
                  evidence.upload_mbps,
                  " Mbps",
                )}
              />

              <Metric
                label="Requests tested"
                value={evidence.request_count.toString()}
              />
            </div>

            <p className="mt-6 text-sm text-gray-500">
              Note: browser diagnostics measure the connection
              between your browser and the diagnostic server. They
              cannot directly inspect your Wi-Fi adapter or router.
            </p>
          </div>
        )}

        <div className="mt-8 flex justify-center gap-3">
          <button
            onClick={onRunAgain}
            className="rounded-lg border border-black px-6 py-3 text-sm font-medium transition hover:bg-black hover:text-white"
          >
            Run diagnostic again
          </button>

          <button
            onClick={onHome}
            className="rounded-lg border border-gray-300 px-6 py-3 text-sm font-medium text-gray-700 transition hover:bg-gray-100"
          >
            Home
          </button>
        </div>
      </div>
    </main>
  )
}