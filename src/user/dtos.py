from pydantic import BaseModel


class UserRegisterResponseBase(BaseModel):
    message:str
    username:str
    role:str
    

class UserRegisterBase(BaseModel):
    username: str
    email: str
    password: str
    name: str
    phone: str
    billing_address:str 
    shipping_address: str

class AdminRegisterBase(BaseModel):
    username:str
    email:str
    password:str
    

class UpdateUser(BaseModel):
    name:str
    phone:str  
    billing_address:str
    shipping_address:str




   

class LoginBase(BaseModel):
    username:str
    password:str


class UserAuthenticateResponseBase(BaseModel):
    message:str = f" is authenticated successfully"
    username:str
    role:str