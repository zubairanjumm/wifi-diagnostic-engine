import { Feature } from "../components/Feature"
import { WifiIcon } from "../components/WifiIcon"

const DOWNLOAD_URL =
  "https://github.com/zubairanjumm/wifi-diagnostic-engine/releases/download/v0.1.2/WiFiDiagnostic-v0.1.2.zip"

const features = [
  {
    number: "01",
    title: "Find local network problems",
    description:
      "Check the connection between your Windows PC, Wi-Fi adapter, and router to identify problems that browser tests cannot see.",
  },
  {
    number: "02",
    title: "Measure connection quality",
    description:
      "Analyze latency, jitter, packet loss, DNS behavior, and connectivity patterns to turn confusing symptoms into useful evidence.",
  },
  {
    number: "03",
    title: "Get a clear explanation",
    description:
      "The diagnostic engine turns technical network measurements into a simple report that tells you what is most likely wrong.",
  },
]

const checks = [
  "Wi-Fi adapter and local network connectivity",
  "Router reachability and response quality",
  "Internet-path stability",
  "DNS resolution",
  "Latency, jitter, and packet loss",
  "A downloadable diagnostic report",
]

export function HomePage() {
  return (
    <main className="min-h-screen overflow-hidden">
      <div className="hero-glow pointer-events-none fixed inset-0 -z-10" />

      <header className="mx-auto flex max-w-7xl items-center justify-between px-6 py-6 lg:px-10">
        <a href="#" className="flex items-center gap-3">
          <span className="brand-mark">
            <WifiIcon />
          </span>
          <span className="text-sm font-bold tracking-[-0.02em] text-white">
            WiFi Diagnostic Engine
          </span>
        </a>

        <span className="hidden rounded-full border border-white/10 bg-white/[0.04] px-4 py-2 text-xs font-medium tracking-[0.12em] text-slate-400 sm:block">
          WINDOWS NETWORK TOOL
        </span>
      </header>

      <section className="mx-auto max-w-7xl px-6 pb-24 pt-14 lg:px-10 lg:pb-32 lg:pt-24">
        <div className="grid items-center gap-14 lg:grid-cols-[1.1fr_0.9fr]">
          <div>
            <div className="eyebrow mb-7">
              <span className="eyebrow-dot" />
              Built for Windows
            </div>

            <h1 className="max-w-4xl text-5xl font-bold leading-[0.98] tracking-[-0.055em] text-white sm:text-6xl lg:text-8xl">
              Stop guessing.
              <span className="gradient-text block">Find the problem.</span>
            </h1>

            <p className="mt-8 max-w-2xl text-lg leading-8 text-slate-400 sm:text-xl">
              A local Windows network diagnostic tool that looks beyond a
              simple speed test. Find out whether the problem is your PC,
              Wi-Fi connection, router, DNS, or the wider internet path.
            </p>

            <div className="mt-10">
              <a
                href={DOWNLOAD_URL}
                className="download-button"
                download
              >
                <span className="download-icon" aria-hidden="true">
                  ↓
                </span>
                <span>
                  <strong>Download for Windows</strong>
                  <small>ZIP • v0.1.2</small>
                </span>
              </a>
            </div>

            <p className="mt-5 text-sm text-slate-500">
              Free to use • No account • Runs locally on Windows
            </p>
          </div>

          <div className="relative">
            <div className="dashboard-card">
              <div className="flex items-center justify-between border-b border-white/10 pb-5">
                <div>
                  <p className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">
                    Diagnostic engine
                  </p>
                  <p className="mt-1 text-lg font-semibold text-white">
                    Network health overview
                  </p>
                </div>
                <span className="status-pill">
                  <span className="status-dot" />
                  Local
                </span>
              </div>

              <div className="mt-7 space-y-3">
                <div className="metric-row">
                  <span>Router connection</span>
                  <strong>Stable</strong>
                </div>
                <div className="metric-row">
                  <span>Internet path</span>
                  <strong>Checked</strong>
                </div>
                <div className="metric-row">
                  <span>DNS resolution</span>
                  <strong>Healthy</strong>
                </div>
                <div className="metric-row">
                  <span>Packet loss</span>
                  <strong>Measured</strong>
                </div>
              </div>

              <div className="mt-7 rounded-2xl border border-cyan-400/15 bg-cyan-400/[0.06] p-5">
                <div className="flex items-center gap-3">
                  <span className="signal-bars">
                    <i />
                    <i />
                    <i />
                    <i />
                  </span>
                  <div>
                    <p className="text-xs uppercase tracking-[0.12em] text-cyan-300/70">
                      Evidence-based
                    </p>
                    <p className="mt-1 text-sm font-medium text-slate-200">
                      Multiple signals, one clear explanation
                    </p>
                  </div>
                </div>
              </div>
            </div>

            <div className="floating-card floating-card-top">
              <span className="mini-icon">01</span>
              <span>PC → Router</span>
            </div>

            <div className="floating-card floating-card-bottom">
              <span className="mini-icon">02</span>
              <span>Router → Internet</span>
            </div>
          </div>
        </div>
      </section>

      <section className="border-y border-white/[0.07] bg-white/[0.02]">
        <div className="mx-auto max-w-7xl px-6 py-20 lg:px-10 lg:py-24">
          <div className="grid gap-10 lg:grid-cols-[0.8fr_1.2fr]">
            <div>
              <p className="section-label">Why it exists</p>
              <h2 className="mt-4 max-w-xl text-3xl font-bold tracking-[-0.04em] text-white sm:text-5xl">
                Internet problems are rarely just “slow Wi-Fi.”
              </h2>
            </div>

            <p className="max-w-2xl self-end text-lg leading-8 text-slate-400">
              A speed test can tell you how fast a connection is at one
              moment. It cannot tell you where the failure is happening.
              WiFi Diagnostic Engine focuses on the local Windows machine and
              the network path around it, so you can investigate the actual
              source of the problem.
            </p>
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-6 py-24 lg:px-10 lg:py-32">
        <div className="mb-14 max-w-2xl">
          <p className="section-label">What it checks</p>
          <h2 className="mt-4 text-3xl font-bold tracking-[-0.04em] text-white sm:text-5xl">
            From your Windows machine outward.
          </h2>
        </div>

        <div className="grid gap-x-8 gap-y-12 md:grid-cols-3">
          {features.map((feature) => (
            <Feature key={feature.number} {...feature} />
          ))}
        </div>

        <div className="mt-20 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {checks.map((check, index) => (
            <div
              key={check}
              className="check-card"
            >
              <span>{String(index + 1).padStart(2, "0")}</span>
              <p>{check}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-6 pb-24 lg:px-10 lg:pb-32">
        <div className="cta-panel">
          <div>
            <p className="section-label">Ready when your connection isn't</p>
            <h2 className="mt-4 max-w-3xl text-3xl font-bold tracking-[-0.04em] text-white sm:text-5xl">
              Diagnose the network from the machine that is actually having
              the problem.
            </h2>
          </div>

          <div className="mt-10 flex flex-wrap gap-x-8 gap-y-3 text-sm text-slate-400">
            <span>Windows desktop</span>
            <span>Local diagnostics</span>
            <span>No account required</span>
            <span>Report generation</span>
          </div>
        </div>
      </section>

      <footer className="border-t border-white/[0.07]">
        <div className="mx-auto flex max-w-7xl flex-col gap-3 px-6 py-8 text-sm text-slate-500 sm:flex-row sm:items-center sm:justify-between lg:px-10">
          <p>WiFi Diagnostic Engine</p>
          <p>Windows network diagnostics without the guesswork.</p>
        </div>
      </footer>
    </main>
  )
}
