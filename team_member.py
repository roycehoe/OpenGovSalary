import re
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup, NavigableString

PLACEHOLDER_URL = "https://www.open.gov.sg/people/charmaine"


@dataclass
class StaffMember:
    profile_picture: str
    name: str
    title: str
    join_date: str


def get_ogp_api_people_info_response(
    url: str,
) -> str:
    try:
        ogp_people_info_response = requests.get(url, timeout=5)
        return ogp_people_info_response.text
    except Exception:
        raise Exception  # To handle custom error here


def get_staff_info(ogp_api_people_info_response: str) -> StaffMember:
    soup = BeautifulSoup(ogp_api_people_info_response, features="html.parser")
    background_image_content: str = soup.find("div", {"class": "staff-pic"})["style"]
    _, profile_picture, _ = re.split("\(|\)", background_image_content)
    name: str = soup.find("div", {"class": "staff-name"}).get_text()
    title: str = soup.find("div", {"class": "staff-title"}).get_text()

    before_intro_tag: NavigableString = soup.find("div", {"class": "staff-heading"})
    intro_tag = before_intro_tag.find_next_sibling()
    join_date = intro_tag.find("strong").get_text()

    return StaffMember(profile_picture, name, title, join_date)


ogp_api_people_info_response = get_ogp_api_people_info_response(PLACEHOLDER_URL)
staff_info = get_staff_info(ogp_api_people_info_response)
print(staff_info)
