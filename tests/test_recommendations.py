from app.diagnostics.models import NetworkEvidence
from app.diagnostics.recommendations import recommend


def test_normal_connection_recommendation():
    evidence = NetworkEvidence(
        router_reachable=True,
        internet_reachable=True,
        dns_working=True,
    )

    recommendation = recommend(
        "no_obvious_problem",
        evidence,
    )

    assert recommendation.title == "No network change is needed right now"


def test_internet_down_does_not_recommend_moving_closer():
    evidence = NetworkEvidence(
        router_reachable=True,
        internet_reachable=False,
        dns_working=False,
        router_packet_loss_percent=0.0,
    )

    recommendation = recommend(
        "internet_connection_problem",
        evidence,
    )

    text = " ".join(recommendation.steps).lower()

    assert "move closer" not in text
    assert "other device" in text


def test_high_local_packet_loss_gets_specific_action():
    evidence = NetworkEvidence(
        router_reachable=True,
        internet_reachable=True,
        dns_working=True,
        router_packet_loss_percent=15.0,
        router_latency_average_ms=30.0,
    )

    recommendation = recommend(
        "local_network_instability",
        evidence,
    )

    assert "losing packets" in recommendation.title.lower()


def test_high_local_latency_gets_local_recommendation():
    evidence = NetworkEvidence(
        router_reachable=True,
        internet_reachable=True,
        dns_working=True,
        router_packet_loss_percent=0.0,
        router_latency_average_ms=200.0,
    )

    recommendation = recommend(
        "high_latency",
        evidence,
    )

    assert "local connection" in recommendation.title.lower()


def test_internet_path_problem_mentions_isp_investigation():
    evidence = NetworkEvidence(
        router_reachable=True,
        internet_reachable=True,
        dns_working=True,
        router_packet_loss_percent=0.0,
        internet_packet_loss_percent=10.0,
    )

    recommendation = recommend(
        "internet_path_instability",
        evidence,
    )

    text = " ".join(recommendation.steps).lower()

    assert "isp" in text


def test_dns_problem_gets_dns_specific_action():
    evidence = NetworkEvidence(
        router_reachable=True,
        internet_reachable=True,
        dns_working=False,
    )

    recommendation = recommend(
        "dns_problem",
        evidence,
    )

    text = " ".join(recommendation.steps).lower()

    assert "dns" in text