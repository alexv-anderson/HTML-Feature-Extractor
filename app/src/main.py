import csv
import json
from lxml import etree

if __name__ == "__main__":
    with open("./config/features.json", "r") as f, open("./out.csv", "w+") as o:
        json_data = json.load(f)

        field_names = []
        for feature in json_data["features_to_count"]:
            field_names.append(feature["name"])
        csv_out = csv.DictWriter(o, field_names)
        csv_out.writeheader()

        html = etree.HTML("./data/index.html")
        data = {}
        for feature in json_data["features_to_count"]:
            data[feature["name"]] = len(html.xpath(feature["xpath"]))
        csv_out.writerow(data)
