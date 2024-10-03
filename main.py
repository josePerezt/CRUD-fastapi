from fastapi import FastAPI,Depends
from schemas import UserResponse
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from CRUD import CRUD

crud = CRUD()

app = FastAPI(
  title="Login",
  description="This is a project of login",
  docs_url="/"
)


@app.get("/Users",tags=["Login"],response_model=list[UserResponse])
async def get_user(db:AsyncSession = Depends(get_db)):
  
  db_users = await crud.get_all_user(db)
  
  return db_users