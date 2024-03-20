from dataclasses import dataclass
from datetime import date, datetime
from typing import Any

from bs4 import BeautifulSoup

from gateway import (
    get_ogp_api_all_repos_response,
    get_ogp_api_people_response,
    get_ogp_api_product_cost_response,
    get_ogp_api_product_members_response,
)
from models import OgpApiRepoResponse


@dataclass
class Product:
    name: str
    logo_url: str
    role: str
    involvement: float
    cost: float


@dataclass
class ProductStaff:
    id: str
    name: str
    terminationDate: Any
    product: Product


@dataclass
class Staff:
    id: str
    name: str
    terminationDate: Any
    product: list[Product]

    OGP_HEADSHOTS_BASEURL: str = "https://www.open.gov.sg/images/headshots/"
    headshot_url: str = ""

    def __post_init__(self) -> None:
        self.headshot_url = f"{self.OGP_HEADSHOTS_BASEURL}{self.id}.jpg"


def _get_product_staff(
    ogp_api_repo_response: OgpApiRepoResponse,
) -> list[ProductStaff]:
    """Returns a list of staff members for a given product"""
    ogp_product_name = ogp_api_repo_response.name
    ogp_product_logo_url = ogp_api_repo_response.logoUrl

    ogp_product_cost_response = get_ogp_api_product_cost_response(
        ogp_api_repo_response.path
    )
    ogp_product_cost = ogp_product_cost_response.manpower

    ogp_product_members = get_ogp_api_product_members_response(
        ogp_api_repo_response.path
    )
    product_staff: list[ProductStaff] = []

    for ogp_product_member in ogp_product_members:
        staff = ProductStaff(
            id=ogp_product_member.staff.id,
            name=ogp_product_member.staff.name,
            terminationDate=ogp_product_member.staff.terminationDate,
            product=Product(
                name=ogp_product_name,
                logo_url=ogp_product_logo_url,
                role=ogp_product_member.role,
                involvement=ogp_product_member.involvement,
                cost=ogp_product_cost,
            ),
        )
        product_staff.append(staff)
    return product_staff


def _get_all_products_staff() -> list[ProductStaff]:
    """Returns a list of all staff members for all products"""
    all_products_staff: list[ProductStaff] = []
    all_ogp_repos_response = get_ogp_api_all_repos_response()
    for ogp_repo_response in all_ogp_repos_response:
        product_staff = _get_product_staff(ogp_repo_response)
        all_products_staff = [*all_products_staff, *product_staff]
    return all_products_staff


def _get_all_staff_ids(all_products_staff: list[ProductStaff]) -> set[str]:
    all_staff_ids: set[str] = set()
    for product_staff in all_products_staff:
        if product_staff.id in all_staff_ids:
            continue
        all_staff_ids.add(product_staff.id)
    return all_staff_ids


def _get_staff_data(
    staff_id: str, all_staff_data_by_product: list[ProductStaff]
) -> Staff:
    """Returns a staff object containing all products worked on by said staff"""
    staff = [
        product_staff
        for product_staff in all_staff_data_by_product
        if product_staff.id == staff_id
    ]
    return Staff(
        id=staff[0].id,
        name=staff[0].name,
        terminationDate=staff[0].terminationDate,
        product=[i.product for i in staff],
    )


def get_staff_start_date(name: str) -> date:
    ogp_api_people_response = get_ogp_api_people_response(name)
    soup = BeautifulSoup(ogp_api_people_response, "html.parser")
    try:
        staff_date_of_hire = (
            soup.select(".content")[0].find("p").find("strong").text.strip()
        )
    except Exception:
        raise Exception  # To raise custom bs4 parsing error here

    return datetime.strptime(staff_date_of_hire, "%B %d, %Y")


def get_staff_job_title(name: str) -> str:
    ogp_api_people_response = get_ogp_api_people_response(name)
    soup = BeautifulSoup(ogp_api_people_response, "html.parser")
    return soup.select(".staff-title")[-1].text.strip()


def get_all_staff_data() -> list[Staff]:
    all_staff_data_by_product = _get_all_products_staff()
    staff_ids = _get_all_staff_ids(all_staff_data_by_product)
    return [_get_staff_data(i, all_staff_data_by_product) for i in staff_ids]
