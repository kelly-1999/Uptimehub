import time
from datetime import UTC, datetime, timedelta

from sqlalchemy import select

from app.core.database import SessionLocal
from app.models.monitor import Monitor
from app.services.monitor_checker import check_monitor


POLL_INTERVAL_SECONDS = 5


def monitor_is_due(monitor: Monitor, now: datetime) -> bool:
    """
    Determine whether a monitor should be checked.

    A monitor is due when:
    - it has never been checked, or
    - enough time has passed since its previous check.
    """

    if monitor.last_checked_at is None:
        return True

    next_check_time = monitor.last_checked_at + timedelta(
        seconds=monitor.interval_seconds
    )

    return now >= next_check_time


def run_check_cycle() -> None:
    """
    Load active monitors from PostgreSQL and check
    any monitors whose interval has expired.
    """

    now = datetime.now(UTC)

    with SessionLocal() as db:
        statement = (
            select(Monitor)
            .where(Monitor.is_active.is_(True))
            .order_by(Monitor.id)
        )

        monitors = db.scalars(statement).all()

        if not monitors:
            print("[WORKER] No active monitors found.")
            return

        for monitor in monitors:
            if not monitor_is_due(monitor, now):
                continue

            print(
                f"[WORKER] Checking monitor "
                f"id={monitor.id} "
                f"name={monitor.name} "
                f"url={monitor.url}"
            )

            try:
                check_monitor(monitor)

                db.commit()
                db.refresh(monitor)

                print(
                    f"[WORKER] Result "
                    f"id={monitor.id} "
                    f"status={monitor.current_status} "
                    f"http={monitor.last_http_status} "
                    f"response_time={monitor.last_response_time_ms}ms"
                )

            except Exception as exc:
                db.rollback()

                print(
                    f"[WORKER] Error checking "
                    f"monitor id={monitor.id}: {exc}"
                )


def main() -> None:
    print("[WORKER] UptimeHub monitoring worker started.")
    print(
        f"[WORKER] Polling database every "
        f"{POLL_INTERVAL_SECONDS} seconds."
    )

    try:
        while True:
            run_check_cycle()
            time.sleep(POLL_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        print("\n[WORKER] Worker stopped.")


if __name__ == "__main__":
    main()
