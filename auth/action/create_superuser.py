import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


from core.model import User, Role, db_helper
from utils.jwt_validate import hash_password

data_superuser = {
    "email": "admin@example.com",
    "password": "admin",
    "name": "admin",
}


async def create_super_user(session: AsyncSession):
    stmt = select(User).where(User.email == data_superuser.get("email"))
    result = await session.scalars(stmt)
    user = result.first()
    if user:
        print(f"Пользователь {data_superuser['email']} уже существует.")
        return
    stmt_role = select(Role).where(Role.name == data_superuser.get("name"))
    result_role = await session.scalars(stmt_role)
    role = result_role.first()
    if not role:
        print(f"Роль '{data_superuser['name']}' не найдена.")
        return
    password = data_superuser.get("password")
    hash_bytes = hash_password(password)
    hex_hash = hash_bytes.hex()
    user = User(
        email=data_superuser.get("email"),
        hashed_password=hex_hash,
        name=data_superuser.get("name"),
        role_id=role.id,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    print(f"Пользователь {user.email} успешно создан.")


async def main():
    async for session in db_helper.helper_db.session_getter():
        await create_super_user(session=session)


if __name__ == "__main__":
    asyncio.run(main())
