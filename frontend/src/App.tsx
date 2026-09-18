import { useState } from "react"
import { collectBrowserEvidence } from "./diagnostics/browser"
import { diagnoseBrowserEvidence } from "./api/diagnosticApi"
import type { BrowserEvidence } from "./types/diagnostic"

function App() {
  const [evidence, setEvidence] = useState<BrowserEvidence | null>(null)
  const [diagnosis, setDiagnosis] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function runDiagnostic() {
    setLoading(true)
    setError(null)
    setEvidence(null)
    setDiagnosis(null)

    try {
      const browserEvidence = await collectBrowserEvidence(
        window.location.origin,
      )

      setEvidence(browserEvidence)

      const diagnosticResult = await diagnoseBrowserEvidence(
        browserEvidence,
      )

      setDiagnosis(diagnosticResult.diagnosis)
    } catch {
      setError("Failed to complete the diagnostic.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="min-h-screen bg-white text-black flex items-center justify-center px-6">
      <div className="w-full max-w-2xl">
        <h1 className="text-4xl font-semibold">
          WiFi Diagnostic
        </h1>

        <p className="mt-3 text-gray-600">
          Test your internet connection.
        </p>

        <button
          onClick={runDiagnostic}
          disabled={loading}
          className="mt-8 rounded-lg bg-black px-6 py-3 text-white disabled:opacity-50"
        >
          {loading ? "Testing..." : "Run Diagnostic"}
        </button>

        {error && (
          <p className="mt-6 text-red-600">
            {error}
          </p>
        )}

        {evidence && (
          <div className="mt-8 space-y-3 rounded-xl border border-gray-200 p-6">
            <h2 className="text-xl font-medium">
              Browser Evidence
            </h2>

            <p>
              HTTPS reachable:{" "}
              <strong>
                {String(evidence.https_reachable)}
              </strong>
            </p>

            <p>
              Request success rate:{" "}
              <strong>
                {evidence.request_success_rate?.toFixed(1)}%
              </strong>
            </p>

            <p>
              Request failure rate:{" "}
              <strong>
                {evidence.request_failure_rate?.toFixed(1)}%
              </strong>
            </p>

            <p>
              Minimum latency:{" "}
              <strong>
                {evidence.browser_latency_min_ms?.toFixed(2)} ms
              </strong>
            </p>

            <p>
              Average latency:{" "}
              <strong>
                {evidence.browser_latency_average_ms?.toFixed(2)} ms
              </strong>
            </p>

            <p>
              Maximum latency:{" "}
              <strong>
                {evidence.browser_latency_max_ms?.toFixed(2)} ms
              </strong>
            </p>

            <p>
              Jitter:{" "}
              <strong>
                {evidence.browser_latency_jitter_ms?.toFixed(2)} ms
              </strong>
            </p>

            {diagnosis && (
              <div className="mt-6 border-t border-gray-200 pt-6">
                <h2 className="text-xl font-medium">
                  Diagnosis
                </h2>

                <p className="mt-2">
                  {diagnosis}
                </p>
              </div>
            )}
          </div>
        )}
      </div>
    </main>
  )
}

export default App