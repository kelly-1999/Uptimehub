import logging

from prometheus_client import start_http_server
from app.core.database import SessionLocal
from app.core.logging import configure_logging
from app.models.monitor import Monitor
from app.services.job_queue import (
    get_monitor_check_job,
    release_monitor_lock,
)
from app.services.monitor_checker import check_monitor


configure_logging()

logger = logging.getLogger("uptimehub.worker")


def process_monitor_job(monitor_id: int) -> None:
    try:
        with SessionLocal() as db:
            monitor = db.get(Monitor, monitor_id)

            if monitor is None:
                logger.warning(
                    "monitor_not_found monitor_id=%s",
                    monitor_id,
                )
                return

            if not monitor.is_active:
                logger.info(
                    "monitor_inactive monitor_id=%s",
                    monitor_id,
                )
                return

            logger.info(
                "monitor_check_started "
                "monitor_id=%s name=%s url=%s",
                monitor.id,
                monitor.name,
                monitor.url,
            )

            try:
                check_monitor(monitor)

                db.commit()
                db.refresh(monitor)

                logger.info(
                    "monitor_check_completed "
                    "monitor_id=%s "
                    "status=%s "
                    "http_status=%s "
                    "response_time_ms=%s",
                    monitor.id,
                    monitor.current_status,
                    monitor.last_http_status,
                    monitor.last_response_time_ms,
                )

            except Exception:
                db.rollback()

                logger.exception(
                    "monitor_check_failed monitor_id=%s",
                    monitor_id,
                )

    finally:
        release_monitor_lock(monitor_id)


def main() -> None:
    start_http_server(9101)

    logger.info(
        "worker_started metrics_port=9101"
    )

    try:
        while True:
            job = get_monitor_check_job()

            if job is None:
                continue

            monitor_id = job.get("monitor_id")

            if monitor_id is None:
                logger.warning(
                    "invalid_job_received job=%s",
                    job,
                )
                continue

            process_monitor_job(monitor_id)

    except KeyboardInterrupt:
        logger.info("worker_stopped")


if __name__ == "__main__":
    main()
