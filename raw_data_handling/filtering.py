import glob
import gzip
import json
import os
import shutil

from tqdm import tqdm

from utils.logging import warning

apis = set()
interesting_entries = ['v1.route_schedules', 'v1.stop_schedules', 'v1.journeys', 'v1.arrivals', 'v1.departures']
not_interesting_entries = ['v1.addresses.id', 'v1.stop_areas.collection', 'v1.networks.id', 'v1.status',
                           'v1.stop_points.id', 'v1.stop_points.collection', 'v1.datasets.collection', 'v1.place_uri',
                           'v1.places_nearby', 'v1.lines.collection', 'v1.routes.collection', 'v1.pt_objects',
                           'v1.commercial_modes.collection', 'v1.coverage', 'v1.disruptions.id', 'v1.lines.id',
                           'v1.stop_areas.id', 'v1.disruptions.collection', 'v1.pois.id', 'v1.places',
                           'v1.networks.collection', 'v1.coord.id', 'v1.routes.id', 'v1.companies.collection']


def process_all_files():
    print("Deleting existing compressed files")
    if os.path.exists("compressed"):
        shutil.rmtree('compressed')
    filenames = [
        *glob.glob('raw_data/simplified/logs/**/*.gz', recursive=True),
        # *glob.glob('raw_data/2020/**/*.gz', recursive=True)
    ]
    print("Starting compression of raw files")
    for filename in tqdm(list(reversed(filenames))):
        _compress_file(filename)


def _compress_file(input_filename):
    directory = "raw_data_filtered/" + "/".join(input_filename.split("\\")[1:-1])
    output_filename = "raw_data_filtered/" + "/".join(input_filename.split("\\")[1:]) + ".compressed"

    if not os.path.exists(directory):
        os.makedirs(directory)

    buffer = []
    with open(output_filename, "a") as output_file:
        with gzip.open(input_filename, 'rb') as input_file:
            for index, line in enumerate(input_file):
                parsed_line = json.loads(line)
                if parsed_line["api"] in interesting_entries:
                    buffer.append(line.decode("utf-8"))
                    if len(buffer) > 500000:
                        output_file.writelines(buffer)
                        buffer = []
                    continue

                if parsed_line["api"] in not_interesting_entries:
                    continue

                warning(f'Unhandled API endpoint, consider adding "{parsed_line["api"]}"')
            output_file.writelines(buffer)
            buffer = []


if __name__ == "__main__":
    process_all_files()
