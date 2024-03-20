import requests

from models import (
    OgpApiProductCostResponse,
    OgpApiProductMembersResponse,
    OgpApiRepoResponse,
)

OGP_REPOS_URL = "https://products.open.gov.sg/api/repos"
OGP_BASE_URL = "https://products.open.gov.sg/"
DEFAULT_START_DATE = "2023-07-01"


def get_ogp_api_all_repos_response(
    url: str = OGP_REPOS_URL,
) -> list[OgpApiRepoResponse]:
    try:
        ogp_repos_response = requests.get(url)
        return [
            OgpApiRepoResponse(**ogp_repo) for ogp_repo in ogp_repos_response.json()
        ]
    except Exception:
        raise Exception  # To handle custom error here


def _get_ogp_product_cost_url(
    product_name: str,
    start_date: str = DEFAULT_START_DATE,
    ogp_base_url: str = OGP_BASE_URL,
):
    return f"{ogp_base_url}{product_name}/api/costs?startDate={start_date}"


def get_ogp_api_product_cost_response(product_path: str) -> OgpApiProductCostResponse:
    url = _get_ogp_product_cost_url(product_path)
    try:
        ogp_product_cost_response = requests.get(url)
        return OgpApiProductCostResponse(**ogp_product_cost_response.json())
    except Exception:
        raise Exception  # To handle custom error here


def _get_ogp_api_product_members_url(
    product_name: str,
    start_date: str = DEFAULT_START_DATE,
    ogp_base_url: str = OGP_BASE_URL,
):
    return f"{ogp_base_url}{product_name}/api/members?startDate={start_date}"


def get_ogp_api_product_members_response(
    product_path: str,
) -> list[OgpApiProductMembersResponse]:
    url = _get_ogp_api_product_members_url(product_path)
    try:
        ogp_api_product_members_response = requests.get(url)
        return [
            OgpApiProductMembersResponse(**ogp_api_product_member)
            for ogp_api_product_member in ogp_api_product_members_response.json()
        ]
    except Exception:
        raise Exception  # To handle custom error here


def get_ogp_api_people_response(
    name: str,
) -> str:
    url = f"{OGP_BASE_URL}/people/{name}"
    try:
        ogp_api_people_response = requests.get(url)
        return ogp_api_people_response.text
    except Exception:
        raise Exception  # To handle custom error here
