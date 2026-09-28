from src.user.dtos import LoginBase,UserRegisterBase,AdminRegisterBase,UpdateUser
from sqlalchemy.orm import Session
from src.utils.db import get_db
from src.user.models import User
from fastapi import HTTPException,status,Depends
from pwdlib import PasswordHash
import jwt
from src.utils.settings import settings
from datetime import datetime,timedelta,timezone


password_hash=PasswordHash.recommended()


def get_password_hash(password):
    return password_hash.hash(password)

def verify_password(plain_password,hashed_password):
    return password_hash.verify(plain_password,hashed_password)

def userRegister(body:UserRegisterBase, db:Session):

    existing_user = db.query(User).filter(User.username == body.username).first()

    if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Username {body.username} already exists."
            )

    existing_email = db.query(User).filter(User.email == body.email).first()

    if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Email {body.email} already exists."
            )

    exist_phone=db.query(User).filter(User.phone==body.phone).first()

    if exist_phone:
          raise HTTPException(status_code=404,detail=f"User with phone number {body.phone} already exist")
    hash_password = get_password_hash(body.password)

    new_user = User(
            name=body.name,
            phone=body.phone,
            billing_address=body.billing_address,
            shipping_address=body.shipping_address,
            username=body.username,
            email=body.email,
            password=hash_password,
            role="user"
        )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
            "message":"Register Successful",
            "username":new_user.username,
            "role":new_user.role
            }


def adminRegister(body:AdminRegisterBase, db:Session):
        existing_admin = db.query(User).filter(User.username == body.username).first()

        if existing_admin:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f" username {body.username} already exists")
        existing_email = db.query(User).filter(User.email == body.email).first()
        
        if existing_email:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Email {body.email} already exists")

        hash_password = get_password_hash(body.password)

        new_admin = User(username=body.username,email=body.email,password=hash_password,role="admin")

        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)

        return {
            "message": " Register successfully",
            "username": new_admin.username,
            "role": new_admin.role
        }

def login_user(body: LoginBase, db: Session):

    user = db.query(User).filter(User.email == body.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong email"
        )

    if not verify_password(body.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong password"
        )

    # Mark user as active
   

    db.commit()
    db.refresh(user)

    exp_time = datetime.now() + timedelta( hours=settings.EXP_TIME)

    token = jwt.encode(
        {"_id": user.id,"role": user.role,"exp": exp_time.timestamp()},settings.SECRET_KEY,algorithm=settings.ALGORITHM)

    return {
        # "message": "Login successful",
        "email": user.email,
        "username": user.username,
        "token": token,
    }

# get user profile
def get_user(user:User):
      return {
            "message":f"Date Fetched of user:    {user.username} ",
            "name":user.name,
            "phone":user.phone,
            "billing_address":user.billing_address,
            "shipping_address":user.shipping_address
      }


#update user profile
def update_user(body: UpdateUser,db: Session,user: User):
    data = body.model_dump()

    for field, value in data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return {
            "message":f"Date Updated of user:    {user.username} ",
            "name":user.name,
            "phone":user.phone,
            "billing_address":user.billing_address,
            "shipping_address":user.shipping_address
    }