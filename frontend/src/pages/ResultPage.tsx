import { Metric } from "../components/Metric"
import type {
  BrowserEvidence,
  DiagnosticResponse,
} from "../types/diagnostic"

interface ResultPageProps {
  evidence: BrowserEvidence
  result: DiagnosticResponse
  onRunAgain: () => void
  onHome: () => void
}

export function ResultPage({
  evidence,
  result,
  onRunAgain,
  onHome,
}: ResultPageProps) {
  return (
    <main className="mx-auto max-w-5xl px-6 py-16 md:py-24">
      <div className="max-w-3xl">
        <p className="text-sm font-medium uppercase tracking-widest text-black/40">
          Diagnostic complete
        </p>

        <h1 className="mt-5 text-4xl font-semibold tracking-tight md:text-5xl">
          {result.title}
        </h1>

        <p className="mt-5 max-w-2xl text-lg leading-8 text-black/55">
          {result.message}
        </p>
      </div>

      <div className="mt-10 rounded-2xl border border-black/10 bg-black p-7 text-white md:p-9">
        <p className="text-xs font-medium uppercase tracking-widest text-white/40">
          Recommended next step
        </p>

        <p className="mt-4 max-w-2xl text-lg leading-7 text-white/80">
          {result.next_action}
        </p>
      </div>

      <section className="mt-12">
        <div>
          <p className="text-sm font-medium uppercase tracking-widest text-black/40">
            Evidence collected
          </p>

          <h2 className="mt-3 text-2xl font-semibold tracking-tight">
            What we measured
          </h2>
        </div>

        <div className="mt-6 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          <Metric
            label="Request success"
            value={
              evidence.request_success_rate !== null
                ? `${evidence.request_success_rate.toFixed(1)}%`
                : "N/A"
            }
          />

          <Metric
            label="Average latency"
            value={
              evidence.browser_latency_average_ms !== null
                ? `${evidence.browser_latency_average_ms.toFixed(2)} ms`
                : "N/A"
            }
          />

          <Metric
            label="Jitter"
            value={
              evidence.browser_latency_jitter_ms !== null
                ? `${evidence.browser_latency_jitter_ms.toFixed(2)} ms`
                : "N/A"
            }
          />

          <Metric
            label="Minimum latency"
            value={
              evidence.browser_latency_min_ms !== null
                ? `${evidence.browser_latency_min_ms.toFixed(2)} ms`
                : "N/A"
            }
          />

          <Metric
            label="Maximum latency"
            value={
              evidence.browser_latency_max_ms !== null
                ? `${evidence.browser_latency_max_ms.toFixed(2)} ms`
                : "N/A"
            }
          />

          <Metric
            label="Request failures"
            value={
              evidence.request_failure_rate !== null
                ? `${evidence.request_failure_rate.toFixed(1)}%`
                : "N/A"
            }
          />
        </div>
      </section>

      <div className="mt-12 flex flex-wrap gap-3">
        <button
          onClick={onRunAgain}
          className="rounded-full bg-black px-6 py-3 text-sm font-medium text-white"
        >
          Run again
        </button>

        <button
          onClick={onHome}
          className="rounded-full border border-black/15 px-6 py-3 text-sm font-medium"
        >
          Back home
        </button>
      </div>

      <p className="mt-8 max-w-2xl text-xs leading-5 text-black/40">
        Note: browser diagnostics measure the connection between
        your browser and the diagnostic server. They cannot directly
        inspect Wi-Fi adapter or router-level information.
      </p>
    </main>
  )
}