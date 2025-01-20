import urllib3
import requests
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "http://localhost:8080"
USERNAME = "admin"
PASSWORD = "admin"


def establish_restconf_connection() -> requests.Session:
    session = requests.session()
    session.auth = HTTPBasicAuth(USERNAME, PASSWORD)
    session.headers.update({"Accept": "application/yang-data+xml"})
    session.verify = False
    return session


def send_restconf_request(
    restconf_session: requests.Session, request_path: str
) -> str:
    response = restconf_session.get(url=BASE_URL + request_path)
    response.raise_for_status()
    return response.text


def parse_xml(xml_data: str) -> dict:
    return BeautifulSoup(xml_data, "xml")


def get_xr_device_hostname_rest_path(device_name: str) -> str:
    return f"/restconf/data/tailf-ncs:devices/device={device_name}/config/tailf-ned-cisco-ios-xr:hostname"


def main() -> None:
    DEVICE_NAME = "core-rtr0"

    session = establish_restconf_connection()
    path = get_xr_device_hostname_rest_path(device_name=DEVICE_NAME)
    response = send_restconf_request(
        restconf_session=session, request_path=path
    )
    parsed_response = parse_xml(xml_data=response)

    print(f"{'#' * 20} xml received: {'#' * 20}")
    print(parsed_response.prettify())
    print(f"{'#' * 20} text received: {'#' * 20}")
    print(parsed_response.text)


if __name__ == "__main__":
    main()
