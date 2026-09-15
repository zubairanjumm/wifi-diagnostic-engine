from app.network.connectivity import (
    get_default_gateway,
    measure_ping,
)


def test_get_default_gateway():
    gateway = get_default_gateway()

    assert gateway is None or isinstance(gateway, str)


def test_measure_ping():
    gateway = get_default_gateway()

    if gateway is None:
        return

    stats = measure_ping(gateway, count=2)

    assert stats is not None
    assert 0 <= stats.packet_loss_percent <= 100

    if stats.min_ms is not None:
        assert stats.min_ms >= 0

    if stats.average_ms is not None:
        assert stats.average_ms >= 0

    if stats.max_ms is not None:
        assert stats.max_ms >= 0

    if stats.jitter_ms is not None:
        assert stats.jitter_ms >= 0


def test_ping_latency_order():
    gateway = get_default_gateway()

    if gateway is None:
        return

    stats = measure_ping(gateway, count=4)

    if stats is None:
        return

    if stats.min_ms is not None and stats.average_ms is not None:
        assert stats.min_ms <= stats.average_ms

    if stats.average_ms is not None and stats.max_ms is not None:
        assert stats.average_ms <= stats.max_ms

    if (
        stats.min_ms is not None
        and stats.max_ms is not None
        and stats.jitter_ms is not None
    ):
        assert stats.jitter_ms == stats.max_ms - stats.min_ms
