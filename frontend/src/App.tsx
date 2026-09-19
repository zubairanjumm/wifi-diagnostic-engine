import { useState } from "react"

import { collectBrowserEvidence } from "./diagnostics/browser"
import { diagnoseBrowserEvidence } from "./api/diagnosticApi"

import { Header } from "./components/Header"

import { HomePage } from "./pages/HomePage"
import { DiagnosticPage } from "./pages/DiagnosticPage"
import { ResultPage } from "./pages/ResultPage"

import type {
  BrowserEvidence,
  DiagnosticResponse,
} from "./types/diagnostic"

type Page =
  | "home"
  | "diagnostic"
  | "result"

function App() {
  const [page, setPage] = useState<Page>("home")
  const [evidence, setEvidence] =
    useState<BrowserEvidence | null>(null)
  const [result, setResult] =
    useState<DiagnosticResponse | null>(null)
  const [error, setError] =
    useState<string | null>(null)

  async function runDiagnostic() {
    setPage("diagnostic")
    setError(null)
    setEvidence(null)
    setResult(null)

    try {
      const endpoint =
        `${import.meta.env.VITE_API_URL}/api/diagnostic-test`

      const browserEvidence =
        await collectBrowserEvidence(endpoint)

      setEvidence(browserEvidence)

      const diagnosticResult =
        await diagnoseBrowserEvidence(
          browserEvidence,
        )

      setResult(diagnosticResult)
      setPage("result")
    } catch {
      setError(
        "Failed to complete the diagnostic.",
      )
    }
  }

  function goHome() {
    setPage("home")
    setError(null)
  }

  return (
    <div className="min-h-screen bg-white text-black">
      <Header
        onRunDiagnostic={runDiagnostic}
      />

      {page === "home" && (
        <HomePage
          onRunDiagnostic={runDiagnostic}
        />
      )}

      {page === "diagnostic" && (
        <DiagnosticPage
          error={error}
          onRetry={runDiagnostic}
        />
      )}

      {page === "result" &&
        evidence &&
        result && (
          <ResultPage
            evidence={evidence}
            result={result}
            onRunAgain={runDiagnostic}
            onHome={goHome}
          />
        )}
    </div>
  )
}

export default App