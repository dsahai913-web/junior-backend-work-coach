import os
from dotenv import load_dotenv
from jose import jwt
from fastapi import Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer
from core.database import get_db
from models.user import User
from sqlalchemy.orm import Session

load_dotenv()

SECRET_KEY=os.getenv("JWT_SECRET_KEY")
ALGORITHM=os.getenv("JWT_ALGORITHM")

oauth2_scheme=OAuth2PasswordBearer(
    tokenUrl="/users/login"
)

def create_access_token(user_id:int):
    payload={
        "sub":str(user_id)
    }
    token=jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return token

def get_current_user(
        token:str=Depends(oauth2_scheme),
        db:Session=Depends(get_db)
):
    try:
        payload=jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        user_id=payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token",
            )
        user=db.query(User).filter(User.id==int(user_id)).first()
        if user is None:
            raise HTTPException(
                status_code=404,
                detail="User not found",
            )
        return user
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )