from fastapi import FastAPI
import logging
from fastapi.exceptions import RequestValidationError
from my_authentication_app.database import engine
from my_authentication_app.router import auth, organization, user
from my_authentication_app.database import Base
from my_authentication_app.exceptions import validation_exception_handler
from my_authentication_app.middleware.auth import OAuth2Middleware

from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_exception_handler(RequestValidationError, validation_exception_handler)

app.add_middleware(OAuth2Middleware)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(organization.router, prefix="/api/organizations", tags=["organizations"])
app.include_router(user.router, prefix="/api/users", tags=["users"])

@app.get("/")
def home():
    return {"message": "Welcome to the HNG Stage 2 Authentication App"}
