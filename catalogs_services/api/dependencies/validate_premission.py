from fastapi import HTTPException, status


async def check_permission(
    permission_codes: dict,
    product_code: str,
) -> None:
    if product_code not in permission_codes:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No access for this operation",
        )
