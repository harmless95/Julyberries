from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
import httpx
import logging

log = logging.getLogger(__name__)


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized",
            )
        token = auth_header.split(" ")[1]
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(
                "http://app_auth:8000/auth/verify_token/", json={"token": token}
            )
            log.warning("Status code: %s", response.status_code)
            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token",
                )
            user_info = response.json()
            log.warning("Data user %s", user_info)
        request.state.user = user_info
        response = await call_next(request)
        return response
