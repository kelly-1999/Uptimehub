from types import SimpleNamespace

import httpx

from app.services.monitor_checker import check_monitor


def test_check_monitor_up(mocker):
    monitor = SimpleNamespace(
        url="https://example.com",
        current_status="unknown",
        last_http_status=None,
        last_response_time_ms=None,
        last_checked_at=None,
    )

    mock_response = SimpleNamespace(
        status_code=200,
    )

    mocker.patch(
        "app.services.monitor_checker.httpx.get",
        return_value=mock_response,
    )

    result = check_monitor(monitor)

    assert result.current_status == "up"
    assert result.last_http_status == 200
    assert result.last_response_time_ms is not None
    assert result.last_checked_at is not None


def test_check_monitor_down_on_http_error(mocker):
    monitor = SimpleNamespace(
        url="https://example.com",
        current_status="unknown",
        last_http_status=None,
        last_response_time_ms=None,
        last_checked_at=None,
    )

    mock_response = SimpleNamespace(
        status_code=500,
    )

    mocker.patch(
        "app.services.monitor_checker.httpx.get",
        return_value=mock_response,
    )

    result = check_monitor(monitor)

    assert result.current_status == "down"
    assert result.last_http_status == 500
    assert result.last_response_time_ms is not None
    assert result.last_checked_at is not None


def test_check_monitor_down_on_request_error(mocker):
    monitor = SimpleNamespace(
        url="https://does-not-exist.invalid",
        current_status="unknown",
        last_http_status=None,
        last_response_time_ms=None,
        last_checked_at=None,
    )

    mocker.patch(
        "app.services.monitor_checker.httpx.get",
        side_effect=httpx.RequestError("Connection failed"),
    )

    result = check_monitor(monitor)

    assert result.current_status == "down"
    assert result.last_http_status is None
    assert result.last_response_time_ms is not None
    assert result.last_checked_at is not None
