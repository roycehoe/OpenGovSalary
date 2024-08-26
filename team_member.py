from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup

PLACEHOLDER_URL = "https://www.open.gov.sg/people/charmaine"


@dataclass
class StaffMember:
    pic: str
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


def get_staff_info(ogp_api_people_info_response: str):
    soup = BeautifulSoup(ogp_api_people_info_response, features="html.parser")
    test = soup.find("div", {"class": "staff-pic"})
    # staff_main_info = soup.find("div", {"class": "staff-main"})

    # test = staff_main_info.find("div", {"class": "staff-pic"})
    return test

    return staff_main_info


# def get_ogp_product_cost_component(
#     ogp_api_product_info_response_soup: BeautifulSoup, cost_component: str
# ) -> float:
#     cost_component_tag = ogp_api_product_info_response_soup.find(
#         "div", string=cost_component
#     )
#     if cost_component_tag is None:
#         return 0
#     cost_component_number_tag = cost_component_tag.find_previous_sibling("div")
#     if cost_component_number_tag is None:
#         return 0
#     cost_component_html_value = cost_component_number_tag.get_text(strip=True)
#     return int(cost_component_html_value[1:].replace(",", ""))


ogp_api_people_info_response = get_ogp_api_people_info_response(PLACEHOLDER_URL)
staff_info = get_staff_info(ogp_api_people_info_response)
print(staff_info)
