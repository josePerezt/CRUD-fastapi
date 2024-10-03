from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import User


class CRUD:
  async def get_all_user(db:AsyncSession):
    query = select(User)
    result = await db.execute(query)
    return result
    


