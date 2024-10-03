from pydantic import BaseModel,Field
from typing import Optional

class UserBase(BaseModel):
  """Modelo base para los datos del usuario."""
  name: str
  email:str
  
class UserCreate(UserBase):
  """Modelo para crear un nuevo usuario."""
  password:str = Field(...,min_length=8)
  
class UserUpdate(UserBase):
  """Modelo para actualizar los datos de un usuario."""
  password: Optional[str] = Field(None,min_length=8)
  
class UserResponse(UserBase):
  """Modelo de respuesta que incluye campos adicionales para el usuario."""
  id:int
  is_active: bool
  
  class Config:
    orm_mode : True