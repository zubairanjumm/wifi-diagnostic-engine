type HomePageProps = {
  onRunDiagnostic: () => void
}

export function HomePage({ onRunDiagnostic }: HomePageProps) {
  return (
    <main className="min-h-[calc(100vh-72px)]">
      <section className="mx-auto flex max-w-6xl flex-col items-center px-6 py-24 text-center">
        <div className="max-w-3xl">
          <p className="mb-4 text-sm font-medium uppercase tracking-[0.2em] text-gray-500">
            WiFi Diagnostic Engine
          </p>

          <h1 className="text-5xl font-semibold tracking-tight md:text-6xl">
            Stop guessing.
            <br />
            Find the problem.
          </h1>

          <p className="mx-auto mt-6 max-w-2xl text-lg leading-8 text-gray-600">
            Test your connection and get a clear explanation of what may be
            causing your network problems.
          </p>

          <div className="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row">
            <button
              onClick={onRunDiagnostic}
              className="rounded-xl bg-black px-7 py-3.5 text-sm font-medium text-white transition hover:bg-gray-800"
            >
              Run Browser Diagnostic
            </button>

            <a
              href="https://github.com/zubairanjumm/wifi-diagnostic-engine/releases/tag/v0.1.2"
              target="_blank"
              rel="noopener noreferrer"
              className="rounded-xl border border-gray-300 bg-white px-7 py-3.5 text-sm font-medium text-black transition hover:bg-gray-50"
            >
              Download Windows App
            </a>
          </div>

          <p className="mt-5 text-sm text-gray-500">
            Browser diagnostic requires no installation. The Windows app
            provides deeper local network diagnostics.
          </p>
        </div>
      </section>
    </main>
  )
}
