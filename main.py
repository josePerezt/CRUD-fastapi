from fastapi import FastAPI,Depends,HTTPException
from fastapi.responses import JSONResponse
from schemas import UserResponse,UserCreate
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from CRUD import CRUD

crud = CRUD()

app = FastAPI(
  title="Login",
  description="This is a project of login",
  docs_url="/"
)


@app.get("/users",tags=["Login"],response_model=list[UserResponse])
async def get_user(db:AsyncSession = Depends(get_db)):
    db_users = await crud.get_all_user(db)
    if not db_users:
         raise HTTPException(status_code=404, detail="there are no registered users")
    return db_users
  
@app.post("/users/register", tags=["Login"], response_model=UserResponse)
async def create_user(user :UserCreate,db:AsyncSession = Depends(get_db)):
  db_user = await crud.create_user(user,db)

  if db_user is None:
    raise HTTPException(status_code=400,detail="the name or email is already registered")
  
  return JSONResponse(status_code=200,content={"message":"User create successfully"})