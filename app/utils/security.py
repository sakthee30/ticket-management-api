from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError

# configure Argon2
pwd_context = CryptContext(schemes=["argon2"],deprecated="auto")

# hash password (used during signup)
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# verify password (used during login)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# JWT settings
SECRET_KEY = "your_secret_key_here"  
ALGORITHM = "HS256"
# Token valid for 30 mins
ACCESS_TOKEN_EXPIRE_MINUTES = 30  

# Create JWT token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

# Verify JWT token
def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # returns the decoded payload if valid
        return payload  
    except JWTError:
        return None

#verifies user login authentication
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# This tells FastAPI: token comes from Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )

    return user_id