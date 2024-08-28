import re
from datetime import datetime
from typing import Optional

from bs4 import BeautifulSoup, NavigableString

from gateway import OGP_BASE_URL, get_ogp_api_people_info_response
from models import OgpTeamMember

PLACEHOLDER_URL = "https://www.open.gov.sg/people/charmaine"


def get_staff_profile_picture(ogp_api_people_info_response_soup: BeautifulSoup) -> str:
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

    return f"{OGP_BASE_URL[:-1]}{profile_picture_subdirectory}"


def _get_staff_name(
    ogp_api_people_info_response_soup: BeautifulSoup, default_name: str
) -> str:
    name = ogp_api_people_info_response_soup.find("div", {"class": "staff-name"})
    if name is None:
        return default_name
    return name.get_text()


def _get_staff_title(ogp_api_people_info_response_soup: BeautifulSoup) -> str:
    name = ogp_api_people_info_response_soup.find("div", {"class": "staff-title"})
    if name is None:
        return ""
    return name.get_text()


def _get_staff_join_date(
    ogp_api_people_info_response_soup: BeautifulSoup,
) -> Optional[datetime]:
    before_intro_tag = ogp_api_people_info_response_soup.find(
        "div", {"class": "staff-heading"}
    )
    if before_intro_tag is None:
        return None
    intro_tag = before_intro_tag.find_next_sibling()
    if intro_tag is None:
        return None
    join_date_tag = intro_tag.find("strong")
    if join_date_tag is None:
        return None
    if isinstance(join_date_tag, int):
        return None

    join_date_content = join_date_tag.get_text()
    join_date = datetime.strptime(join_date_content, "%B %d, %Y")
    return join_date


def get_team_member_info(team_member_url: str, default_name: str) -> OgpTeamMember:
    ogp_api_people_info_response = get_ogp_api_people_info_response(team_member_url)
    soup = BeautifulSoup(ogp_api_people_info_response, features="html.parser")

    profile_picture = get_staff_profile_picture(soup)
    name = _get_staff_name(soup, default_name)
    title = _get_staff_title(soup)
    join_date = _get_staff_join_date(soup)

    return OgpTeamMember(
        profile_picture=profile_picture, name=name, title=title, join_date=join_date
    )
