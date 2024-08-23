from dataclasses import asdict, dataclass
from typing import Union

import numpy as np
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from gateway import get_ogp_api_all_repos_response, get_ogp_api_product_cost_response
from models import OgpRepo, StaffResponse
from staff import Staff, get_all_staff_data


@dataclass
class StaffAnnualSalary:
    name: str
    salary: float

    def __str__(self):
        return f"{self.name}: {self.salary:,.0f}"


def get_all_staff_contribution_per_product(
    all_staff_data: list[Staff], product_name: str
) -> list[Union[int, float]]:
    contribution = []
    for individual_staff_data in all_staff_data:
        staff_contribution = 0
        for product in individual_staff_data.product:
            if product.name == product_name:
                staff_contribution = product.involvement
        contribution.append(staff_contribution)
    return contribution


def get_ogp_product_contribution_matrix(
    all_staff_data: list[Staff], ogp_repos_response: list[OgpRepo]
) -> list[list[Union[int, float]]]:
    """
    Each row represents a product
    Each column represents an individual person
    Each element represents the contribution of an individual to a given product
    """
    contribution_matrix: list[list[Union[int, float]]] = []
    for ogp_repo in ogp_repos_response:
        product_name = ogp_repo.name
        staff_contribution = get_all_staff_contribution_per_product(
            all_staff_data, product_name
        )
        contribution_matrix.append(staff_contribution)
    return contribution_matrix


def get_ogp_product_costs() -> list[float]:
    all_ogp_api_all_repos_response = get_ogp_api_all_repos_response()
    ogp_product_costs = [
        get_ogp_api_product_cost_response(ogp_api_repo_response.path).salary
        for ogp_api_repo_response in all_ogp_api_all_repos_response
    ]
    return ogp_product_costs


MONTHS_IN_YEAR = 12
MONTHS_IN_QUARTER = 3


def _get_yearly_salary(
    quarterly_salary: float,
    months_in_year: int = MONTHS_IN_YEAR,
    months_in_quarter: int = MONTHS_IN_QUARTER,
):
    return quarterly_salary / months_in_quarter * months_in_year


def get_quarterly_staff_costs_with_least_squares_method(
    product_contribution_matrix: list[list[Union[int, float]]],
    quarterly_product_costs: list[float],
):
    staff_costs, _, _, _ = np.linalg.lstsq(
        np.array(product_contribution_matrix),
        np.array(quarterly_product_costs),
        rcond=None,
    )
    return staff_costs


def get_all_staff_annual_salary(
    all_staff_data: list[Staff],
    ogp_api_repos_response: list[OgpRepo],
    ogp_product_costs: list[float],
) -> list[StaffAnnualSalary]:
    all_staff_annual_salary: list[StaffAnnualSalary] = []

    product_contribution_matrix = get_ogp_product_contribution_matrix(
        all_staff_data, ogp_api_repos_response
    )
    all_staff_quarterly_cost = get_quarterly_staff_costs_with_least_squares_method(
        product_contribution_matrix, ogp_product_costs
    )
    individual_staff_yearly_cost = [
        _get_yearly_salary(individual_staff_quarterly_cost)
        for individual_staff_quarterly_cost in all_staff_quarterly_cost
    ]

    for i in range(len(all_staff_data)):
        all_staff_annual_salary.append(
            StaffAnnualSalary(
                name=all_staff_data[i].name, salary=individual_staff_yearly_cost[i]
            )
        )
    return all_staff_annual_salary


def get_staff_response() -> list[StaffResponse]:
    staff_response: list[StaffResponse] = []
    all_staff_data = get_all_staff_data()
    all_ogp_repos_response = get_ogp_api_all_repos_response()
    ogp_product_costs = get_ogp_product_costs()
    all_staff_annual_salary = get_all_staff_annual_salary(
        all_staff_data, all_ogp_repos_response, ogp_product_costs
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
    all_ogp_repos_response = get_ogp_api_all_repos_response()
    ogp_product_costs = get_ogp_product_costs()
    all_staff_annual_salary = get_all_staff_annual_salary(
        all_staff_data, all_ogp_repos_response, ogp_product_costs
    )
    sorted_all_staff_annual_salary = sorted(
        all_staff_annual_salary, key=lambda staff: staff.salary, reverse=True
    )
    for individual_staff_annual_salary in sorted_all_staff_annual_salary:
        print(individual_staff_annual_salary)


app = FastAPI()


@app.get("/")
def get_staff_salaries() -> list[StaffResponse]:
    return get_staff_response()


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
