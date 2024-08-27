from datetime import date, datetime
from typing import Any, Optional

from pydantic import BaseModel


class OgpProductBase(BaseModel):
    path: str
    logoUrl: str
    name: str


class OgpProductCost(BaseModel):
    infrastructure: float
    salary: float
    corporate_overhead: float
    equipment_software_and_office: float
    others: float


class OgpApiStaffResponse(BaseModel):
    id: str
    name: str
    terminationDate: Any


class OgpApiProductMembersResponse(BaseModel):
    role: str
    involvement: float
    staff: OgpApiStaffResponse


class OgpProductTeamMember(BaseModel):
    path: str
    involvement: float


class OgpProduct(OgpProductBase):
    cost: OgpProductCost
    team_members: list[OgpProductTeamMember]


class OgpTeamMember(BaseModel):
    profile_picture: str
    name: str
    title: str
    join_date: Optional[datetime]
