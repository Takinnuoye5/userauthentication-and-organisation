from pydantic import BaseModel
from typing import Optional, List

class OrganizationCreate(BaseModel):
    name: str
    description: Optional[str] = None

class OrganizationResponse(BaseModel):
    orgId: str
    name: str
    description: Optional[str] = None

    class Config:
        orm_mode = True

class AddUserToOrganization(BaseModel):
    userId: str

class OrganizationsResponse(BaseModel):
    status: str
    message: str
    data: List[OrganizationResponse]

    class Config:
        orm_mode = True
