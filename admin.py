import getpass

from src.utils.db import SessionLocal
from src.user.models import User
from src.user.controller import get_password_hash


db = SessionLocal()


username = input("Enter username: ")
email = input("Enter email: ")
password = getpass.getpass("Enter password: ")


existing_admin = db.query(User).filter(User.username == username).first()

if existing_admin:
    print(f"Username {username} already exists.")
    db.close()
    exit()


existing_email = db.query(User).filter(User.email == email).first()

if existing_email:
    print(f"Email {email} already exists.")
    db.close()
    exit()


new_admin = User(
    username=username,
    email=email,
    password=get_password_hash(password),
    role="admin"
)


db.add(new_admin)
db.commit()
db.refresh(new_admin)


print("Admin created successfully.")
print("Username:", new_admin.username)
print("Email:", new_admin.email)
print("Role:", new_admin.role)


db.close()