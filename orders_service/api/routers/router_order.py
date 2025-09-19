from typing import Annotated
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status, Request

from api.CRUD.crud_order import get_order, create_order, update_order_by_id
from core.model import helper_db, Order
from core.schemas.schema_orders import OrderRead, OrderCreate, OrderUpdate

router = APIRouter(prefix="/orders", tags=["Order"])


@router.get(
    "/{order_id}/",
    response_model=OrderRead,
    status_code=status.HTTP_200_OK,
)
async def get_order_by_id(
    session: Annotated[AsyncSession, Depends(helper_db.session_getter)],
    order_id: UUID,
) -> Order:
    order = await get_order(session=session, order_id=order_id)
    return order


@router.post(
    "/",
    response_model=OrderRead,
    status_code=status.HTTP_200_OK,
)
async def create_new_order(
    request: Request,
    session: Annotated[AsyncSession, Depends(helper_db.session_getter)],
    data_order: OrderCreate,
) -> Order:
    order = await create_order(session=session, data_order=data_order, request=request)
    return order


@router.patch(
    "/{order_id}/",
    response_model=OrderRead,
    status_code=status.HTTP_200_OK,
)
async def update_order(
    session: Annotated[AsyncSession, Depends(helper_db.session_getter)],
    data_update: OrderUpdate,
    data_order: Order = Depends(get_order_by_id),
) -> OrderRead:
    result_update = await update_order_by_id(
        session=session,
        data_update=data_update,
        data_order=data_order,
        partial=True,
    )
    return OrderRead.model_validate(result_update)


@router.delete(
    "/{order_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_order(
    session: Annotated[AsyncSession, Depends(helper_db.session_getter)],
    data_order: Order = Depends(get_order_by_id),
) -> None:
    await session.delete(data_order)
    await session.commit()
