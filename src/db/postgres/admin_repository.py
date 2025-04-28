from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Admin


class AdminRepository:
    db_model = Admin

    async def get_by_email(self, email: str, session: AsyncSession) -> Admin | None:
        try:
            query = select(self.db_model).where(self.db_model.email == email).limit(1)
            result = await session.execute(query)
            admin = result.scalar()
        except Exception as error:
            await session.rollback()
            raise error

        return admin if admin else None


def get_admin_repository() -> AdminRepository:
    return AdminRepository()
