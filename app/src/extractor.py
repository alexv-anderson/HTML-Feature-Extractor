import csv
import json
import os

from io import BytesIO, StringIO

from lxml import etree

def extract_features_from_string(feature_criteria, text):
    return extract_features_from_file(feature_criteria, StringIO(text))

def extract_features_from_bytes(feature_criteria, bytes_string):
    return extract_features_from_file(feature_criteria, BytesIO(bytes_string))

def extract_features_from_file(feature_criteria, source_file):
    html = etree.parse(source_file)
    data = {}
    for feature in feature_criteria["features_to_count"]:
        data[feature["name"]] = len(html.xpath(feature["xpath"]))
    return data

def extract_features_from_directory(feature_criteria, directory_path):
    data_rows = []
    for file_name in os.listdir(directory_path):
        if file_name.endswith(".html"):
            with open(os.path.join(directory_path, file_name), "r") as f:
                data = extract_features_from_file(feature_criteria, f)
                data["path"] = directory_path
                data["file"] = file_name
                data_rows.append(data)
    return data_rows

def load_feature_criteria(config_file_path):
    with open(config_file_path, "r") as f:
        return json.load(f)

if __name__ == "__main__":
    feature_criteria = load_feature_criteria("./config/features.json")

    with open("./out.csv", "w+") as o:
        field_names = ["path", "file"]
        for feature in feature_criteria["features_to_count"]:
            field_names.append(feature["name"])
        csv_out = csv.DictWriter(o, field_names)
        csv_out.writeheader()

        csv_out.writerows(extract_features_from_directory(feature_criteria, "./data"))