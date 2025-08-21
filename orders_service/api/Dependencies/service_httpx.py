import httpx
from fastapi import HTTPException, status


async def query_result(url_data: str):
    """Получаем данные по url"""
    async with httpx.AsyncClient() as client:
        data_result = await client.get(url_data)
        try:
            data_result.raise_for_status()
        except httpx.HTTPStatusError as ex:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Invalid not found",
            ) from ex
        return data_result.json()


async def is_cast_present(
    url_service: str,
    cast_id: int,
):
    """Получаем данные по id"""
    id_url = f"{url_service}{cast_id}/"
    return await query_result(url_data=id_url)


async def is_cast_present_all(url_service: str):
    """Получаем полный список"""
    result_url = f"{url_service}"
    return await query_result(url_data=result_url)
