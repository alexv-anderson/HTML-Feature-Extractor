import csv
import json
import os

from io import BytesIO, StringIO

from lxml import etree

def extract_features_from_string(feature_criteria, text):
    """
    Extract features from an ASCII string.
    Returns a dictionary of the number of matches for each criteria. The keys of the
    dictionary are the names of the criteria.
    """
    return extract_features_from_file(feature_criteria, StringIO(text))

def extract_features_from_bytes(feature_criteria, bytes_string):
    """
    Extract features from a byte string.
    Returns a dictionary of the number of matches for each criteria. The keys of the
    dictionary are the names of the criteria.
    """
    return extract_features_from_file(feature_criteria, BytesIO(bytes_string))

def extract_features_from_file(feature_criteria, source_file):
    """
    Extract features from a file like object.
    Returns a dictionary of the number of matches for each criteria. The keys of the
    dictionary are the names of the criteria.
    """

    # Parse the HTML
    html = etree.parse(source_file)

    # Store the number of matches in the file for each criteria's XPath query
    data = {}
    for feature in feature_criteria["features_to_count"]:
        data[feature["name"]] = len(html.xpath(feature["xpath"]))

    return data

def extract_features_from_directory(feature_criteria, directory_path):
    """
    Extract features from all HTML files in a directory
    Returns a list of dictionaries. Each dicationary contains the number of matches for each
    criteria. The keys of the dictionaries are the names of the criteria.
    NOTE: The keys "path" and "file" are dynamically added to help track the sources
    """
    data_rows = []

    for file_name in os.listdir(directory_path):
        # Only extract data from HTML files
        if file_name.endswith(".html"):
            with open(os.path.join(directory_path, file_name), "r") as f:
                data = extract_features_from_file(feature_criteria, f)
                data["path"] = directory_path
                data["file"] = file_name
                data_rows.append(data)

    return data_rows

def load_feature_criteria(config_file_path):
    """
    Loads the criteria which define the features to search for.
    Returns a dictionary which resulted from loading the JSON file at the given path.
    """
    with open(config_file_path, "r") as f:
        return json.load(f)

if __name__ == "__main__":
    # Load criteria
    feature_criteria = load_feature_criteria("./config/features.json")

    with open("./out.csv", "w+") as o:
        # Add "path" and "file" fields
        field_names = ["path", "file"]
        for feature in feature_criteria["features_to_count"]:
            field_names.append(feature["name"])
        csv_out = csv.DictWriter(o, field_names)
        csv_out.writeheader()

        csv_out.writerows(extract_features_from_directory(feature_criteria, "./data"))