import os

import pandas as pd

from navitia_api_connector._requests import query_navitia, query_from_url


def _get_stop_areas_data():
    stop_points = []

    response = query_navitia("fr-idf", "stop_areas", {"depth": 3, "disable_disruption": True})
    next_page = [elem for elem in response["links"] if elem["type"] == "next"]

    for item in response["stop_areas"]:
        stop_points.append(_parse_line_data(item))

    while len(next_page) > 0:
        response = query_from_url(next_page[0]["href"])
        next_page = [elem for elem in response["links"] if elem["type"] == "next"]

        for item in response["stop_areas"]:
            stop_points.append(_parse_line_data(item))
    return stop_points


def _parse_line_data(item):
    relevant_columns = ["label", "name", "id"]
    relevant_fields = {col: item[col] for col in relevant_columns}
    relevant_fields.update({"lines": [line["id"] for line in item["lines"]]})
    return relevant_fields


def download_stop_areas():
    print("     Downloading stop_areas data...")
    stop_points = _get_stop_areas_data()
    df = pd.DataFrame(stop_points)
    if not os.path.exists("navitia_data"):
        os.mkdir("navitia_data")
    df.to_csv("navitia_data/stop_areas.csv")


if __name__ == "__main__":
    download_stop_areas()
