import type {
  BrowserEvidence,
  DiagnosticResponse,
} from "../types/diagnostic"

const API_URL = import.meta.env.VITE_API_URL

export async function diagnoseBrowserEvidence(
  evidence: BrowserEvidence,
): Promise<DiagnosticResponse> {
  const response = await fetch(
    `${API_URL}/api/diagnose`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(evidence),
    },
  )

  if (!response.ok) {
    throw new Error("Diagnostic request failed.")
  }

  return response.json()
}