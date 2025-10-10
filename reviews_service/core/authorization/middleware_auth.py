from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from fastapi import HTTPException, status
import httpx


class MiddlewareAuth(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        if request.url.path in ["/metrics", "/docs", "/openapi.json"]:
            return await call_next(request)
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized",
            )
        token = auth_header.split(" ")[1]
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(
                "http://app_auth:8000/auth/verify_token/",
                json={"token": token},
            )
            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token",
                )
            user_data = response.json()
            request.state.user = user_data
            response = await call_next(request)
            return response
