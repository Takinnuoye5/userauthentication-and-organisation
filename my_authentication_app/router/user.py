from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from my_authentication_app.database import get_db
from my_authentication_app.schema import user as user_schema
from my_authentication_app.model import User
from my_authentication_app.dependencies import get_current_user
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/{id}", response_model=user_schema.UserResponse)
def get_user(id: str, current_user: user_schema.User = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.userId == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if user.userId != current_user.userId:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this user")
    return {
        "status": "success",
        "message": "User fetched successfully",
        "data": user
    }
