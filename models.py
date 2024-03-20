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


class OgpApiStaffResponse(BaseModel):
    id: str
    name: str
    terminationDate: Any


class OgpApiProductMembersResponse(BaseModel):
    role: str
    involvement: float
    staff: OgpApiStaffResponse


class Product(BaseModel):
    name: str
    logo_url: str
    role: str
    involvement: float
    cost: float


class StaffResponse(BaseModel):
    id: str
    name: str
    terminationDate: Any
    product: list[Product]
    headshot_url: str
    salary: float
