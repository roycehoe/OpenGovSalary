import json
import requests
from pydantic import BaseModel
from typing import Any
import numpy as np

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

class StaffDataByProject(StaffResponse):
    project: Project

class StaffData(StaffResponse):
    projects: list[Project]

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


def get_project_staff(ogp_repo: OgpRepoResponse) -> list[StaffDataByProject]:
    ogp_product_name = ogp_repo.name
    ogp_product_logo_url = ogp_repo.logoUrl

    ogp_product_cost_response = get_ogp_product_cost_response(ogp_repo.path)
    ogp_product_cost = ogp_product_cost_response.manpower

    ogp_product_members = get_ogp_product_members_response(ogp_repo.path)
    output = []

    for i in ogp_product_members:
        staff = StaffDataByProject(id=i.staff.id, name=i.staff.name,
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


def get_all_staff_data_by_project() -> list[StaffDataByProject]:
    all_staff_data_by_project: list[StaffDataByProject] = []
    ogp_repos_response = get_ogp_repos_response()
    for i in ogp_repos_response:
        project_staff = get_project_staff(i)
        all_staff_data_by_project = [*all_staff_data_by_project, *project_staff]
    return all_staff_data_by_project


def get_all_staff_ids():
    all_staff_ids: set[str] = set()
    all_project_staff = get_all_staff_data_by_project()
    for i in all_project_staff:
        if i.id in all_staff_ids:
            continue
        all_staff_ids.add(i.id)
    return all_staff_ids


def get_staff_data(staff_id: str, all_staff_data_by_project: list[StaffDataByProject]) -> StaffData:
    staff = [project_staff for project_staff in all_staff_data_by_project if project_staff.id==staff_id]
    return StaffData(id=staff[0].id, name=staff[0].name, terminationDate=staff[0].terminationDate, projects=[i.project for i in staff])


def get_all_staff_data() -> list[StaffData]:
    all_staff_data_by_project = get_all_staff_data_by_project()
    staff_ids = get_all_staff_ids()
    return [get_staff_data(i, all_staff_data_by_project) for i in staff_ids]


def get_all_staff_contribution_per_project(all_staff_data: list[StaffData], project_name: str):
    contribution = []
    for individual_staff_data in all_staff_data:
        staff_contribution = 0
        for project in individual_staff_data.projects:
            if project.name == project_name:
                staff_contribution = project.involvement
        contribution.append(staff_contribution)
    return contribution

def get_contribution_matrix():
    """
    Each row represents a project
    Each column represents an individual person
    Each element represents the contribution of an individual to a given project
    """
    ans = []
    all_staff_data = get_all_staff_data()
    ogp_repos_response = get_ogp_repos_response()
    for ogp_repo in ogp_repos_response:
        project_name = ogp_repo.name
        staff_contribution = get_all_staff_contribution_per_project(all_staff_data, project_name)
        ans.append(staff_contribution)
    return ans

def get_ogp_project_costs():
    ogp_repos_response = get_ogp_repos_response()
    ogp_project_costs = [get_ogp_product_cost_response(i.path).manpower for i in ogp_repos_response]
    return ogp_project_costs

A = np.array(get_contribution_matrix())
b = np.array(get_ogp_project_costs())

individual_costs, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)
all_staff_data = get_all_staff_data()

print(len(all_staff_data) == len(individual_costs))

for i in range(len(all_staff_data)):
    print(f'{all_staff_data[i].name}: {individual_costs[i] * 4}')
