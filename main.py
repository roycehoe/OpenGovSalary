from dataclasses import dataclass

import numpy as np

from gateway import (
    get_ogp_api_product_cost_response,
    get_ogp_api_product_members_response,
    get_ogp_api_repos_response,
)
from models import OgpApiRepoResponse, Project, StaffData, StaffDataByProject


def get_project_staff(
    ogp_api_repo_response: OgpApiRepoResponse,
) -> list[StaffDataByProject]:
    ogp_product_name = ogp_api_repo_response.name
    ogp_product_logo_url = ogp_api_repo_response.logoUrl

    ogp_product_cost_response = get_ogp_api_product_cost_response(
        ogp_api_repo_response.path
    )
    ogp_product_cost = ogp_product_cost_response.manpower

    ogp_product_members = get_ogp_api_product_members_response(
        ogp_api_repo_response.path
    )
    output = []

    for i in ogp_product_members:
        staff = StaffDataByProject(
            id=i.staff.id,
            name=i.staff.name,
            terminationDate=i.staff.terminationDate,
            project=Project(
                name=ogp_product_name,
                logo_url=ogp_product_logo_url,
                role=i.role,
                involvement=i.involvement,
                cost=ogp_product_cost,
            ),
        )
        output.append(staff)
    return output


def get_all_staff_data_by_project() -> list[StaffDataByProject]:
    all_staff_data_by_project: list[StaffDataByProject] = []
    ogp_repos_response = get_ogp_api_repos_response()
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


def get_staff_data(
    staff_id: str, all_staff_data_by_project: list[StaffDataByProject]
) -> StaffData:
    staff = [
        project_staff
        for project_staff in all_staff_data_by_project
        if project_staff.id == staff_id
    ]
    return StaffData(
        id=staff[0].id,
        name=staff[0].name,
        terminationDate=staff[0].terminationDate,
        projects=[i.project for i in staff],
    )


def get_all_staff_data() -> list[StaffData]:
    all_staff_data_by_project = get_all_staff_data_by_project()
    staff_ids = get_all_staff_ids()
    return [get_staff_data(i, all_staff_data_by_project) for i in staff_ids]


def get_all_staff_contribution_per_project(
    all_staff_data: list[StaffData], project_name: str
):
    contribution = []
    for individual_staff_data in all_staff_data:
        staff_contribution = 0
        for project in individual_staff_data.projects:
            if project.name == project_name:
                staff_contribution = project.involvement
        contribution.append(staff_contribution)
    return contribution


def get_ogp_project_contribution_matrix(
    all_staff_data: list[StaffData], ogp_repos_response: list[OgpApiRepoResponse]
) -> list[list[int]]:
    """
    Each row represents a project
    Each column represents an individual person
    Each element represents the contribution of an individual to a given project
    """
    contribution_matrix: list[list[int]] = []
    for ogp_repo in ogp_repos_response:
        project_name = ogp_repo.name
        staff_contribution = get_all_staff_contribution_per_project(
            all_staff_data, project_name
        )
        contribution_matrix.append(staff_contribution)
    return contribution_matrix


def get_ogp_project_costs() -> list[float]:
    ogp_repos_response = get_ogp_api_repos_response()
    ogp_project_costs = [
        get_ogp_api_product_cost_response(i.path).manpower for i in ogp_repos_response
    ]
    return ogp_project_costs


MONTHS_IN_YEAR = 12
MONTHS_IN_QUARTER = 3


def get_yearly_salary(
    quarterly_salary: float,
    months_in_year: int = MONTHS_IN_YEAR,
    months_in_quarter: int = MONTHS_IN_QUARTER,
):
    return quarterly_salary / months_in_quarter * months_in_year


def get_staff_costs_with_least_squares_method(
    project_contribution_matrix: list[list[int]], project_costs: list[float]
):
    staff_costs, _, _, _ = np.linalg.lstsq(
        np.array(project_contribution_matrix), np.array(project_costs), rcond=None
    )
    return staff_costs


@dataclass
class StaffAnnualSalary:
    name: str
    salary: float


def get_all_staff_annual_salary(
    all_staff_data: list[StaffData],
    ogp_api_repos_response: list[OgpApiRepoResponse],
    ogp_project_costs: list[float],
) -> list[StaffAnnualSalary]:
    all_staff_annual_salary: list[StaffAnnualSalary] = []

    project_contribution_matrix = get_ogp_project_contribution_matrix(
        all_staff_data, ogp_api_repos_response
    )
    all_staff_quarterly_salary = get_staff_costs_with_least_squares_method(
        project_contribution_matrix, ogp_project_costs
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


def display_staff_salaries():
    all_staff_data = get_all_staff_data()
    ogp_repos_response = get_ogp_api_repos_response()

    project_contribution_matrix = get_ogp_project_contribution_matrix(
        all_staff_data, ogp_repos_response
    )
    ogp_project_costs = get_ogp_project_costs()
    all_staff_quarterly_salary = get_staff_costs_with_least_squares_method(
        project_contribution_matrix, ogp_project_costs
    )

    individual_staff_yearly_salary = [
        get_yearly_salary(individual_staff_quarterly_salary)
        for individual_staff_quarterly_salary in all_staff_quarterly_salary
    ]

    for i in range(len(all_staff_data)):
        print(f"{all_staff_data[i].name}: {individual_staff_yearly_salary[i]}")


all_staff_data = get_all_staff_data()
ogp_repos_response = get_ogp_api_repos_response()
ogp_project_costs = get_ogp_project_costs()
all_staff_annual_salary = get_all_staff_annual_salary(
    all_staff_data, ogp_repos_response, ogp_project_costs
)
print(all_staff_annual_salary)

# display_staff_salaries()
