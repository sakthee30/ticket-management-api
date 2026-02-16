from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.utils.security import hash_password

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

#Signup
@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(user: UserCreate, db: Session = Depends(get_db)):

    # 1. Check if email already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # 2. Hash password
    hashed_pwd = hash_password(user.password)

    # 3. Create User model object
    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_pwd
    )

    # 4. Save to DB
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

#Login API Authentication with JWT
from app.schemas.user import UserLogin
from app.utils.security import verify_password, create_access_token
from datetime import timedelta
from fastapi import status
from app.utils.jwt import get_current_user

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    #Check if user exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid email or password")
    
    #Verify password
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid email or password")
    
    #Create JWT token
    access_token_expires = timedelta(minutes=30)  # token valid for 30 mins
    token = create_access_token(
        data={
            "user_id": db_user.id,
            "role": db_user.role 
            }, expires_delta=access_token_expires)

    #Return token
    return {
        "access_token": token,
        "token_type": "bearer",  # standard
        "user": {
            "id": db_user.id,
            "name": db_user.name,
            "email": db_user.email
        }
    }

@router.get("/profile")
def get_profile(current_user: User = Depends(get_current_user)):
    return {
        "message": "You are authenticated",
        "user_id": current_user.id,
        "email": current_user.email
    }