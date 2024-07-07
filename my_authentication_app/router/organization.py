from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from my_authentication_app.database import get_db
from my_authentication_app.schema.organization import OrganizationCreate, OrganizationResponse, OrganizationsResponse, AddUserToOrganization
from my_authentication_app.service import organization as org_service
from my_authentication_app.dependencies import get_current_user
from my_authentication_app.model.user import User

router = APIRouter()

@router.get("/", response_model=OrganizationsResponse)
def get_organizations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    organizations = org_service.get_organizations_for_user(current_user.userId, db)
    organizations_data = [
        OrganizationResponse(
            orgId=org.orgId,
            name=org.name,
            description=org.description
        ) for org in organizations
    ]
    return OrganizationsResponse(
        status="success",
        message="Organizations fetched successfully",
        data=organizations_data
    )

@router.get("/{org_id}", response_model=OrganizationResponse)
def get_organization(
    org_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    organization = org_service.get_organization(org_id, db)
    if not organization:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
    return OrganizationResponse(
        orgId=organization.orgId,
        name=organization.name,
        description=organization.description
    )

@router.post("/", response_model=OrganizationResponse)
def create_organization(
    org: OrganizationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not org.name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Name is required"
        )
    try:
        new_org = org_service.create_organization(org, current_user.userId, db)
        return OrganizationResponse(
            orgId=new_org.orgId,
            name=new_org.name,
            description=new_org.description
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/{org_id}/users", response_model=OrganizationsResponse)
def add_user_to_organization(
    org_id: str,
    request: AddUserToOrganization,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    organization = org_service.get_organization(org_id, db)
    if not organization:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")

    user = db.query(User).filter(User.userId == request.userId).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    try:
        org_service.add_user_to_organization(org_id, request.userId, db)
        return OrganizationsResponse(
            status="success",
            message="User added to organization successfully"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
