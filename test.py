from bs4 import BeautifulSoup, Tag
import requests

from models import OgpApiRepoResponse

OGP_PRODUCTS_URL = "https://products.open.gov.sg/"
OGP_BASE_URL = "https://open.gov.sg/"
DEFAULT_START_DATE = "2023-07-01"


def get_ogp_api_products_response(
    url: str = OGP_PRODUCTS_URL,
) -> str:
    try:
        ogp_repos_response = requests.get(url)
        return ogp_repos_response.text
    except Exception:
        raise Exception  # To handle custom error here


def get_ogp_repo_tags(a_tags: list[Tag]) -> list[Tag]:
    return a_tags[1:-4]


def get_ogp_repos(ogp_api_products_response: str) -> list[OgpApiRepoResponse]:
    ogp_repos: list[OgpApiRepoResponse] = []

    soup = BeautifulSoup(ogp_api_products_response, features="html.parser")
    a_tags: list[Tag] = soup.find_all("a")
    ogp_repo_tags = get_ogp_repo_tags(a_tags)

    repo_links = [tag["href"] for tag in ogp_repo_tags]
    repo_logo_links = [tag.find("img")["src"] for tag in ogp_repo_tags]
    repo_name = [repo_link[1:] for repo_link in repo_links]

    for i in range(len(repo_links)):
        ogp_repos.append(
            OgpApiRepoResponse(
                path=f"{OGP_BASE_URL}{repo_links[i]}",
                logoUrl=f"{OGP_PRODUCTS_URL[:-1]}{repo_logo_links[i]}",
                name=repo_name[i],
            )
        )

    return ogp_repos


ogp_api_products_response = get_ogp_api_products_response()
print(get_ogp_repos(ogp_api_products_response))
