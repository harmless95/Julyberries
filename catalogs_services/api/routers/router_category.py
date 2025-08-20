from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.CRUD.crud_category import all_categories, get_category
from core.model import helper_db, Category
from core.schemas.schema_category import CategoryRead

router = APIRouter(prefix="/categories", tags=["Category"])


@router.get(
    "/",
    response_model=list[CategoryRead],
    status_code=status.HTTP_200_OK,
)
async def get_all_categories(
    session: Annotated[AsyncSession, Depends(helper_db.session_getter)],
) -> list[CategoryRead]:
    categories = await all_categories(session=session)
    return [CategoryRead.model_validate(category) for category in categories]


@router.get(
    "/{category_id}/",
    response_model=CategoryRead,
    status_code=status.HTTP_200_OK,
)
async def get_category_by_id(
    session: Annotated[AsyncSession, Depends(helper_db.session_getter)],
    category_id: int,
) -> Category:
    category = await get_category(
        session=session,
        category_id=category_id,
    )
    return category
