from dataclasses import asdict, dataclass
from typing import Any

import numpy as np
from pydantic import BaseModel

from gateway import (
    get_ogp_api_product_cost_response,
    get_ogp_api_product_members_response,
    get_ogp_api_repos_response,
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

    def model_post_init(self, __context) -> None:
        self.headshot_url = f"{self.OGP_HEADSHOTS_BASEURL}{self.id}.jpg"


@dataclass
class StaffAnnualSalary:
    name: str
    salary: float

    def __str__(self):
        return f"{self.name}: {self.salary:,.0f}"


class StaffResponse(BaseModel):
    id: str
    name: str
    terminationDate: Any
    product: list[Product]
    headshot_url: str
    salary: float


def get_product_staff(
    ogp_api_repo_response: OgpApiRepoResponse,
) -> list[ProductStaff]:
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


def get_all_products_staff() -> list[ProductStaff]:
    all_products_staff: list[ProductStaff] = []
    ogp_repos_response = get_ogp_api_repos_response()
    for ogp_repo_response in ogp_repos_response:
        product_staff = get_product_staff(ogp_repo_response)
        all_products_staff = [*all_products_staff, *product_staff]
    return all_products_staff


def get_all_staff_ids() -> set[str]:
    all_staff_ids: set[str] = set()
    all_products_staff = get_all_products_staff()
    for product_staff in all_products_staff:
        if product_staff.id in all_staff_ids:
            continue
        all_staff_ids.add(product_staff.id)
    return all_staff_ids


def get_staff_data(
    staff_id: str, all_staff_data_by_product: list[ProductStaff]
) -> Staff:
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


def get_all_staff_data() -> list[Staff]:
    all_staff_data_by_product = get_all_products_staff()
    staff_ids = get_all_staff_ids()
    return [get_staff_data(i, all_staff_data_by_product) for i in staff_ids]


def get_all_staff_contribution_per_product(
    all_staff_data: list[Staff], product_name: str
):
    contribution = []
    for individual_staff_data in all_staff_data:
        staff_contribution = 0
        for product in individual_staff_data.product:
            if product.name == product_name:
                staff_contribution = product.involvement
        contribution.append(staff_contribution)
    return contribution


def get_ogp_product_contribution_matrix(
    all_staff_data: list[Staff], ogp_repos_response: list[OgpApiRepoResponse]
) -> list[list[int]]:
    """
    Each row represents a product
    Each column represents an individual person
    Each element represents the contribution of an individual to a given product
    """
    contribution_matrix: list[list[int]] = []
    for ogp_repo in ogp_repos_response:
        product_name = ogp_repo.name
        staff_contribution = get_all_staff_contribution_per_product(
            all_staff_data, product_name
        )
        contribution_matrix.append(staff_contribution)
    return contribution_matrix


def get_ogp_product_costs() -> list[float]:
    ogp_repos_response = get_ogp_api_repos_response()
    ogp_product_costs = [
        get_ogp_api_product_cost_response(i.path).manpower for i in ogp_repos_response
    ]
    return ogp_product_costs


MONTHS_IN_YEAR = 12
MONTHS_IN_QUARTER = 3


def get_yearly_salary(
    quarterly_salary: float,
    months_in_year: int = MONTHS_IN_YEAR,
    months_in_quarter: int = MONTHS_IN_QUARTER,
):
    return quarterly_salary / months_in_quarter * months_in_year


def get_staff_costs_with_least_squares_method(
    product_contribution_matrix: list[list[int]], product_costs: list[float]
):
    staff_costs, _, _, _ = np.linalg.lstsq(
        np.array(product_contribution_matrix), np.array(product_costs), rcond=None
    )
    return staff_costs


def get_all_staff_annual_salary(
    all_staff_data: list[Staff],
    ogp_api_repos_response: list[OgpApiRepoResponse],
    ogp_product_costs: list[float],
) -> list[StaffAnnualSalary]:
    all_staff_annual_salary: list[StaffAnnualSalary] = []

    product_contribution_matrix = get_ogp_product_contribution_matrix(
        all_staff_data, ogp_api_repos_response
    )
    all_staff_quarterly_salary = get_staff_costs_with_least_squares_method(
        product_contribution_matrix, ogp_product_costs
    )
    individual_staff_yearly_salary = [
        get_yearly_salary(individual_staff_quarterly_salary)
        for individual_staff_quarterly_salary in all_staff_quarterly_salary
    ]

    for i in range(len(all_staff_data)):
        all_staff_annual_salary.append(
            StaffAnnualSalary(
                name=all_staff_data[i].name, salary=individual_staff_yearly_salary[i]
            )
        )
    return all_staff_annual_salary


SIMPLE_CACHE: list[StaffResponse] = []


def get_set_cache(func):
    def wrap():
        global SIMPLE_CACHE
        if SIMPLE_CACHE:
            return SIMPLE_CACHE
        ans = func()
        SIMPLE_CACHE = ans
        return ans

    return wrap


@get_set_cache
def get_staff_response() -> list[StaffResponse]:
    staff_response: list[StaffResponse] = []
    all_staff_data = get_all_staff_data()
    ogp_repos_response = get_ogp_api_repos_response()
    ogp_product_costs = get_ogp_product_costs()
    all_staff_annual_salary = get_all_staff_annual_salary(
        all_staff_data, ogp_repos_response, ogp_product_costs
    )
    for staff_data in all_staff_data:
        staff_name = staff_data.name
        for staff_annual_salary in all_staff_annual_salary:
            if staff_annual_salary.name != staff_name:
                continue
            staff_response.append(
                StaffResponse(**asdict(staff_data), salary=staff_annual_salary.salary)
            )
    staff_response = sorted(
        staff_response, key=lambda staff: staff.salary, reverse=True
    )
    return staff_response


def display_staff_salaries() -> None:
    all_staff_data = get_all_staff_data()
    ogp_repos_response = get_ogp_api_repos_response()
    ogp_product_costs = get_ogp_product_costs()
    all_staff_annual_salary = get_all_staff_annual_salary(
        all_staff_data, ogp_repos_response, ogp_product_costs
    )
    sorted_all_staff_annual_salary = sorted(
        all_staff_annual_salary, key=lambda staff: staff.salary, reverse=True
    )
    for individual_staff_annual_salary in sorted_all_staff_annual_salary:
        print(individual_staff_annual_salary)


print(get_staff_response())
