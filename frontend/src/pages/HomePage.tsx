import { Feature } from "../components/Feature"
import { WifiIcon } from "../components/WifiIcon"

const DOWNLOAD_URL =
  "https://github.com/zubairanjumm/wifi-diagnostic-engine/releases/download/v0.1.2/WiFiDiagnostic-v0.1.2.zip"

const features = [
  {
    number: "01",
    title: "Diagnose the local connection",
    description:
      "NetSense checks the Windows machine, Wi-Fi adapter, and router to identify problems that a normal browser speed test cannot see.",
  },
  {
    number: "02",
    title: "Measure the network path",
    description:
      "It evaluates latency, jitter, packet loss, DNS behavior, and connectivity patterns to determine where instability is occurring.",
  },
  {
    number: "03",
    title: "Explain what is wrong",
    description:
      "Instead of leaving you with raw numbers, NetSense turns the evidence into a clear diagnosis and a downloadable report.",
  },
]

const checks = [
  "Windows PC and Wi-Fi adapter connectivity",
  "Router reachability and response quality",
  "Internet-path stability and failures",
  "DNS resolution and connectivity",
  "Latency, jitter, and packet loss",
  "A clear downloadable diagnostic report",
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
            NetSense
          </span>
        </a>

        <span className="hidden rounded-full border border-white/10 bg-white/[0.04] px-4 py-2 text-xs font-medium tracking-[0.12em] text-slate-400 sm:block">
          WINDOWS NETWORK DIAGNOSTICS
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
              Know what's wrong.
              <span className="gradient-text block">Not just how fast.</span>
            </h1>

            <p className="mt-8 max-w-2xl text-lg leading-8 text-slate-400 sm:text-xl">
              <strong className="font-semibold text-slate-200">NetSense</strong>{" "}
              is a Windows network diagnostic tool that investigates the
              connection from your PC outward. It checks your local network,
              router, DNS, and internet path to help identify where the
              problem is actually happening.
            </p>

            <div className="mt-10 flex flex-wrap items-center gap-4">
              <a href={DOWNLOAD_URL} className="download-button" download>
                <span className="download-icon" aria-hidden="true">
                  ↓
                </span>
                <span>
                  <strong>Download for Windows</strong>
                  <small>ZIP • v0.1.2</small>
                </span>
              </a>

              <span className="live-badge">
                <span className="live-dot" />
                Local diagnostic engine
              </span>
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
                    NetSense
                  </p>
                  <p className="mt-1 text-lg font-semibold text-white">
                    Live network signals
                  </p>
                </div>
                <span className="status-pill">
                  <span className="status-dot" />
                  Monitoring
                </span>
              </div>

              <div className="network-visual">
                <div className="network-node">
                  <span className="node-icon">PC</span>
                  <small>Your PC</small>
                </div>
                <span className="network-line"><i /></span>
                <div className="network-node">
                  <span className="node-icon">R</span>
                  <small>Router</small>
                </div>
                <span className="network-line"><i /></span>
                <div className="network-node">
                  <span className="node-icon">W</span>
                  <small>Internet</small>
                </div>
              </div>

              <div className="mt-3 space-y-3">
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
                      Evidence-based diagnosis
                    </p>
                    <p className="mt-1 text-sm font-medium text-slate-200">
                      Multiple signals → one clear explanation
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
              <p className="section-label">What NetSense does</p>
              <h2 className="mt-4 max-w-xl text-3xl font-bold tracking-[-0.04em] text-white sm:text-5xl">
                A speed test tells you the result. NetSense investigates the
                reason.
              </h2>
            </div>

            <p className="max-w-2xl self-end text-lg leading-8 text-slate-400">
              When Wi-Fi feels slow, unstable, or randomly disconnects, the
              cause could be your computer, adapter, router, DNS, or the
              internet path. NetSense collects evidence from the Windows
              machine and compares multiple signals so you can understand
              where the connection is failing instead of guessing.
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
            <div key={check} className="check-card">
              <span>{String(index + 1).padStart(2, "0")}</span>
              <p>{check}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-6 pb-24 lg:px-10 lg:pb-32">
        <div className="cta-panel">
          <div>
            <p className="section-label">Start with the machine having the problem</p>
            <h2 className="mt-4 max-w-3xl text-3xl font-bold tracking-[-0.04em] text-white sm:text-5xl">
              Download NetSense and turn network symptoms into evidence.
            </h2>
          </div>

          <div className="mt-10 flex flex-wrap gap-x-8 gap-y-3 text-sm text-slate-400">
            <span>Windows desktop</span>
            <span>Local diagnostics</span>
            <span>No account required</span>
            <span>Diagnostic report</span>
          </div>
        </div>
      </section>

      <footer className="border-t border-white/[0.07]">
        <div className="mx-auto flex max-w-7xl flex-col gap-3 px-6 py-8 text-sm text-slate-500 sm:flex-row sm:items-center sm:justify-between lg:px-10">
          <p>NetSense</p>
          <p>Windows network diagnostics without the guesswork.</p>
        </div>
      </footer>
    </main>
  )
}
