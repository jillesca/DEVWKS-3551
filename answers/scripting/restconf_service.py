import urllib3
import requests
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "http://localhost:8080"
USERNAME = "admin"
PASSWORD = "admin"


def establish_restconf_connection() -> requests.Session:
    http_headers = {
        "Accept": "application/yang-data+xml",
        "Content-Type": "application/yang-data+json",
    }
    session = requests.session()
    session.auth = HTTPBasicAuth(USERNAME, PASSWORD)
    session.headers.update(http_headers)
    session.verify = False
    return session


def send_restconf_request(
    restconf_session: requests.Session, request_path: str, request_data: str
) -> str:
    response = restconf_session.patch(
        BASE_URL + request_path, json=request_data
    )
    response.raise_for_status()
    return response.text, response.status_code


def add_dns_server_dry_run(
    service_name: str, device_name: str, server_address: str
) -> tuple[str, dict]:
    path = "/restconf/data?dry-run"
    data = _get_dns_server_payload(service_name, device_name, server_address)
    return path, data


def add_dns_server(
    service_name: str, device_name: str, server_address: str
) -> tuple[str, dict]:
    path = "/restconf/data"
    data = _get_dns_server_payload(service_name, device_name, server_address)
    return path, data


def _get_dns_server_payload(
    service_name: str, device_name: str, server_address: str
) -> str:
    """
    To get the data payload, add first an example manually,
    commit it, and then use 'display json' as below

    show running-config router | display json
    """
    return {
        "router:router": [
            {
                "name": service_name,
                "device": [device_name],
                "sys": {"ntp": {"server": [{"name": server_address}]}},
            }
        ]
    }


def display_parsed_response(
    parsed_data: BeautifulSoup, http_status_code: str
) -> None:
    print(f"{'#' * 20} Response received: {'#' * 20}")
    print(parsed_data.prettify())
    print(f"http status code: {http_status_code}")


def parse_xml(xml_data: str) -> BeautifulSoup:
    return BeautifulSoup(xml_data, "xml")


def main() -> None:
    SERVICE_NAME = "core"
    DEVICE_NAME = "core-rtr0"
    SERVER_ADDRESS = "9.9.9.9"

    session = establish_restconf_connection()

    ## Dry run
    path, data = add_dns_server_dry_run(
        service_name=SERVICE_NAME,
        device_name=DEVICE_NAME,
        server_address=SERVER_ADDRESS,
    )
    response, status_code = send_restconf_request(
        restconf_session=session, request_path=path, request_data=data
    )
    parsed_response = parse_xml(xml_data=response)
    display_parsed_response(
        parsed_data=parsed_response, http_status_code=status_code
    )

    # Apply
    path, data = add_dns_server(
        service_name=SERVICE_NAME,
        device_name=DEVICE_NAME,
        server_address=SERVER_ADDRESS,
    )
    response, status_code = send_restconf_request(
        restconf_session=session, request_path=path, request_data=data
    )
    parsed_response = parse_xml(xml_data=response)
    display_parsed_response(
        parsed_data=parsed_response, http_status_code=status_code
    )


if __name__ == "__main__":
    main()
