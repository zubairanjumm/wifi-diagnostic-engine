from numbers import Real


def validate_browser_evidence(data: dict) -> dict:
    """Validate and normalize evidence collected by the browser."""

    if not isinstance(data, dict):
        raise TypeError("Browser evidence must be a dictionary.")

    validated = {}

    boolean_fields = [
        "https_reachable",
    ]

    integer_fields = [
        "request_count",
        "successful_request_count",
        "failed_request_count",
    ]

    percentage_fields = [
        "request_success_rate",
        "request_failure_rate",
    ]

    latency_fields = [
        "browser_latency_min_ms",
        "browser_latency_average_ms",
        "browser_latency_median_ms",
        "browser_latency_p95_ms",
        "browser_latency_max_ms",
        "browser_latency_jitter_ms",
    ]

    speed_fields = [
        "download_mbps",
        "upload_mbps",
    ]

    for field in boolean_fields:
        value = data.get(field)

        if value is not None and not isinstance(value, bool):
            raise ValueError(
                f"{field} must be a boolean or None."
            )

        validated[field] = value

    for field in integer_fields:
        value = data.get(field, 0)

        if (
            not isinstance(value, int)
            or isinstance(value, bool)
        ):
            raise ValueError(
                f"{field} must be an integer."
            )

        if value < 0:
            raise ValueError(
                f"{field} cannot be negative."
            )

        validated[field] = value

    for field in percentage_fields:
        value = data.get(field)

        if value is not None:
            if (
                not isinstance(value, Real)
                or isinstance(value, bool)
            ):
                raise ValueError(
                    f"{field} must be a number or None."
                )

            if not 0 <= value <= 100:
                raise ValueError(
                    f"{field} must be between 0 and 100."
                )

            value = float(value)

        validated[field] = value

    for field in latency_fields:
        value = data.get(field)

        if value is not None:
            if (
                not isinstance(value, Real)
                or isinstance(value, bool)
            ):
                raise ValueError(
                    f"{field} must be a number or None."
                )

            if value < 0:
                raise ValueError(
                    f"{field} cannot be negative."
                )

            value = float(value)

        validated[field] = value

    for field in speed_fields:
        value = data.get(field)

        if value is not None:
            if (
                not isinstance(value, Real)
                or isinstance(value, bool)
            ):
                raise ValueError(
                    f"{field} must be a number or None."
                )

            if value < 0:
                raise ValueError(
                    f"{field} cannot be negative."
                )

            value = float(value)

        validated[field] = value

    return validated