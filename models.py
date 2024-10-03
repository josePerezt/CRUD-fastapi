from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import Integer,String,Boolean
from db import BASE


class User(BASE):
  __tablename__="user"
  
  id : Mapped[int] = mapped_column(Integer,primary_key = True)
  name: Mapped[str] = mapped_column(String(40),nullable = False)
  email: Mapped[str] = mapped_column(String(255),nullable = False, unique= True)
  password : Mapped[str] = mapped_column(String(255), nullable = False)
  is_active: Mapped[bool] = mapped_column(Boolean,default=True)
  
  def __repr__(self)-> str:
    return f"name: {self.name}"