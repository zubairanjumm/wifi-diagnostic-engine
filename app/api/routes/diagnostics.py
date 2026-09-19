import time

from fastapi import APIRouter, Request
from fastapi.responses import Response

from app.diagnostics.explanations import explain_diagnosis
from app.diagnostics.models import NetworkEvidence
from app.diagnostics.rules import diagnose
from app.schemas.diagnostic import (
    BrowserEvidenceRequest,
    DiagnosticResponse,
)

router = APIRouter()


@router.post(
    "/diagnose",
    response_model=DiagnosticResponse,
)
def diagnose_browser_evidence(
    evidence: BrowserEvidenceRequest,
) -> DiagnosticResponse:
    network_evidence = NetworkEvidence(
        https_reachable=evidence.https_reachable,
        request_count=evidence.request_count,
        successful_request_count=evidence.successful_request_count,
        failed_request_count=evidence.failed_request_count,
        request_success_rate=evidence.request_success_rate,
        request_failure_rate=evidence.request_failure_rate,
        browser_latency_min_ms=evidence.browser_latency_min_ms,
        browser_latency_average_ms=evidence.browser_latency_average_ms,
        browser_latency_median_ms=evidence.browser_latency_median_ms,
        browser_latency_p95_ms=evidence.browser_latency_p95_ms,
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


@router.get("/speed/download")
def download_test(size_mb: int = 3):
    size_mb = max(1, min(size_mb, 10))

    payload = b"0" * (
        size_mb * 1024 * 1024
    )

    return Response(
        content=payload,
        media_type="application/octet-stream",
        headers={
            "Cache-Control": "no-store",
            "Content-Length": str(len(payload)),
        },
    )


@router.post("/speed/upload")
async def upload_test(request: Request):
    await request.body()

    return {
        "status": "ok",
        "timestamp": time.time(),
    }