import requests

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


def get_ogp_api_people_info_response(
    url: str,
) -> str:
    try:
        ogp_people_info_response = requests.get(url, timeout=5)
        return ogp_people_info_response.text
    except Exception:
        raise Exception  # To handle custom error here
