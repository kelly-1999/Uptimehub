from prometheus_client import Counter, Gauge, Histogram


HTTP_REQUESTS_TOTAL = Counter(
    "uptimehub_http_requests_total",
    "Total number of HTTP requests received by the API",
    ["method", "path", "status_code"],
)


HTTP_REQUEST_DURATION_SECONDS = Histogram(
    "uptimehub_http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "path"],
)


MONITOR_CHECKS_TOTAL = Counter(
    "uptimehub_monitor_checks_total",
    "Total number of monitor checks performed",
    ["status"],
)


MONITOR_CHECK_FAILURES_TOTAL = Counter(
    "uptimehub_monitor_check_failures_total",
    "Total number of monitor checks that failed unexpectedly",
)


MONITOR_RESPONSE_TIME_SECONDS = Histogram(
    "uptimehub_monitor_response_time_seconds",
    "Response time of monitored websites in seconds",
)


MONITOR_QUEUE_SIZE = Gauge(
    "uptimehub_monitor_queue_size",
    "Current number of jobs waiting in the Redis monitor queue",
)


SCHEDULER_JOBS_QUEUED_TOTAL = Counter(
    "uptimehub_scheduler_jobs_queued_total",
    "Total number of monitor jobs queued by the scheduler",
)


SCHEDULER_DUPLICATE_SKIPS_TOTAL = Counter(
    "uptimehub_scheduler_duplicate_skips_total",
    "Total number of duplicate jobs prevented by Redis locks",
)
