import csv
import json
import os

from io import BytesIO, StringIO

from lxml import etree

class CountingFeatureExtractor:
    def __init__(self, config_file_path=None):
        self._feature_criteria = {}
        self.feature_counts = []

        if config_file_path is not None:
            self.load_features(config_file_path)
    
    def load_features(self, config_file_path):
        load_feature_criteria(config_file_path, self._feature_criteria)
    
    def add_feature(self, name, xpath):
        if name in self._feature_criteria:
            raise ValueError("There is already a feature named '%s'." % name)
        if xpath is None:
            raise ValueError("An XPath expression is required for criteria.")
        put_feature_criterion(self._feature_criteria, name, xpath)

    def accumulate_features_from_string(self, text):
        self.feature_counts.append(extract_features_from_string(self._feature_criteria, text))

    def accumulate_features_from_bytes(self, byte_string):
        self.feature_counts.append(extract_features_from_bytes(self._feature_criteria, byte_string))
    
    def accumulate_features_from_file(self, source_file):
        self.feature_counts.append(extract_features_from_file(self._feature_criteria, source_file))

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
    for feature_name in feature_criteria:
        data[feature_name] = len(html.xpath(feature_criteria[feature_name]))

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

def load_feature_criteria(config_file_path, feature_criteria={}):
    """
    Loads criteria from the JSON file described in the path and returns the dictionary.
    The criteria define the features to search for.
    """
    with open(config_file_path, "r") as f:
        for feature in json.load(f)["features_to_count"]:
            put_feature_criterion(feature_criteria, feature["name"], feature["xpath"])

    return feature_criteria

def put_feature_criterion(feature_criteria, name, xpath):
    feature_criteria[name] = xpath

if __name__ == "__main__":
    extractor = CountingFeatureExtractor("./config/features.json")

    with open("./out.csv", "w+") as o:
        field_names = []
        for feature_name in extractor._feature_criteria:
            field_names.append(feature_name)
        csv_out = csv.DictWriter(o, field_names)
        csv_out.writeheader()

        extractor.accumulate_features_from_file("./data/index.html")

        csv_out.writerows(extractor.feature_counts)