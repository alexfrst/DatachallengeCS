import os

import pandas as pd

from navitia_api_connector._requests import query_navitia, query_from_url


def _get_lines_data():
    lines = []

    response = query_navitia("fr-idf", "lines", {"depth": 0, "disable_disruption": True})
    next_page = [elem for elem in response["links"] if elem["type"] == "next"]

    for item in response["lines"]:
        lines.append(_parse_line_data(item))

    while len(next_page) > 0:
        response = query_from_url(next_page[0]["href"])
        next_page = [elem for elem in response["links"] if elem["type"] == "next"]

        for item in response["lines"]:
            lines.append(_parse_line_data(item))
    return lines


def _parse_line_data(item):
    relevant_columns = ["code", "name", "id"]
    relevant_info = {col.replace(".", "_"): item[col] for col in relevant_columns}
    return {**relevant_info, "type": item["physical_modes"][0]["name"].split(":")[-1]}


def download_lines_data():
    print("     Downloading lines data...")
    lines = _get_lines_data()
    df = pd.DataFrame(lines)
    if not os.path.exists("navitia_data"):
        os.mkdir("navitia_data")
    df.to_csv("navitia_data/lines.csv")


if __name__ == "__main__":
    download_lines_data()
