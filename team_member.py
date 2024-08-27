import re
from dataclasses import dataclass
from datetime import datetime
from test import OGP_BASE_URL

import requests
from bs4 import BeautifulSoup, NavigableString

PLACEHOLDER_URL = "https://www.open.gov.sg/people/charmaine"


@dataclass
class StaffInfo:
    profile_picture: str
    name: str
    title: str
    join_date: datetime


def get_ogp_api_people_info_response(
    url: str,
) -> str:
    try:
        ogp_people_info_response = requests.get(url, timeout=5)
        return ogp_people_info_response.text
    except Exception:
        raise Exception  # To handle custom error here


def get_profile_picture(ogp_api_people_info_response_soup: BeautifulSoup) -> str:
    background_image_content = ogp_api_people_info_response_soup.find(
        "div", {"class": "staff-pic"}
    )
    if background_image_content is None:
        return ""
    if isinstance(background_image_content, NavigableString):
        return ""
    background_image_content.get("style")
    background_image_content_style = background_image_content.get("style")
    if background_image_content_style is None:
        return ""
    if isinstance(background_image_content_style, list):
        return ""

    _, profile_picture_subdirectory, _ = re.split(
        r"\(|\)", background_image_content_style
    )

    return f"{OGP_BASE_URL}{profile_picture_subdirectory}"


def get_staff_info(ogp_api_people_info_response: str) -> StaffInfo:
    soup = BeautifulSoup(ogp_api_people_info_response, features="html.parser")

    profile_picture = get_profile_picture(soup)

    name: str = soup.find("div", {"class": "staff-name"}).get_text()
    title: str = soup.find("div", {"class": "staff-title"}).get_text()

    before_intro_tag: NavigableString = soup.find("div", {"class": "staff-heading"})
    intro_tag = before_intro_tag.find_next_sibling()
    join_date_content = intro_tag.find("strong").get_text()
    join_date = datetime.strptime(join_date_content, "%B %d, %Y")

    return StaffInfo(profile_picture, name, title, join_date)


def main():
    ogp_api_people_info_response = get_ogp_api_people_info_response(PLACEHOLDER_URL)
    soup = BeautifulSoup(ogp_api_people_info_response, features="html.parser")
    print(get_profile_picture(soup))


main()
