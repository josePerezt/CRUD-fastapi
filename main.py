from fastapi import FastAPI,Depends,HTTPException
from typing import Annotated
from fastapi.responses import JSONResponse
from schemas import UserResponse,UserCreate
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from db import get_db
from CRUD import CRUD
from jose import jwt, JWTError
from dotenv import load_dotenv
import os

load_dotenv()


crud = CRUD()
oauth2_scheme= OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI(
  title="Login",
  description="This is a project of login",
  docs_url="/"
)

# generar token
def encode_token(payload:dict)->str:
  secret_key = os.getenv("SECRET_KEY")
  algorithm = os.getenv("ALGORITHMS")
  token = jwt.encode(payload,secret_key,algorithm=algorithm)
  
  return token

# decodificar token
def decode_token(token:Annotated[str,Depends(oauth2_scheme)])->dict:
  print(token)
  secret_key = os.getenv("SECRET_KEY")
  algorithm = os.getenv("ALGORITHMS")
  
  try:
    data = jwt.decode(token,secret_key,algorithm=[algorithm])
    return data
  except JWTError:
    raise HTTPException(
      status_code=401,
      detail="token invalid or expired",
      headers={"WWW-Authenticate":"Bearer"}
    )

  
# Ruta para registrar un nuevo usuario 
@app.post("/users/register", tags=["Login"], response_model=UserResponse)
async def create_user(user :UserCreate,db:AsyncSession = Depends(get_db)):
  db_user = await crud.create_user(user,db)

  if db_user is None:
    raise HTTPException(status_code=400,detail="the name or email is already registered")
  
  return JSONResponse(status_code=200,content={"message":"User create successfully"})

# ruta para generar token de usuario login
@app.post("/token",tags=["Login"])
async def login(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],db:AsyncSession=Depends(get_db)):
  
  user_data = await crud.get_user_by(form_data,db)
  
  if user_data is None:
    raise HTTPException(status_code=404,detail="username or password are invalid")
  
  token = encode_token({"username": user_data.name, "email":user_data.email})
  
  return {"access_token":token}

# ruta protegida para probar el token
@app.get("/users/profile",tags=["profile"])
async def profile(my_user:Annotated[dict,Depends(decode_token)]):
  return my_user

# ruta para obtener todos los datos de mi base de datos de usuarios
@app.get("/users",tags=["Login"],response_model=list[UserResponse])
async def get_user(db:AsyncSession = Depends(get_db)):
    db_users = await crud.get_all_user(db)
    if not db_users:
         raise HTTPException(status_code=404, detail="there are no registered users")
    return db_users
