import httpx
from fastapi import HTTPException, status, Request


async def query_result(
    request: Request,
    url_data: str,
):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing",
        )
    """Получаем данные по url"""
    async with httpx.AsyncClient() as client:
        data_result = await client.get(url_data, headers={"Authorization": auth_header})
        try:
            data_result.raise_for_status()
        except httpx.HTTPStatusError as ex:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Invalid not found",
            ) from ex
        return data_result.json()


async def is_cast_present_all(
    url_service: str,
    request: Request,
):
    """Получаем полный список"""
    result_url = f"{url_service}"
    return await query_result(url_data=result_url, request=request)
