from sqlalchemy.orm import sessionmaker
from my_authentication_app.model import User
from my_authentication_app.database import engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_user():
    db = SessionLocal()
    try:
        db_user = User(
            userId="test_user_id",
            firstName="Test",
            lastName="User",
            email="test.user@example.com",
            password="hashed_password",
            phone="1234567890",
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        print(f"User created with email: {db_user.email}")
    finally:
        db.close()

if __name__ == "__main__":
    create_user()
