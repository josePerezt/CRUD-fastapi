from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import User
from schemas import UserCreate
from fastapi.security import OAuth2PasswordRequestForm

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
  
  async def get_user_by(self,form_data:OAuth2PasswordRequestForm,db:AsyncSession):

    query = select(User).filter_by(name = form_data.username,password = form_data.password)
    
    user_response = await db.execute(query)
    
    if  user_response is None:
      return None

    user_db = user_response.scalars().first()

    return  user_db
  

  async def get_user(self,user:str,db:AsyncSession):

    query = select(User).filter_by(user)
    
    user_response = await db.execute(query)
    
    if  user_response is None:
      return None

    user_db = user_response.scalars().first()

    return  user_db
  