from fastapi import APIRouter, Depends,status,Request
from src.user import controller
from src.user.dtos import LoginBase,UserRegisterBase,AdminRegisterBase,UpdateUser,UserRegisterResponseBase,UserAuthenticateResponseBase
from src.utils.db import get_db
from src.user.is_auth import is_authenticated
from sqlalchemy.orm import Session
from src.user.models import User
from src.user import is_auth



user_router=APIRouter(prefix="/users")


@user_router.post("/user_register",response_model=UserRegisterResponseBase ,status_code=status.HTTP_201_CREATED)
def register(body:UserRegisterBase,db:Session=Depends(get_db)):
    return controller.userRegister(body,db)

@user_router.post("/admin_register",response_model=UserRegisterResponseBase,status_code=status.HTTP_201_CREATED)
def register(body:AdminRegisterBase,db:Session=Depends(get_db)):
    return controller.adminRegister(body,db)

@user_router.post("/login",status_code=200)
def login(body:LoginBase,db:Session= Depends(get_db)):
    return controller.login_user(body,db)

@user_router.get("/is_auth",response_model=UserAuthenticateResponseBase,status_code=status.HTTP_200_OK)
def user_authenticate(request:Request, db:Session = Depends(get_db)):
    return is_auth.is_authenticated(request,db)

@user_router.get("/is_admin_auth",response_model=UserAuthenticateResponseBase,status_code=status.HTTP_200_OK)
def admin_authenticate(request:Request, db:Session = Depends(get_db)):
    return is_auth.is_admin_authenticated(request,db)

@user_router.put("/update_user",status_code=status.HTTP_201_CREATED)
def update_user(body:UpdateUser,db:Session=Depends(get_db),user:User=Depends(is_authenticated)):
    return controller.update_user(body,db,user)

@user_router.get("/user_profile",status_code=status.HTTP_200_OK)
def get_user_profile(user:User=Depends(is_authenticated)):
    return controller.get_user(user)