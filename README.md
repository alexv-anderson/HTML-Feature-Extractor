# Feature Counter

Simplified wrapper for [lxml](https://lxml.de/) which counts the number of features in an HTML document.

## Install/Setup
Execute `setup.bash` to create the virtual environment and install `lxml`.

## Standalone

1. Place the page which needs to be parsed into the `app/data` directory.
1. Add features to be counted to the `features_to_count` property in `app/config/features.json`
1. Execute the script from the `app` directory by executing `python3 src/extractor.py`
1. View the output in `app/out.csv`

## API

### Class

The `CountingFeatureExtractor` class provides a wrapper around the functions defined in `extractor.py` which structures the functions' use in a standard way. If you prefer to use the functions in a non-standard way, then review the instructions in the [Custom](#custom) section of this README.

0. _(Optional)_ create feature criteria in a `JSON` file.
0. Import the module using `import extractor`
0. Create an instance of the class
0. Define the features of interest:
    - The criteria to be extracted using can be defined using the constructor's parameters or the `load_extracted_features`, `add_meta_feature`, and `add_extracted_feature` methods.
    - **Extracted Features** are those which are extracted from `HTML` files using `XPath` queries.
    - **Meta Features** are those which provide context for the values after they have been extracted such as file name, file path, or URL.
0. Process files and strings using either the `accumulate_features_from_string`, `accumulate_features_from_bytes`, or `accumulate_features_from_file` methods while supplying meta features as necessary via the `meta_features` parameter.

### Custom

1. Create feature criteria `JSON` file _(described below)_.
1. Import the module using `import extractor`
1. Load the criteria defining the features using `load_feature_criteria()`
1. Process `HTML` data using one of the three methods below
   1. Process entire string of `ASCII` characters using `extract_features_from_string()`
   1. Process entire string of byte characters using `extract_features_from_bytes()`
   1. Process entire file using `extract_features_from_file()`

## Adding a Feature to Count
The features which will be counted are taken from the list given by the `features_to_count` property in `app/config/features.json`. The list contains objects with two required properties
- **`name`** is the name of the feature and is used to identify the feature in the output `CSV` file.
- **`xpath`** is an [XPath](https://www.w3schools.com/xml/xml_xpath.asp) query which describes what should be counted.

Additionally there are two optional properties which can be used to further refine the criteria.
- **`text_re_mode`** may be either `match` or `search`. The mode indicates which of the two methods from the [re](https://docs.python.org/3/library/re.html) module should be used.
- **`text_re_pattern`** is the pattern which will be given to either [re.match](https://docs.python.org/3/library/re.html#re.Pattern.match) or [re.search](https://docs.python.org/3/library/re.html#re.Pattern.search).

_Note: Both `text_re_mode` and `text_re_pattern` must be specified for either property to be used._
```json
{
    "features_to_count": [
        {
            "name": "paragraphs",
            "xpath": "//p",
            "text_re_mode": "search",
            "text_re_pattern": "phrase"
        },
        {
            "name": "anchors",
            "xpath": "//a"
        }
    ]
}
```


