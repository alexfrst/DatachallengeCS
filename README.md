# Datachallenge CentraleSupélex x Illuin x Keolis

You can find the maintainers in the right tab

## Project architecture

Here is the folder structure for this project

```
├───raw_data
├───data-analysis
├───utils
├───raw_data_handling
├───navitia_api_connector
├───raw_data_filtered
├───navitia_data
└───raw_data_aggregated
```

- `raw_data` contains all the s3 bucket data.
- `data-analysis` contains all the processing done on the chaos csv, **mainly cleaning**, **imputation** and **classification**.
- `utils` contains utilities function, mainly logging functions for the moment.
- `raw_data_handling` contains python files that are used to transform raw_data into filtered data into aggregated_data.
- `navitia_api_connector` connects to navitia api in order to fetch and enrich all the logs data.
- `raw_data_filtered` contains filtered raw_files.
- `navitia_data` contains snapshots of the downloaded data from navitia.
- `raw_data_filtered` contains aggregated raw_files.

# TODO
- Models
- Demonstrator
- Docstring