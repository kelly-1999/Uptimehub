from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

from app.services.monitor_scheduler import (
    monitor_is_due,
    schedule_due_monitors,
)


def test_monitor_is_due_when_never_checked():
    monitor = SimpleNamespace(
        last_checked_at=None,
        interval_seconds=60,
    )

    now = datetime.now(UTC)

    assert monitor_is_due(monitor, now) is True


def test_monitor_is_due_when_interval_expired():
    now = datetime.now(UTC)

    monitor = SimpleNamespace(
        last_checked_at=now - timedelta(seconds=61),
        interval_seconds=60,
    )

    assert monitor_is_due(monitor, now) is True


def test_monitor_is_not_due_before_interval():
    now = datetime.now(UTC)

    monitor = SimpleNamespace(
        last_checked_at=now - timedelta(seconds=20),
        interval_seconds=60,
    )

    assert monitor_is_due(monitor, now) is False


def test_scheduler_enqueues_due_monitor(mocker):
    monitor = SimpleNamespace(
        id=1,
        name="Google",
        is_active=True,
        last_checked_at=None,
        interval_seconds=60,
    )

    db = mocker.MagicMock()
    db.scalars.return_value.all.return_value = [monitor]

    session_context = mocker.MagicMock()
    session_context.__enter__.return_value = db
    session_context.__exit__.return_value = False

    mocker.patch(
        "app.services.monitor_scheduler.SessionLocal",
        return_value=session_context,
    )

    acquire_lock = mocker.patch(
        "app.services.monitor_scheduler.acquire_monitor_lock",
        return_value=True,
    )

    enqueue = mocker.patch(
        "app.services.monitor_scheduler.enqueue_monitor_check"
    )

    schedule_due_monitors()

    acquire_lock.assert_called_once_with(1)
    enqueue.assert_called_once_with(1)


def test_scheduler_does_not_enqueue_when_locked(mocker):
    monitor = SimpleNamespace(
        id=1,
        name="Google",
        is_active=True,
        last_checked_at=None,
        interval_seconds=60,
    )

    db = mocker.MagicMock()
    db.scalars.return_value.all.return_value = [monitor]

    session_context = mocker.MagicMock()
    session_context.__enter__.return_value = db
    session_context.__exit__.return_value = False

    mocker.patch(
        "app.services.monitor_scheduler.SessionLocal",
        return_value=session_context,
    )

    mocker.patch(
        "app.services.monitor_scheduler.acquire_monitor_lock",
        return_value=False,
    )

    enqueue = mocker.patch(
        "app.services.monitor_scheduler.enqueue_monitor_check"
    )

    schedule_due_monitors()

    enqueue.assert_not_called()
