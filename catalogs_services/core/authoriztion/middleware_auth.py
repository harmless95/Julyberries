from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from fastapi import Request
import jwt

from core.config import setting


class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        unprotected_paths = ["/login", "/signup", "/open"]
        if request.url.path in unprotected_paths:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401, content={"detail": "Отсутствует токен авторизации"}
            )
        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(
                token,
                setting.auth_jwt.private_key_path,
                algorithms=[setting.auth_jwt.algorithm],
            )

            request.state.user = payload.get("sub")
        except jwt.ExpiredSignatureError:
            return JSONResponse(status_code=401, content={"detail": "Токен истек"})
        except jwt.InvalidTokenError:
            return JSONResponse(status_code=401, content={"detail": "Неверный токен"})

        response = await call_next(request)
        return response
