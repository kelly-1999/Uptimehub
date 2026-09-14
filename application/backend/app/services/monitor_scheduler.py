import logging
import time
from datetime import UTC, datetime, timedelta
from prometheus_client import start_http_server
from sqlalchemy import select
from app.core.metrics import (
    SCHEDULER_DUPLICATE_SKIPS_TOTAL,
    SCHEDULER_JOBS_QUEUED_TOTAL,
)


from app.core.database import SessionLocal
from app.core.logging import configure_logging
from app.models.monitor import Monitor
from app.services.job_queue import (
    acquire_monitor_lock,
    enqueue_monitor_check,
    release_monitor_lock,
)


configure_logging()

logger = logging.getLogger("uptimehub.scheduler")


SCHEDULER_INTERVAL_SECONDS = 5


def monitor_is_due(monitor: Monitor, now: datetime) -> bool:
    if monitor.last_checked_at is None:
        return True

    next_check_time = monitor.last_checked_at + timedelta(
        seconds=monitor.interval_seconds
    )

    return now >= next_check_time


def schedule_due_monitors() -> None:
    now = datetime.now(UTC)

    with SessionLocal() as db:
        statement = (
            select(Monitor)
            .where(Monitor.is_active.is_(True))
            .order_by(Monitor.id)
        )

        monitors = db.scalars(statement).all()

        for monitor in monitors:
            if not monitor_is_due(monitor, now):
                continue

            if not acquire_monitor_lock(monitor.id):
                logger.debug(
                    "monitor_already_queued monitor_id=%s",
                    monitor.id,
                )
                continue

            try:
                enqueue_monitor_check(monitor.id)
                SCHEDULER_JOBS_QUEUED_TOTAL.inc()
                logger.info(
                    "monitor_queued monitor_id=%s name=%s",
                    monitor.id,
                    monitor.name,
                )

            except Exception:
                release_monitor_lock(monitor.id)

                logger.exception(
                    "monitor_enqueue_failed monitor_id=%s",
                    monitor.id,
                )

                raise


def main() -> None:
    start_http_server(9102)

    logger.info(
        "scheduler_started "
        "polling_interval_seconds=%s "
        "metrics_port=9102",
        SCHEDULER_INTERVAL_SECONDS,
    )

    try:
        while True:
            schedule_due_monitors()
            time.sleep(SCHEDULER_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        logger.info("scheduler_stopped")

if __name__ == "__main__":
    main()
