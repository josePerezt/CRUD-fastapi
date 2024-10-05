from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from models import User
from schemas import UserCreate

class CRUD:
  async def get_all_user(self,db:AsyncSession):
    query = select(User)
    users = await db.execute(query)
    if not users:
      return []
    return users.scalars().all()
    
  async def create_user(self, user:UserCreate,db:AsyncSession):
    db_user = User(name= user.name, email=user.email, password= user.password)
    
    existing_user = await db.execute(select(User).filter((User.name == user.name) | (User.email == user.email)))
    
    existe = existing_user.scalars().first()
    
    if existe :
      return None
    
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
