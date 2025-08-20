from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.CRUD.crud_category import (
    all_categories,
    get_category,
    create_category,
    update_category,
)
from core.config import setting
from core.model import helper_db, Category
from core.schemas.schema_category import CategoryRead, CategoryCreate, CategoryUpdate

router = APIRouter(
    prefix=setting.api.prefix,
    tags=[setting.api.tags],
)


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


@router.post(
    "/",
    response_model=CategoryRead,
    status_code=status.HTTP_200_OK,
)
async def create_new_category(
    session: Annotated[AsyncSession, Depends(helper_db.session_getter)],
    data_category: CategoryCreate,
) -> Category:
    category = await create_category(
        session=session,
        data_category=data_category,
    )
    return category


@router.put(
    "/{category_id}/",
    response_model=CategoryRead,
    status_code=status.HTTP_200_OK,
)
async def update_category_by_id(
    session: Annotated[AsyncSession, Depends(helper_db.session_getter)],
    data_update: CategoryUpdate,
    category_id: Category = Depends(get_category_by_id),
) -> Category:
    category = await update_category(
        session=session,
        data_update=data_update,
        category=category_id,
    )
    return category


@router.delete(
    "/{category_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_category(
    session: Annotated[AsyncSession, Depends(helper_db.session_getter)],
    category_id: Category = Depends(get_category_by_id),
) -> None:
    await session.delete(category_id)
    await session.commit()
