import json
import requests
from pydantic import BaseModel

OGP_REPOS_URL = "https://products.open.gov.sg/api/repos"

class OgpRepo(BaseModel):
    path: str
    logoUrl: str
    name: str


def get_ogp_repos(url=OGP_REPOS_URL) -> list[OgpRepo]:
    try:
        ogp_repos_response = requests.get(url)
        return [OgpRepo(**ogp_repo) for ogp_repo in ogp_repos_response.json()]
    except Exception:
        raise Exception # To handle custom error here

print(get_ogp_repos())
