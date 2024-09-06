
from typing import Annotated
from fastapi import security
from fastapi.security import HTTPAuthorizationCredentials
import jwt
from src import  dto, models
from src.auth_bearer import JWTBearer
from src.config import JWT_SECRET_KEY
from src.utils import ALGORITHM, create_access_token, create_refresh_token, verify_password, get_hashed_password
from src.dependencies import SessionDependency
from fastapi import APIRouter, Depends, HTTPException, Request


router = APIRouter(
    prefix="/users", #..the prefix must not include a final /.
    tags=["users"],
    responses={404: {"description": "Not found"}}
)


@router.get('/getusers',)
def getusers(db: SessionDependency, dependencies=Depends(JWTBearer())):
    users = db.query(models.UserAccount).all()
    return users

@router.post('/login' ,response_model=dto.TokenSchema)
def login(request: dto.requestdetails, db: SessionDependency):
    user = db.query(models.UserAccount).filter(models.UserAccount.email == request.email).first()
    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect email")
    hashed_pass = user.password
    if not verify_password(request.password, hashed_pass):
        raise HTTPException(
            status_code=400,
            detail="Incorrect password"
        )

    access=create_access_token(user.user_account_id)
    refresh = create_refresh_token(user.user_account_id)

    token_db = models.TokenTable(user_id=user.user_account_id,  access_toke=access,  refresh_toke=refresh, status=True)
    db.add(token_db)
    db.commit()
    db.refresh(token_db)
    return {
        "user_id": user.user_account_id,
        "access_token": access,
        "refresh_token": refresh,
    }

@router.post("/register")
def register_user(user: dto.UserCreate, db: SessionDependency):
    existing_user = db.query(models.UserAccount).filter_by(email=user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    encrypted_password = get_hashed_password(user.password)

    user_account = models.UserAccount()
    user_account.email = user.email
    user_account.user_type_id = models.UserTypeValue.Patient
    user_account.password = encrypted_password
    db.add(user_account)
    db.commit()
    return {"message":"user created successfully"}

@router.post('/change-password')
def change_password(request: dto.changepassword, db: SessionDependency):
    user = db.query(models.UserAccount).filter(models.UserAccount.email == request.email).first()
    if user is None:
        raise HTTPException(status_code=400, detail="User not found")

    if not verify_password(request.old_password, user.password):
        raise HTTPException(status_code=400, detail="Invalid old password")
    
    encrypted_password = get_hashed_password(request.new_password)
    user.password = encrypted_password
    db.commit()
    
    return {"message": "Password changed successfully"}


