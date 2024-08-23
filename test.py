import requests
from bs4 import BeautifulSoup, Tag

from models import OgpProduct, OgpProductCost

OGP_PRODUCTS_URL = "https://products.open.gov.sg/"
OGP_BASE_URL = "https://open.gov.sg/"
DEFAULT_START_DATE = "2023-07-01"

SALARY_HTML_TAG = "Salary"
INFRASTRUCTURE_HTML_TAG = "Infrastructure"
CORPORATE_OVERHEAD_HTML_TAG = "Corporate Overhead"
EQUIPMENT_SOFTWARE_AND_OFFICE_HTML_TAG = "Equipment, Software & Office"
OTHERS_HTML_TAG = "Others"


def get_ogp_api_products_response(
    url: str = OGP_PRODUCTS_URL,
) -> str:
    try:
        ogp_products_response = requests.get(url, timeout=5)
        return ogp_products_response.text
    except Exception:
        raise Exception  # To handle custom error here


def get_ogp_api_product_info_response(
    url: str,
) -> str:
    try:
        ogp_product_info_response = requests.get(url, timeout=5)
        return ogp_product_info_response.text
    except Exception:
        raise Exception  # To handle custom error here


def get_ogp_repo_tags(a_tags: list[Tag]) -> list[Tag]:
    return a_tags[1:-4]


def get_ogp_products(ogp_api_products_response: str) -> list[OgpProduct]:
    ogp_repos: list[OgpProduct] = []

    soup = BeautifulSoup(ogp_api_products_response, features="html.parser")
    a_tags: list[Tag] = soup.find_all("a")
    ogp_repo_tags = get_ogp_repo_tags(a_tags)

    repo_links = [tag["href"] for tag in ogp_repo_tags]
    repo_logo_links = [tag.find("img")["src"] for tag in ogp_repo_tags]

    repo_name = [repo_link[1:] for repo_link in repo_links]

    for i in range(len(repo_links)):
        ogp_repos.append(
            OgpProduct(
                path=f"{OGP_PRODUCTS_URL[:-1]}{repo_links[i]}",
                logoUrl=f"{OGP_PRODUCTS_URL[:-1]}{repo_logo_links[i]}",
                name=repo_name[i],
            )
        )

    return ogp_repos


def get_ogp_product_cost_component(
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


def get_ogp_product_info(ogp_api_product_info_response: str) -> OgpProductCost:
    soup = BeautifulSoup(ogp_api_product_info_response, features="html.parser")
    return OgpProductCost(
        salary=get_ogp_product_cost_component(soup, SALARY_HTML_TAG),
        infrastructure=get_ogp_product_cost_component(soup, SALARY_HTML_TAG),
        corporate_overhead=get_ogp_product_cost_component(soup, SALARY_HTML_TAG),
        equipment_software_and_office=get_ogp_product_cost_component(
            soup, SALARY_HTML_TAG
        ),
        others=get_ogp_product_cost_component(soup, SALARY_HTML_TAG),
    )


def main():
    ogp_api_products_response = get_ogp_api_products_response()
    ogp_repos = get_ogp_products(ogp_api_products_response)
    ogp_product_info = get_ogp_api_product_info_response(ogp_repos[0].path)
    print(get_ogp_product_info(ogp_product_info))


main()
