from datetime import date
from typing import Any, Optional

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
    product: list[Product]
    headshot_url: str
    salary: float
    title: Optional[str] = None
    start_date: Optional[date] = None
    termination_date: Optional[date] = None
