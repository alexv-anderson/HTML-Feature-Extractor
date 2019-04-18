import csv
import json
import os

from io import StringIO

from lxml import etree

def extract_features_from_string(json_data, text):
    return extract_features_from_file(json_data, StringIO(text))

def extract_features_from_file(json_data, source_file):
    html = etree.parse(source_file)
    data = {}
    for feature in json_data["features_to_count"]:
        data[feature["name"]] = len(html.xpath(feature["xpath"]))
    return data

def extract_features_from_directory(json_data, directory_path):
    data_rows = []
    for file_name in os.listdir(directory_path):
        if file_name.endswith(".html"):
            with open(os.path.join(directory_path, file_name), "r") as f:
                data = extract_features_from_file(json_data, f)
                data["path"] = directory_path
                data["file"] = file_name
                data_rows.append(data)
    return data_rows

if __name__ == "__main__":
    with open("./config/features.json", "r") as f, open("./out.csv", "w+") as o:
        json_data = json.load(f)

        field_names = ["path", "file"]
        for feature in json_data["features_to_count"]:
            field_names.append(feature["name"])
        csv_out = csv.DictWriter(o, field_names)
        csv_out.writeheader()

        csv_out.writerows(extract_features_from_directory(json_data, "./data"))