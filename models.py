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


class Product(BaseModel):
    name: str
    logo_url: str
    role: str
    involvement: float
    cost: float


class StaffDataByProduct(StaffResponse):
    product: Product


class StaffData(StaffResponse):
    OGP_HEADSHOTS_URL: str = "https://www.open.gov.sg/images/headshots/"

    product: list[Product]
    headshot_url: str = ""

    def model_post_init(self, __context) -> None:
        self.headshot_url = f"{self.OGP_HEADSHOTS_URL}{self.id}.jpg"
