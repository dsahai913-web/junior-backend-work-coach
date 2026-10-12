from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session

from core.database import get_db
from schemas.user import UserCreate,UserLogin
from services.user_service import create_user,login_user
from core.security import get_current_user
from models.user import User
from fastapi.security import OAuth2PasswordRequestForm


router=APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.post("/register")
def register_user(user_data:UserCreate,db:Session=Depends(get_db)):
    new_user=create_user(db,user_data)
    return {
        "message":"user registered",
        "user_id":new_user.id,
        "name":new_user.name,
        "email":new_user.email,
    }

@router.post("/login")
def login(
        form_data:OAuth2PasswordRequestForm=Depends(),
        db:Session=Depends(get_db)
):
    access_token=login_user(db,form_data.username,form_data.password)
    return{
        "message":"Login successful",
        "access_token":access_token,
        "token_type":"bearer",

    }

@router.get("/me")
def get_my_profile(
        current_user:User=Depends(get_current_user),
):
    return{
        "id":current_user.id,
        "name":current_user.name,
        "email":current_user.email,
        "role":current_user.role,
    }

