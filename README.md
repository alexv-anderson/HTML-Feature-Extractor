# Feature Counter

Simplified wrapper for [lxml](https://lxml.de/) which counts the number of features in an HTML document.

## Install/Setup
Execute `setup.bash` to create the virtual environment and install `lxml`.

## Use

1. Place the page which needs to be parsed into the `app/data` directory and name the file `index.html`.
1. Add features to be counted to the `features_to_count` property in `app/config/features.json`
1. Execute the script from the `app` directory by executing `python3 src/main.py`
1. View the output in `app/out.csv`

### Adding a Feature to Count
The features which will be counted are taken from the list given by the `features_to_count` property in `app/config/features.json`. The list contains objects with two properties
- **`name`** is the name of the feature and is used to identify the feature in the output `CSV` file.
- **`xpath`** is an [XPath](https://www.w3schools.com/xml/xml_xpath.asp) query which describes what should be counted.
```json
{
    "features_to_count": [
        {
            "name": "paragraphs",
            "xpath": "//p"
        },
        {
            "name": "anchors",
            "xpath": "//a"
        }
    ]
}
```


