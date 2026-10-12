from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate,UserLogin
from core.security import create_access_token

pwd_context=CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def create_user(db:Session,user_data:UserCreate):
    hashed_password=pwd_context.hash(user_data.password)
    new_user=User(
        name=user_data.name,
        email=user_data.email,
        password_hash=hashed_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def login_user(db:Session,email:str,password:str):
    user=db.query(User).filter(User.email==email).first()
    if user is None:
        raise HTTPException(status_code=401,detail="Invalid email or password")
    password_correct=pwd_context.verify(password,user.password_hash)
    if not password_correct:
        raise HTTPException(status_code=401,detail="Invalid email or password")
    access_token=create_access_token(user.id)
    return access_token
