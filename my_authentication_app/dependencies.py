from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from my_authentication_app.database import get_db
from my_authentication_app.model.user import User
import os
import logging

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

logger = logging.getLogger(__name__)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            logger.error("Email in token payload is None")
            raise credentials_exception
        logger.info(f"Token payload: {payload}")
    except JWTError as e:
        logger.error(f"JWTError during token verification: {e}")
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        logger.error(f"User not found with email: {email}")
        raise credentials_exception
    logger.info(f"Current user: {user.email}")
    return user
