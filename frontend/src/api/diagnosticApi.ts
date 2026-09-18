import type { BrowserEvidence } from "../types/diagnostic"

interface DiagnosticResponse {
  diagnosis: string
}

export async function diagnoseBrowserEvidence(
  evidence: BrowserEvidence,
): Promise<DiagnosticResponse> {
  const response = await fetch("http://127.0.0.1:8000/api/diagnose", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(evidence),
  })

  if (!response.ok) {
    throw new Error("Diagnostic request failed.")
  }

  return response.json()
}