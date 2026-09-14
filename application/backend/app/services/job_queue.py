import json

from redis.exceptions import TimeoutError as RedisTimeoutError

from app.core.redis import redis_client


MONITOR_QUEUE = "uptimehub:monitor-checks"
MONITOR_LOCK_PREFIX = "uptimehub:monitor-lock"
JOB_LOCK_TTL_SECONDS = 120


def get_monitor_lock_key(monitor_id: int) -> str:
    return f"{MONITOR_LOCK_PREFIX}:{monitor_id}"


def acquire_monitor_lock(monitor_id: int) -> bool:
    lock_key = get_monitor_lock_key(monitor_id)

    acquired = redis_client.set(
        lock_key,
        "locked",
        nx=True,
        ex=JOB_LOCK_TTL_SECONDS,
    )

    return bool(acquired)


def release_monitor_lock(monitor_id: int) -> None:
    lock_key = get_monitor_lock_key(monitor_id)

    redis_client.delete(lock_key)


def enqueue_monitor_check(monitor_id: int) -> None:
    job = {
        "monitor_id": monitor_id,
    }

    redis_client.lpush(
        MONITOR_QUEUE,
        json.dumps(job),
    )


def get_monitor_check_job(timeout: int = 5) -> dict | None:
    try:
        result = redis_client.brpop(
            MONITOR_QUEUE,
            timeout=timeout,
        )
    except RedisTimeoutError:
        return None

    if result is None:
        return None

    _, payload = result

    return json.loads(payload)
