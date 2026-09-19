interface HeaderProps {
  onRunDiagnostic: () => void
}

export function Header({
  onRunDiagnostic,
}: HeaderProps) {
  return (
    <header className="border-b border-black/10">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-5">
        <div className="flex items-center gap-3">
          <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-black">
            <WifiIcon />
          </div>

          <span className="text-sm font-semibold tracking-tight">
            WiFi Diagnostic
          </span>
        </div>

        <button
          onClick={onRunDiagnostic}
          className="rounded-full bg-black px-5 py-2.5 text-sm font-medium text-white transition hover:bg-black/80"
        >
          Run diagnostic
        </button>
      </div>
    </header>
  )
}

function WifiIcon() {
  return (
    <svg
      width="18"
      height="18"
      viewBox="0 0 24 24"
      fill="none"
      stroke="white"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M5 13a10 10 0 0 1 14 0" />
      <path d="M8 16a6 6 0 0 1 8 0" />
      <path d="M11 19a2 2 0 0 1 2 0" />
    </svg>
  )
}