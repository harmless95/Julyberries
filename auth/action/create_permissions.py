import asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from core.model import Permission, db_helper

DEFAULT_PERMISSIONS = {
    "product.create": "Добавление нового ассортимента",
    "product.read": "Просмотр доступных продуктов",
    "product.update": "Обновление ассортимента продуктов",
    "product.delete": "Удаление продукта из списка доступных",
}


async def add_permissions(session: AsyncSession):
    permissions = [
        Permission(code=name, description=DEFAULT_PERMISSIONS[name])
        for name in DEFAULT_PERMISSIONS
    ]
    session.add_all(permissions)
    await session.commit()


async def main():
    async for session in db_helper.helper_db.session_getter():
        await add_permissions(session=session)


if __name__ == "__main__":
    asyncio.run(main())
