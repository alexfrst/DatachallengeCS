import requests
from navitia_api_connector.credentials import NAVITIA_ACCESS_TOKEN

url = "https://api.navitia.io/v1/coverage"
headers = {"Authorization": NAVITIA_ACCESS_TOKEN}
default_params = {"count": 1000}


def query_navitia(region, endpoint, params):
    merged_params = {**default_params, **params}
    request = requests.get(f"{url}/{region}/{endpoint}",
                           params=merged_params, headers=headers)
    return request.json()

def query_from_url(url):
    return requests.get(url,headers=headers).json()
