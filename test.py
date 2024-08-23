import requests
from bs4 import BeautifulSoup, Tag

from models import OgpProduct, OgpProductCost

OGP_PRODUCTS_URL = "https://products.open.gov.sg/"
OGP_BASE_URL = "https://open.gov.sg/"
DEFAULT_START_DATE = "2023-07-01"


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


def get_ogp_product_info(ogp_api_product_info_response: str) -> OgpProductCost:
    soup = BeautifulSoup(ogp_api_product_info_response, features="html.parser")
    salary = (
        soup.find("div", string="Salary")
        .find_previous_sibling("div")
        .get_text(strip=True)
    )[1:].replace(",", "")
    infrastructure = (
        soup.find("div", string="Infrastructure")
        .find_previous_sibling("div")
        .get_text(strip=True)
    )[1:].replace(",", "")
    corporate_overhead = (
        soup.find("div", string="Corporate Overhead")
        .find_previous_sibling("div")
        .get_text(strip=True)
    )[1:].replace(",", "")
    equipment_software_and_office = (
        soup.find("div", string="Equipment, Software & Office")
        .find_previous_sibling("div")
        .get_text(strip=True)
    )[1:].replace(",", "")
    others = (
        soup.find("div", string="Others")
        .find_previous_sibling("div")
        .get_text(strip=True)
    )[1:].replace(",", "")
    return OgpProductCost(
        salary=int(salary),
        infrastructure=int(infrastructure),
        corporate_overhead=int(corporate_overhead),
        equipment_software_and_office=int(equipment_software_and_office),
        others=int(others),
    )


def main():
    ogp_api_products_response = get_ogp_api_products_response()
    ogp_repos = get_ogp_products(ogp_api_products_response)
    ogp_product_info = get_ogp_api_product_info_response(ogp_repos[0].path)
    print(get_ogp_product_info(ogp_product_info))


main()
