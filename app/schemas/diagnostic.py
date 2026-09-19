from pydantic import BaseModel, Field


class BrowserEvidenceRequest(BaseModel):
    https_reachable: bool | None = None

    request_success_rate: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    request_failure_rate: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    browser_latency_min_ms: float | None = Field(
        default=None,
        ge=0,
    )

    browser_latency_average_ms: float | None = Field(
        default=None,
        ge=0,
    )

    browser_latency_max_ms: float | None = Field(
        default=None,
        ge=0,
    )

    browser_latency_jitter_ms: float | None = Field(
        default=None,
        ge=0,
    )

    download_mbps: float | None = Field(
        default=None,
        ge=0,
    )

    upload_mbps: float | None = Field(
        default=None,
        ge=0,
    )

class DiagnosticResponse(BaseModel):
    diagnosis: str
    title: str
    message: str
    next_action: str