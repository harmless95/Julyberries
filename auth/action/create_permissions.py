import asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from core.model import Permission, db_helper, Role, RolesPermission

perms = {
    "product.create": "Добавление нового ассортимента",
    "product.read": "Просмотр доступных продуктов",
    "product.update": "Обновление ассортимента продуктов",
    "product.delete": "Удаление продукта из списка доступных",
}

roles_data = {
    "user": {
        "description": "Обычный пользователь",
        "permissions": ["product.read"],
    },
    "manager": {
        "description": "Менеджер",
        "permissions": ["product.read", "product.update"],
    },
    "admin": {
        "description": "Администратор",
        "permissions": [
            "product.read",
            "product.update",
            "product.create",
            "product.delete",
        ],
    },
}


async def add_permissions(session: AsyncSession):
    dict_roles = {}
    for role_name, role_info in roles_data.items():
        role = Role(name=role_name, description=role_info["description"])
        session.add(role)
        dict_roles[role_name] = role

    dict_permission = {}
    for code, description_code in perms.items():
        permission = Permission(code=code, description=description_code)
        session.add(permission)
        dict_permission[code] = permission

    await session.flush()

    roles_permission = []
    for role_name, role_info in roles_data.items():
        object_role = dict_roles[role_name]
        for code_per in role_info["permissions"]:
            object_perm = dict_permission[code_per]
            roles_permission.append(
                RolesPermission(roles_id=object_role.id, permission_id=object_perm.id)
            )

    session.add_all(roles_permission)
    await session.commit()


async def main():
    async for session in db_helper.helper_db.session_getter():
        await add_permissions(session=session)


if __name__ == "__main__":
    asyncio.run(main())
