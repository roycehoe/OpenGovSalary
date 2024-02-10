import json
import requests
from pydantic import BaseModel
from typing import Any

OGP_REPOS_URL = "https://products.open.gov.sg/api/repos"
OGP_BASE_URL = "https://products.open.gov.sg/"
DEFAULT_START_DATE = "2023-07-01"

class OgpRepoResponse(BaseModel):
    path: str
    logoUrl: str
    name: str


class OgpProductCostResponse(BaseModel):
    infra: float
    manpower: float
    overhead: float


class StaffResponse(BaseModel):
    id: str
    name: str
    terminationDate: Any


class OgpProductMembersResponse(BaseModel):
    role: str
    involvement: float
    staff: StaffResponse


class Project(BaseModel):
    name: str
    logo_url: str
    role: str
    involvement: float
    cost: float

class Staff(StaffResponse):
    project: Project


def get_ogp_repos_response(url:str = OGP_REPOS_URL) -> list[OgpRepoResponse]:
    try:
        ogp_repos_response = requests.get(url)
        return [OgpRepoResponse(**ogp_repo) for ogp_repo in ogp_repos_response.json()]
    except Exception:
        raise Exception # To handle custom error here


def get_ogp_product_cost_url(product_name:str, start_date:str=DEFAULT_START_DATE, ogp_base_url:str = OGP_BASE_URL):
    return f'{ogp_base_url}{product_name}/api/costs?startDate={start_date}'


def get_ogp_product_cost_response(product_path: str) -> OgpProductCostResponse:
    url = get_ogp_product_cost_url(product_path)
    try:
        ogp_product_cost_response = requests.get(url)
        return OgpProductCostResponse(**ogp_product_cost_response.json())
    except Exception:
        raise Exception # To handle custom error here


def get_ogp_product_members_url(product_name:str, start_date:str=DEFAULT_START_DATE, ogp_base_url:str = OGP_BASE_URL):
    return f'{ogp_base_url}{product_name}/api/members?startDate={start_date}'


def get_ogp_product_members_response(product_path: str) -> list[OgpProductMembersResponse]:
    url = get_ogp_product_members_url(product_path)
    try:
        ogp_product_members_response = requests.get(url)
        return [OgpProductMembersResponse(**i) for i in ogp_product_members_response.json()]
    except Exception:
        raise Exception # To handle custom error here


ogp_repos_response = get_ogp_repos_response()
ogp_repo = ogp_repos_response[0]

def get_project_staff(ogp_repo: OgpRepoResponse) -> list[Staff]:
    ogp_product_name = ogp_repo.name
    ogp_product_logo_url = ogp_repo.logoUrl

    ogp_product_cost_response = get_ogp_product_cost_response(ogp_repo.path)
    ogp_product_cost = ogp_product_cost_response.manpower

    ogp_product_members = get_ogp_product_members_response(ogp_repo.path)
    output = []

    for i in ogp_product_members:
        staff = Staff(id=i.staff.id, name=i.staff.name, 
                      terminationDate=i.staff.terminationDate, 
                      project=Project(
                        name=ogp_product_name,
                        logo_url=ogp_product_logo_url,
                        role=i.role, 
                        involvement=i.involvement, 
                        cost=ogp_product_cost)
                      )
        output.append(staff)
    return output

def get_all_project_staff() -> list[Staff]:
    all_project_staff: list[Staff] = []
    ogp_repos_response = get_ogp_repos_response()
    for i in ogp_repos_response:
        project_staff = get_project_staff(i)
        all_project_staff = [*all_project_staff, *project_staff]
    return all_project_staff

class Data(BaseModel):
    data: list[Staff]

all_project_staff = get_all_project_staff()
data = Data(data=all_project_staff)
print(data.model_dump_json())
