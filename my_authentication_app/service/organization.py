from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from my_authentication_app.model.organization import Organization, OrganizationMember
from my_authentication_app.model.user import User
from my_authentication_app.schema.organization import OrganizationCreate
import uuid

def get_organization(org_id: str, db: Session):
    return db.query(Organization).filter(Organization.orgId == org_id).first()

def get_organizations_for_user(user_id: str, db: Session):
    user = db.query(User).filter(User.userId == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    organizations = db.query(Organization).filter(
        (Organization.owner_id == user_id) |
        (Organization.members.any(User.userId == user_id))
    ).all()
    return organizations

def create_organization(org: OrganizationCreate, owner_id: str, db: Session):
    new_org = Organization(orgId=str(uuid.uuid4()), name=org.name, description=org.description, owner_id=owner_id)
    db.add(new_org)
    db.commit()
    db.refresh(new_org)
    return new_org

def add_user_to_organization(org_id: str, user_id: str, db: Session):
    user = db.query(User).filter(User.userId == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    organization_member = OrganizationMember(orgId=org_id, userId=user_id)
    db.add(organization_member)
    db.commit()
    db.refresh(organization_member)
    return organization_member
