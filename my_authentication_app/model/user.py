from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from my_authentication_app.database import Base

class User(Base):
    __tablename__ = "users"

    userId = Column(String, primary_key=True, index=True, unique=True)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    phone = Column(String, nullable=True)

    organizations = relationship("Organization", back_populates="owner")
    memberships = relationship("OrganizationMember", back_populates="user")
