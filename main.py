from navitia_api_connector.stop_points import download_stop_points
from navitia_api_connector.stop_areas import download_stop_areas
from navitia_api_connector.lines import download_lines_data
import raw_data_handling.filtering as filtering
import raw_data_handling.aggregator as aggregation
import os

if os.path.exists("navitia_data"):
    print("Navitia data already downloaded")
else:
    print("Navitia theorical data not found")
    download_stop_points()
    download_lines_data()
    download_stop_areas()
    print("Downloaded theorical data successfully")

if os.path.exists("compressed"):
    print("Compressed data already downloaded")
else:
    print("No compressed data found, compressing raw_data")
    filtering.process_all_files()

if os.path.exists("raw_data_aggregated"):
    print("Aggregated data already treated")
else:
    print("No aggregated data found, aggregating filtered_data")
    aggregation.process_all_files()
