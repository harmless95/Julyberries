from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from fastapi import Request, HTTPException
import logging
import traceback


class ExceptionHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except HTTPException as http_exc:
            return JSONResponse(
                status_code=http_exc.status_code, content={"detail": http_exc.detail}
            )
        except Exception as exc:
            logging.error(f"Unexpected error: {traceback.format_exc()}")
            return JSONResponse(
                status_code=500, content={"detail": "Internal server error"}
            )
