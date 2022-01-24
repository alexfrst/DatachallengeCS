import glob
import json
import os
import re
import shutil

import pandas as pd
from tqdm import tqdm


def process_all_files():
    print("Deleting existing aggregated files")
    if os.path.exists("aggregated"):
        shutil.rmtree('aggregated')
    filenames = [
        *glob.glob('raw_data_filtered/**/*.compressed', recursive=True),
        # *glob.glob('raw_data/2020/**/*.gz', recursive=True)
    ]
    print("Starting aggregation of filtered files")
    for filename in tqdm(filenames):
        _aggregate_file(filename)

    filenames = [
        *glob.glob('raw_data_aggregated/**/*.csv', recursive=True),
        # *glob.glob('raw_data/2020/**/*.gz', recursive=True)
    ]

    dfs = []
    print("Aggregating all files into one")
    for filename in tqdm(filenames):
        df = pd.read_csv(filename, index_col=None, header=0)
        dfs.append(df)

    pd.concat(dfs, axis=0, ignore_index=True).to_csv("raw_data_aggregated/aggregated_final.csv")


def load_object_mapping():
    stop_areas = pd.read_csv("navitia_data/stop_areas.csv")
    stop_areas.set_index("id", inplace=True)

    stop_points = pd.read_csv("navitia_data/stop_points.csv")
    stop_points.set_index("id", inplace=True)

    lines = pd.read_csv("navitia_data/lines.csv")
    lines.set_index("id", inplace=True)

    values_to_str = {**stop_points["lines"].to_dict(), **stop_areas["lines"].to_dict(), **stop_areas["lines"].to_dict()}
    return {key: eval(values_to_str[key]) for key in values_to_str}


entity_mapping = load_object_mapping()


def _aggregate_file(input_filename):
    data = []
    with open(input_filename, 'r') as input_file:
        for index, line in enumerate(input_file):
            parsed_line = json.loads(line)
            matched_patterns = re.findall(r"line:\w+:\w+|stop_area:\w+:\w+|stop_point:\w+:\w+", parsed_line["path"])
            for group in matched_patterns:
                data.append({"datetime": pd.Timestamp(parsed_line["request_date"], unit='s'), "entity": group})

                # for item in parsed_line["path"].split("/"):
                #     if "line:" in parsed_line["path"] or "stop_area:" in parsed_line["path"] or "stop_point:" in parsed_line["path"]:
                #         data.append({"datetime":pd.Timestamp(parsed_line["request_date"],unit='s'), "entity":item})
            else:
                if "parameters" in parsed_line:
                    for item in parsed_line["parameters"]:
                        if item["key"] in ["from", "to"]:
                            if re.match(r"line|stop_area|stop_point", item["value"]):
                                data.append({"datetime": pd.Timestamp(parsed_line["request_date"], unit='s'),
                                             "entity": item["value"]})

    directory = "raw_data_aggregated/" + "/".join(input_filename.split("\\")[1:-1])
    output_filename = ("raw_data_aggregated/" + "/".join(input_filename.split("\\")[1:])).split(".")[0] + "aggreggated.csv"

    if not os.path.exists(directory):
        os.makedirs(directory)
    df = pd.DataFrame(data)
    df["datetime"] = df["datetime"].dt.round("1h")
    df["entity"] = df["entity"].map(entity_mapping)
    df.explode("entity").groupby(["entity", "datetime"]).size().reset_index().to_csv(output_filename)
# _aggregate_file("raw_data_aggregated/2021/12/idfm_20211201.json.log.gz.aggregated")
