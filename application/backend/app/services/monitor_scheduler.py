import time
from datetime import UTC, datetime, timedelta

from sqlalchemy import select

from app.core.database import SessionLocal
from app.models.monitor import Monitor
from app.services.job_queue import (
    acquire_monitor_lock,
    enqueue_monitor_check,
    release_monitor_lock,
)


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
                print(
                    f"[SCHEDULER] Monitor "
                    f"id={monitor.id} "
                    f"already queued or processing."
                )
                continue

            try:
                enqueue_monitor_check(monitor.id)

                print(
                    f"[SCHEDULER] Queued monitor "
                    f"id={monitor.id} "
                    f"name={monitor.name}"
                )

            except Exception:
                release_monitor_lock(monitor.id)
                raise


def main() -> None:
    print("[SCHEDULER] UptimeHub scheduler started.")

    try:
        while True:
            schedule_due_monitors()
            time.sleep(SCHEDULER_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        print("\n[SCHEDULER] Scheduler stopped.")


if __name__ == "__main__":
    main()
