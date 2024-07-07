from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from my_authentication_app.database import Base

class OrganizationMember(Base):
    __tablename__ = 'organization_members'
    __table_args__ = {'extend_existing': True}
    
    orgId = Column(String, ForeignKey('organizations.orgId'), primary_key=True)
    userId = Column(String, ForeignKey('users.userId'), primary_key=True)

    user = relationship("User", back_populates="memberships")
    organization = relationship("Organization", back_populates="members")
