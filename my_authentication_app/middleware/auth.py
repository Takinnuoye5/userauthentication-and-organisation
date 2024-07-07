from fastapi import Request, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from starlette.middleware.base import BaseHTTPMiddleware
from jose import JWTError, jwt
from my_authentication_app.database import get_db
from my_authentication_app.model.user import User
import os
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

class OAuth2Middleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        public_routes = ["/auth/login", "/auth/register", "/"]
        if any(request.url.path.startswith(route) for route in public_routes):
            response = await call_next(request)
            return response

        token = await oauth2_scheme(request)
        if not token:
            logger.error("Token not found in request")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                logger.error("Email not found in token payload")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        except JWTError as e:
            logger.error(f"JWT Error: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        db: Session = next(get_db())
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            logger.error("User not found in database")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        request.state.user = user
        response = await call_next(request)
        return response
