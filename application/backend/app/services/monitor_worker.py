from app.core.database import SessionLocal
from app.models.monitor import Monitor
from app.services.job_queue import get_monitor_check_job
from app.services.monitor_checker import check_monitor


def process_monitor_job(monitor_id: int) -> None:
    with SessionLocal() as db:
        monitor = db.get(Monitor, monitor_id)

        if monitor is None:
            print(
                f"[WORKER] Monitor id={monitor_id} "
                f"does not exist."
            )
            return

        if not monitor.is_active:
            print(
                f"[WORKER] Monitor id={monitor_id} "
                f"is inactive. Skipping."
            )
            return

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
                f"[WORKER] Error processing "
                f"monitor id={monitor_id}: {exc}"
            )


def main() -> None:
    print("[WORKER] UptimeHub queue worker started.")

    try:
        while True:
            job = get_monitor_check_job()

            if job is None:
                continue

            monitor_id = job.get("monitor_id")

            if monitor_id is None:
                print("[WORKER] Invalid job received.")
                continue

            process_monitor_job(monitor_id)

    except KeyboardInterrupt:
        print("\n[WORKER] Worker stopped.")


if __name__ == "__main__":
    main()
