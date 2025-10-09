from prometheus_client import (
    Counter,
    Histogram,
    Gauge,
)

http_requests_total = Counter(
    "orders_requests_total",
    "Total number of HTTP requests",
    ["method", "path", "status"],
)

http_request_duration_seconds = Histogram(
    "orders_request_duration_seconds",
    "Duration of HTTP request in seconds",
    ["method", "path", "status"],
)

http_active_requests = Gauge(
    "orders_active_requests",
    "Number of active requests",
)
