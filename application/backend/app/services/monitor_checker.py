import time
from datetime import UTC, datetime

import httpx

from app.models.monitor import Monitor


def check_monitor(monitor: Monitor) -> Monitor:
    start_time = time.perf_counter()

    try:
        response = httpx.get(
            monitor.url,
            timeout=10.0,
            follow_redirects=True,
        )

        elapsed = time.perf_counter() - start_time
        response_time_ms = int(elapsed * 1000)

        monitor.last_http_status = response.status_code
        monitor.last_response_time_ms = response_time_ms
        monitor.last_checked_at = datetime.now(UTC)

        if 200 <= response.status_code < 400:
            monitor.current_status = "up"
        else:
            monitor.current_status = "down"

    except httpx.RequestError:
        elapsed = time.perf_counter() - start_time
        response_time_ms = int(elapsed * 1000)

        monitor.current_status = "down"
        monitor.last_http_status = None
        monitor.last_response_time_ms = response_time_ms
        monitor.last_checked_at = datetime.now(UTC)

    return monitor
