import json
from dataclasses import asdict, dataclass
from typing import Union

import numpy as np

from models import OgpProduct
from products import get_ogp_products
from team_member import get_team_member_info

MONTHS_IN_YEAR = 12
MONTHS_IN_QUARTER = 3


@dataclass
class Contribution:
    product_name: str
    team_member_name: str
    team_member_contribution: float
    team_member_title: str
    product_salary_cost: float


def _get_yearly_salary(
    quarterly_salary: float,
    months_in_year: int = MONTHS_IN_YEAR,
    months_in_quarter: int = MONTHS_IN_QUARTER,
):
    return quarterly_salary / months_in_quarter * months_in_year


def get_contribution_by_product(ogp_product: OgpProduct) -> list[Contribution]:
    contribution: list[Contribution] = []

    for team_member in ogp_product.team_members:
        team_member_info = get_team_member_info(
            team_member.path, team_member.default_name
        )
        contribution.append(
            Contribution(
                product_name=ogp_product.name,
                team_member_name=team_member_info.name,
                team_member_contribution=team_member.involvement,
                team_member_title=team_member_info.title,
                product_salary_cost=ogp_product.cost.salary,
            )
        )

    return contribution


def get_all_contributions() -> list[Contribution]:
    with open("data.json") as file:
        loaded_file = json.load(file)
        return [Contribution(**i) for i in loaded_file]


def get_product_contribution_matrix(
    contributions: list[Contribution],
) -> list[list[Union[int, float]]]:
    """
    Each row represents a product
    Each column represents an individual person
    Each element represents the contribution of an individual to a given product
    """
    products = sorted(set(contribution.product_name for contribution in contributions))
    team_members = sorted(
        set(contribution.team_member_name for contribution in contributions)
    )

    # Create a dictionary to map products and team members to indices
    product_index = {product: i for i, product in enumerate(products)}
    team_member_index = {team_member: i for i, team_member in enumerate(team_members)}

    # Initialize a matrix with zeros
    product_contribution_matrix: list[list[Union[int, float]]] = [
        [0 for _ in range(len(team_members))] for _ in range(len(products))
    ]

    # Populate the matrix with contributions
    for contribution in contributions:
        row_index = product_index.get(contribution.product_name)
        col_index = team_member_index.get(contribution.team_member_name)

        # Ensure valid indices and aggregate contributions if necessary
        if row_index is not None and col_index is not None:
            product_contribution_matrix[row_index][
                col_index
            ] += contribution.team_member_contribution

    return product_contribution_matrix


def get_quarterly_product_costs(contributions: list[Contribution]) -> list[float]:
    quarterly_product_costs: list[float] = []

    seen_products = set()

    for contribution in contributions:
        if contribution.product_name in seen_products:
            continue
        quarterly_product_costs.append(contribution.product_salary_cost)
        seen_products.add(contribution.product_name)
    return quarterly_product_costs


def get_quarterly_team_members_cost_with_least_squares_method(
    product_contribution_matrix: list[list[Union[int, float]]],
    quarterly_product_costs: list[float],
):
    staff_costs, _, _, _ = np.linalg.lstsq(
        np.array(product_contribution_matrix),
        np.array(quarterly_product_costs),
        rcond=None,
    )
    return staff_costs


def get_team_members_yearly_salary():
    # ogp_products = get_ogp_products()

    # contributions = []
    # for ogp_product in ogp_products:
    #     contribution = get_contribution_by_product(ogp_product)
    #     contributions = [*contributions, *contribution]

    contributions = get_all_contributions()

    product_contribution_matrix = get_product_contribution_matrix(contributions)
    quarterly_product_costs = get_quarterly_product_costs(contributions)

    team_members_quarterly_salary = (
        get_quarterly_team_members_cost_with_least_squares_method(
            product_contribution_matrix, quarterly_product_costs
        )
    )
    team_members_yearly_salary = [
        _get_yearly_salary(team_member_quarterly_salary)
        for team_member_quarterly_salary in team_members_quarterly_salary
    ]
    team_members_names = sorted(
        set(contribution.team_member_name for contribution in contributions)
    )
    return dict(zip(team_members_names, team_members_yearly_salary))


def main():
    print(get_team_members_yearly_salary())


main()
