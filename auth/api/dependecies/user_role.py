from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from fastapi import HTTPException, status

from api.dependecies.user_token import validate_payload
from core.model import User, Role, RolesPermission


async def user_role(
    session: AsyncSession,
    token: str,
):
    payload = await validate_payload(token=token)
    user_email = payload.get("sub")

    stmt = (
        select(User)
        .options(selectinload(User.role).selectinload(Role.permissions_helper).selectinload(RolesPermission.permission_r))
        .where(User.email == user_email)
    )

    result_user = await session.scalars(stmt)
    user = result_user.first()
    if not user or not user.role:
        raise HTTPException(status_code=404, detail="User or role not found")

    permissions_codes = {p.permission_r.code for p in user.role.permissions_helper}

    return permissions_codes
