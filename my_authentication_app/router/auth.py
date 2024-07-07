from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from my_authentication_app.database import get_db
from my_authentication_app.schema import user as user_schema
from my_authentication_app.service import auth as auth_service
from my_authentication_app.service import organization as org_service
from my_authentication_app.dependencies import get_current_user
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/login", response_model=user_schema.LoginResponse)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    logger.info(f"Login attempt for {form_data.username}")
    try:
        db_user = auth_service.authenticate_user(form_data.username, form_data.password, db)
        if not db_user:
            logger.error(f"Invalid credentials for {form_data.username}")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        token = auth_service.create_access_token({"sub": db_user.email})
        logger.info(f"Created token for {db_user.email}: {token}")
        return {
            "status": "success",
            "message": "Login successful",
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "userId": db_user.userId,
                "firstName": db_user.firstName,
                "lastName": db_user.lastName,
                "email": db_user.email,
                "phone": db_user.phone,
            }
        }
    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.post("/register")
def register_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    logger.info(f"Registration attempt for {user.email}")
    try:
        db_user = auth_service.create_user(user, db)
        organization_name = f"{user.firstName}'s Organization"
        org_data = org_service.OrganizationCreate(name=organization_name)
        org_service.create_organization(org_data, db_user.userId, db)
        access_token = auth_service.create_access_token({"sub": user.email})
        logger.info(f"Created token for {user.email}: {access_token}")
        return {
            "status": "success",
            "message": "Registration successful",
            "data": {
                "access_token": access_token,
                "token_type": "bearer",
                "user": {
                    "userId": db_user.userId,
                    "firstName": db_user.firstName,
                    "lastName": db_user.lastName,
                    "email": db_user.email,
                    "phone": db_user.phone,
                }
            }
        }
    except HTTPException as e:
        logger.error(f"Error during registration: {e.detail}")
        raise e
    except IntegrityError as e:
        db.rollback()
        if isinstance(e.orig, UniqueViolation):
            logger.error(f"Email {user.email} already registered.")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Email {user.email} already registered."
            )
    except Exception as e:
        logger.error(f"Unexpected error during registration: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/users/me", response_model=user_schema.User)
def read_users_me(current_user: user_schema.User = Depends(get_current_user)):
    return current_user
