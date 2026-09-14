import json

from app.services.job_queue import (
    MONITOR_QUEUE,
    acquire_monitor_lock,
    enqueue_monitor_check,
    get_monitor_check_job,
    release_monitor_lock,
)


def test_acquire_monitor_lock_success(mocker):
    redis_mock = mocker.patch(
        "app.services.job_queue.redis_client"
    )

    redis_mock.set.return_value = True

    result = acquire_monitor_lock(10)

    assert result is True

    redis_mock.set.assert_called_once_with(
        "uptimehub:monitor-lock:10",
        "locked",
        nx=True,
        ex=120,
    )


def test_acquire_monitor_lock_already_exists(mocker):
    redis_mock = mocker.patch(
        "app.services.job_queue.redis_client"
    )

    redis_mock.set.return_value = None

    result = acquire_monitor_lock(10)

    assert result is False


def test_release_monitor_lock(mocker):
    redis_mock = mocker.patch(
        "app.services.job_queue.redis_client"
    )

    release_monitor_lock(10)

    redis_mock.delete.assert_called_once_with(
        "uptimehub:monitor-lock:10"
    )


def test_enqueue_monitor_check(mocker):
    redis_mock = mocker.patch(
        "app.services.job_queue.redis_client"
    )

    enqueue_monitor_check(5)

    expected_payload = json.dumps(
        {
            "monitor_id": 5,
        }
    )

    redis_mock.lpush.assert_called_once_with(
        MONITOR_QUEUE,
        expected_payload,
    )


def test_get_monitor_check_job(mocker):
    redis_mock = mocker.patch(
        "app.services.job_queue.redis_client"
    )

    redis_mock.brpop.return_value = (
        MONITOR_QUEUE,
        '{"monitor_id": 7}',
    )

    result = get_monitor_check_job()

    assert result == {
        "monitor_id": 7,
    }


def test_get_monitor_check_job_returns_none(mocker):
    redis_mock = mocker.patch(
        "app.services.job_queue.redis_client"
    )

    redis_mock.brpop.return_value = None

    result = get_monitor_check_job()

    assert result is None
