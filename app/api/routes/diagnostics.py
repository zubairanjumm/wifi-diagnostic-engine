from fastapi import APIRouter
import time
from app.diagnostics.models import NetworkEvidence
from app.diagnostics.rules import diagnose
from app.schemas.diagnostic import (
    BrowserEvidenceRequest,
    DiagnosticResponse,
)
from app.diagnostics.explanations import explain_diagnosis
router = APIRouter()

@router.post("/diagnose", response_model=DiagnosticResponse)
def diagnose_browser_evidence(
    evidence: BrowserEvidenceRequest,
) -> DiagnosticResponse:
    network_evidence = NetworkEvidence(
        https_reachable=evidence.https_reachable,
        request_success_rate=evidence.request_success_rate,
        request_failure_rate=evidence.request_failure_rate,
        browser_latency_min_ms=evidence.browser_latency_min_ms,
        browser_latency_average_ms=evidence.browser_latency_average_ms,
        browser_latency_max_ms=evidence.browser_latency_max_ms,
        browser_latency_jitter_ms=evidence.browser_latency_jitter_ms,
        download_mbps=evidence.download_mbps,
        upload_mbps=evidence.upload_mbps,
    )
    
    result = diagnose(network_evidence)
    explanation = explain_diagnosis(result)

    return DiagnosticResponse(
        diagnosis=result,
        title=explanation.title,
        message=explanation.message,
        next_action=explanation.next_action,
    )


@router.get("/diagnostic-test")
def diagnostic_test():
    return {
        "status": "ok",
        "timestamp": time.time(),
    }