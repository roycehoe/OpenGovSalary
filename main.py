import json
import requests
from pydantic import BaseModel

OGP_REPOS_URL = "https://products.open.gov.sg/api/repos"
OGP_BASE_URL = "https://products.open.gov.sg/"
DEFAULT_START_DATE = "2023-07-01"

class OgpRepo(BaseModel):
    path: str
    logoUrl: str
    name: str


class OgpProductCost(BaseModel):
    infra: float
    manpower: float
    overhead: float


def get_ogp_repos(url:str = OGP_REPOS_URL) -> list[OgpRepo]:
    try:
        ogp_repos_response = requests.get(url)
        return [OgpRepo(**ogp_repo) for ogp_repo in ogp_repos_response.json()]
    except Exception:
        raise Exception # To handle custom error here


def get_ogp_product_cost_url(product_name:str, start_date:str=DEFAULT_START_DATE, ogp_base_url:str = OGP_BASE_URL):
    return f'{ogp_base_url}{product_name}/api/costs?startDate={start_date}'


def get_ogp_product_members_url(product_name:str, ogp_base_url:str = OGP_BASE_URL):
    return f'{ogp_base_url}{product_name}/api/members'


def get_ogp_product_cost(product_path: str) -> OgpProductCost:
    url = get_ogp_product_cost_url(product_path)
    try:
        ogp_product_cost_response = requests.get(url)
        return OgpProductCost(**ogp_product_cost_response.json())
    except Exception:
        raise Exception # To handle custom error here

ogp_repos = get_ogp_repos()
for ogp_repo in ogp_repos:
    ogp_product_cost = get_ogp_product_cost(ogp_repo.path)
    print(ogp_product_cost)


    # def get_ogp_product_members():
    #     ...
