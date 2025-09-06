import httpx
from fastapi import HTTPException, status


async def permission_product(token: str, product_code: str):
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(
            "http://app_auth:8000/auth/permission_check/",
            json={"token": token, "code": product_code},
        )
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
        result_permission = response.json()
        if not result_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="not enough rights"
            )
        return result_permission
