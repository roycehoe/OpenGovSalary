from typing import Optional
from unicodedata import numeric

from bs4 import BeautifulSoup, NavigableString, Tag

from gateway import (
    CORPORATE_OVERHEAD_HTML_TAG,
    EQUIPMENT_SOFTWARE_AND_OFFICE_HTML_TAG,
    INFRASTRUCTURE_HTML_TAG,
    OGP_PRODUCTS_URL,
    OTHERS_HTML_TAG,
    SALARY_HTML_TAG,
    get_ogp_api_product_info_response,
    get_ogp_api_products_response,
)
from models import OgpProduct, OgpProductBase, OgpProductCost, OgpProductTeamMember


def _get_ogp_repo_tags(a_tags: list[Tag]) -> list[Tag]:
    return a_tags[1:-4]


def _get_ogp_products_base(ogp_api_products_response: str) -> list[OgpProductBase]:
    ogp_repos: list[OgpProductBase] = []

    soup = BeautifulSoup(ogp_api_products_response, features="html.parser")
    a_tags: list[Tag] = soup.find_all("a")
    ogp_repo_tags = _get_ogp_repo_tags(a_tags)

    repo_links = [tag["href"] for tag in ogp_repo_tags]
    repo_logo_links = [tag.find("img")["src"] for tag in ogp_repo_tags]

    repo_name = [repo_link[1:] for repo_link in repo_links]

    for i in range(len(repo_links)):
        ogp_repos.append(
            OgpProductBase(
                path=f"{OGP_PRODUCTS_URL[:-1]}{repo_links[i]}",
                logoUrl=f"{OGP_PRODUCTS_URL[:-1]}{repo_logo_links[i]}",
                name=repo_name[i],
            )
        )

    return ogp_repos


def _get_ogp_product_cost_component(
    ogp_api_product_info_response_soup: BeautifulSoup, cost_component: str
) -> float:
    cost_component_tag = ogp_api_product_info_response_soup.find(
        "div", string=cost_component
    )
    if cost_component_tag is None:
        return 0
    cost_component_number_tag = cost_component_tag.find_previous_sibling("div")
    if cost_component_number_tag is None:
        return 0
    cost_component_html_value = cost_component_number_tag.get_text(strip=True)
    return int(cost_component_html_value[1:].replace(",", ""))


def _get_ogp_product_cost(ogp_api_product_info_response: str) -> OgpProductCost:
    soup = BeautifulSoup(ogp_api_product_info_response, features="html.parser")
    return OgpProductCost(
        salary=_get_ogp_product_cost_component(soup, SALARY_HTML_TAG),
        infrastructure=_get_ogp_product_cost_component(soup, INFRASTRUCTURE_HTML_TAG),
        corporate_overhead=_get_ogp_product_cost_component(
            soup, CORPORATE_OVERHEAD_HTML_TAG
        ),
        equipment_software_and_office=_get_ogp_product_cost_component(
            soup, EQUIPMENT_SOFTWARE_AND_OFFICE_HTML_TAG
        ),
        others=_get_ogp_product_cost_component(soup, OTHERS_HTML_TAG),
    )


def get_ogp_product_team_member(
    ogp_product_member_tag: Tag,
) -> Optional[OgpProductTeamMember]:
    involvement_value = ogp_product_member_tag.find("img")
    if involvement_value is None:
        return None
    involvement_text = involvement_value["title"]
    involvement = numeric(
        involvement_text[involvement_text.index("(") + 1 : involvement_text.index(")")]
    )

    return OgpProductTeamMember(
        path=ogp_product_member_tag["href"],
        involvement=involvement,
    )


def _get_ogp_product_team_members(
    ogp_api_product_info_response: str,
) -> list[OgpProductTeamMember]:
    soup = BeautifulSoup(ogp_api_product_info_response, features="html.parser")
    team_members_title_tag = soup.find("h2", string="Team Members")
    if team_members_title_tag is None:
        return []
    team_members_title_parent_tag = team_members_title_tag.find_parent("div")
    if team_members_title_parent_tag is None:
        return []
    team_members_data_tag = team_members_title_parent_tag.find_next_sibling("div")
    if team_members_data_tag is None or isinstance(
        team_members_data_tag, NavigableString
    ):
        return []
    team_members_data = team_members_data_tag.find_all("a")
    if isinstance(team_members_data, Tag):
        return []

    return [
        get_ogp_product_team_member(team_member_data)
        for team_member_data in team_members_data
        if get_ogp_product_team_member(team_member_data) is not None
    ]


def _get_ogp_product(ogp_product_base: OgpProductBase) -> OgpProduct:
    ogp_api_product_info_response = get_ogp_api_product_info_response(
        ogp_product_base.path
    )

    product_team_members = _get_ogp_product_team_members(ogp_api_product_info_response)
    cost = _get_ogp_product_cost(ogp_api_product_info_response)
    return OgpProduct(
        path=ogp_product_base.path,
        logoUrl=ogp_product_base.logoUrl,
        name=ogp_product_base.name,
        cost=cost,
        team_members=product_team_members,
    )


def get_ogp_products() -> list[OgpProduct]:
    ogp_api_products_response = get_ogp_api_products_response()
    ogp_products_base = _get_ogp_products_base(ogp_api_products_response)
    print(ogp_products_base)
    return [
        _get_ogp_product(ogp_product_base) for ogp_product_base in ogp_products_base
    ]
