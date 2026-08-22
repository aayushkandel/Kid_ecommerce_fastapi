from fastapi import HTTPException,Request,status,Depends
from src.utils.settings import settings
from src.utils.db import get_db
from sqlalchemy.orm import Session
import jwt
from jwt.exceptions import InvalidTokenError
from src.user.models import User   

def is_authenticated(request:Request,db:Session=Depends(get_db)):
 try:
    token=request.headers.get("authorization")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are unauthorized")

    token=token.split(" ")[-1]

    data=jwt.decode(token,settings.SECRET_KEY,settings.ALGORITHM)
    user_id=data.get("_id")
    

    user=db.query(User).filter(User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are unauthorized")
    
    return user
 except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are unauthorized")



#for admin Authentication for product crud

def is_admin_authenticated(request: Request):
    

    try:
        token = request.    headers.get("authorization")

        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="admin is unauthorized"
            )

        token = token.split(" ")[-1]

        data = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        if data.get("username") != "admin":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="admin is unauthorized"
            )

        if data.get("role") != "admin":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="admin is unauthorized"
            )

        return data

    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="admin is unauthorized"
        )