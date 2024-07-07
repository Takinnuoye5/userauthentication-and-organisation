from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from my_authentication_app.database import Base
from my_authentication_app.model.organization_member import OrganizationMember

class Organization(Base):
    __tablename__ = "organizations"

    orgId = Column(String, primary_key=True, index=True, unique=True)
    name = Column(String, nullable=False)
    description = Column(String)
    owner_id = Column(String, ForeignKey('users.userId'))

    owner = relationship("User", back_populates="organizations")
    members = relationship("OrganizationMember", back_populates="organization")
