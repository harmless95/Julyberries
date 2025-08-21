from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status

from api.CRUD.crud_order import get_order, create_order
from core.model import helper_db, Order
from core.schemas.schema_orders import OrderRead, OrderCreate

router = APIRouter(prefix="/orders", tags=["Order"])


@router.get(
    "/{order_id}/",
    response_model=OrderRead,
    status_code=status.HTTP_200_OK,
)
async def get_order_by_id(
    session: Annotated[AsyncSession, Depends(helper_db.session_getter)],
    order_id: int,
) -> Order:
    order = await get_order(session=session, order_id=order_id)
    return order


@router.post(
    "/",
    response_model=OrderRead,
    status_code=status.HTTP_200_OK,
)
async def create_new_order(
    session: Annotated[AsyncSession, Depends(helper_db.session_getter)],
    data_order: OrderCreate,
) -> Order:
    order = await create_order(session=session, data_order=data_order)
    return order
