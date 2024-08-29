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


def get_current_product_contribution_matrix(contributions: list[Contribution]):
    matrix = []
    product_names = sorted(set([i.product_name for i in contributions]))
    team_members = sorted(set([i.team_member_name for i in contributions]))

    for product_name in product_names:
        row = []
        contributions_by_product = {
            contribution.team_member_name: contribution.team_member_contribution
            for contribution in contributions
            if contribution.product_name == product_name
        }
        for team_member in team_members:
            row.append(contributions_by_product.get(team_member, 0))
        matrix.append(row)

    return matrix


def get_team_members_yearly_salary():
    # ogp_products = get_ogp_products()

    # contributions = []
    # for ogp_product in ogp_products:
    #     contribution = get_contribution_by_product(ogp_product)
    #     contributions = [*contributions, *contribution]

    contributions = get_all_contributions()

    product_contribution_matrix = get_current_product_contribution_matrix(contributions)
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
    team_members_names = set(
        contribution.team_member_name for contribution in contributions
    )
    return dict(zip(team_members_names, team_members_yearly_salary))


def main():
    print(get_team_members_yearly_salary())


main()
