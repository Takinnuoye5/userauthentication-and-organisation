import logging
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from my_authentication_app.model import user as user_model
from my_authentication_app.schema.user import UserCreate
from my_authentication_app.utils import hash_password, verify_password, create_access_token, verify_token
from uuid import uuid4
from datetime import timedelta
import os

logger = logging.getLogger(__name__)

def create_user(user: UserCreate, db: Session):
    logger.info(f"Creating user with email: {user.email}")
    hashed_password = hash_password(user.password)
    db_user = user_model.User(
        userId=str(uuid4()),
        firstName=user.firstName,
        lastName=user.lastName,
        email=user.email,
        password=hashed_password,
        phone=user.phone,
    )
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
        logger.info(f"User created with email: {user.email}")
    except IntegrityError as e:
        db.rollback()
        if isinstance(e.orig, UniqueViolation):
            logger.error(f"IntegrityError: Email {user.email} already registered.")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Email {user.email} already registered."
            )
        logger.error(f"IntegrityError: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error during registration: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error: {str(e)}"
        )
    return db_user

def authenticate_user(email: str, password: str, db: Session):
    logger.info(f"Authenticating user with email: {email}")
    user = db.query(user_model.User).filter(user_model.User.email == email).first()
    if user is None:
        logger.warning(f"User not found with email: {email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_password(password, user.password):
        logger.warning(f"Password verification failed for user: {email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    logger.info(f"Authentication successful for user: {email}")
    return user
