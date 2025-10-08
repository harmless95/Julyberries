import time
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from utils.metrics import (
    http_requests_total,
    http_active_requests,
    http_request_duration_seconds,
)


class PrometheusMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        http_active_requests.inc()
        start_time = time.time()

        response = await call_next(request)

        resp_time = time.time() - start_time
        http_active_requests.dec()

        http_requests_total.labels(
            method=request.method,
            path=request.url.path,
            status=str(response.status_code),
        ).inc()

        http_request_duration_seconds.labels(
            method=request.method,
            path=request.url.path,
            status=str(response.status_code),
        ).observe(resp_time)

        return response
