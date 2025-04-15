# cdc-shareit-scan/code_json_generator.py
#
# $> python code_json_generator.py --input_dir /path/to/repo-jsons/ --output /var/www/html/code.json
#
#
# This will be auto-generated but here’s a sample structure:
#
# {
# "agency": "Centers for Disease Control and Prevention",
# "organization": {
#   "acronym": "CDC",
#   "name": "Centers for Disease Control and Prevention",
#   "website": "https://www.cdc.gov",
#   "codeUrl": "https://www.cdc.gov/code.json"
# },
# "version": "2.0.0",
# "measurementType": {
#   "agencyWidePolicy": true,
#   "complianceBaseline": true,
#   "customPolicy": false
# },
# "releases": [
#   {
#     "name": "CDC Data Visualization Toolkit",
#     "description": "Internal visualization framework for public health reporting.",
#     "url": "https://github.com/cdcgov/dataviz-toolkit",
#     "permissions": {
#       "usageType": "openSource",
#       "exemptionText": "N/A"
#     },
#     "tags": ["visualization", "python", "publichealth"],
#     "contact": {
#       "email": "opensource@cdc.gov"
#     },
#     "date": {
#       "created": "2023-09-01",
#      "lastModified": "2024-01-12"
#    }
#   }
# ]
# }

import json
import os
import yaml
from datetime import datetime
from glob import glob

# Load configuration
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

def collect_all_metadata(folder_path):
    all_releases = []
    for path in glob(os.path.join(folder_path, "*.json")):
        with open(path) as f:
            try:
                data = json.load(f)
                all_releases.extend(data.get("releases", []))
            except Exception as e:
                print(f"Error reading {path}: {e}")
    return all_releases

def generate_merged_code_json(releases, output_path="code.json"):
    code_json = {
        "agency": "Centers for Disease Control and Prevention",
        "organization": {
            "acronym": "CDC",
            "name": "Centers for Disease Control and Prevention",
            "website": "https://www.cdc.gov",
            "codeUrl": "https://www.cdc.gov/code.json"
        },
        "version": "2.0.0",
        "measurementType": {
            "agencyWidePolicy": True,
            "complianceBaseline": True,
            "customPolicy": False
        },
        "releases": releases
    }
    with open(output_path, "w") as f:
        json.dump(code_json, f, indent=2)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', type=str, required=True, help='Directory containing individual code.json files')
    parser.add_argument('--output', type=str, default='code.json', help='Output file name')
    args = parser.parse_args()

    all_metadata = collect_all_metadata(args.input_dir)
    generate_merged_code_json(all_metadata, args.output)
    print(f"Merged code.json generated successfully at {args.output}")
