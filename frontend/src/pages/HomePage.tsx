import { Feature } from "../components/Feature"

interface HomePageProps {
  onRunDiagnostic: () => void
}

export function HomePage({
  onRunDiagnostic,
}: HomePageProps) {
  return (
    <>
      <section className="mx-auto max-w-6xl px-6 pb-24 pt-24 md:pb-32 md:pt-32">
        <div className="max-w-3xl">
          <p className="mb-6 text-sm font-medium uppercase tracking-widest text-black/45">
            Home network diagnostics
          </p>

          <h1 className="text-5xl font-semibold tracking-[-0.04em] md:text-7xl">
            Stop guessing.
            <br />
            Find the problem.
          </h1>

          <p className="mt-8 max-w-xl text-lg leading-8 text-black/55">
            Run a simple connection diagnostic and get
            a clear explanation of what your network
            evidence shows.
          </p>

          <button
            onClick={onRunDiagnostic}
            className="mt-10 rounded-full bg-black px-7 py-3.5 text-sm font-medium text-white transition hover:bg-black/80"
          >
            Check my connection
          </button>
        </div>
      </section>

      <section className="border-y border-black/10">
        <div className="mx-auto grid max-w-6xl gap-10 px-6 py-16 md:grid-cols-3">
          <Feature
            number="01"
            title="Test"
            description="Collect measurable evidence from your browser instead of relying on guesses."
          />

          <Feature
            number="02"
            title="Understand"
            description="Turn raw network measurements into a simple diagnosis you can understand."
          />

          <Feature
            number="03"
            title="Act"
            description="Get a practical next step based on what the diagnostic actually found."
          />
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-6 py-24">
        <div className="grid gap-16 md:grid-cols-2 md:items-center">
          <div>
            <p className="text-sm font-medium uppercase tracking-widest text-black/40">
              Evidence first
            </p>

            <h2 className="mt-5 text-3xl font-semibold tracking-tight md:text-4xl">
              No technical knowledge required.
            </h2>

            <p className="mt-5 max-w-lg leading-7 text-black/55">
              The diagnostic collects network measurements,
              interprets them, and presents the result in
              plain language.
            </p>
          </div>

          <div className="rounded-2xl border border-black/10 bg-black p-6 text-white shadow-2xl shadow-black/10">
            <div className="flex items-center justify-between">
              <span className="text-sm text-white/50">
                Example result
              </span>

              <span className="rounded-full border border-white/15 px-3 py-1 text-xs text-white/60">
                Complete
              </span>
            </div>

            <h3 className="mt-10 text-2xl font-semibold">
              Your connection looks stable
            </h3>

            <p className="mt-3 text-sm leading-6 text-white/55">
              We did not detect significant connection
              failures, latency problems, or instability.
            </p>

            <div className="mt-8 grid grid-cols-2 gap-3">
              <div className="rounded-xl bg-white/10 p-4">
                <p className="text-xs text-white/40">
                  Success
                </p>
                <p className="mt-1 text-lg font-medium">
                  100%
                </p>
              </div>

              <div className="rounded-xl bg-white/10 p-4">
                <p className="text-xs text-white/40">
                  Jitter
                </p>
                <p className="mt-1 text-lg font-medium">
                  1.2 ms
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <footer className="border-t border-black/10">
        <div className="mx-auto max-w-6xl px-6 py-8 text-sm text-black/40">
          WiFi Diagnostic
        </div>
      </footer>
    </>
  )
}