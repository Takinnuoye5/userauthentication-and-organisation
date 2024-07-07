import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from my_authentication_app.main import app
from my_authentication_app.database import Base, get_db
import os
from dotenv import load_dotenv
from alembic import command
from alembic.config import Config

load_dotenv()

DATABASE_URL_TEST = os.getenv("DATABASE_URL_TEST")

# Setup the test database
engine_test = create_engine(DATABASE_URL_TEST)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

@pytest.fixture(scope="function")
def db_session():
    # Setup Alembic configuration for test database
    alembic_cfg = Config("alembic_test.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", DATABASE_URL_TEST)
    command.upgrade(alembic_cfg, "head")
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Clean up after tests
        Base.metadata.drop_all(bind=engine_test)
        Base.metadata.create_all(bind=engine_test)

@pytest_asyncio.fixture(scope="function")
async def client(db_session):
    def override_get_db():
        try:
            db = db_session
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client
