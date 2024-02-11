from typing import Any

from pydantic import BaseModel


class OgpApiRepoResponse(BaseModel):
    path: str
    logoUrl: str
    name: str


class OgpApiProductCostResponse(BaseModel):
    infra: float
    manpower: float
    overhead: float


class StaffResponse(BaseModel):
    id: str
    name: str
    terminationDate: Any


class OgpApiProductMembersResponse(BaseModel):
    role: str
    involvement: float
    staff: StaffResponse
