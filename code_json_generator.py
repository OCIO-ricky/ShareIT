# cdc-shareit-scan/code_json_generator.py
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

# cdc-shareit-scan/code_json_generator.py

import json
import yaml
import os
from datetime import datetime
from clients.github_client import fetch_github_repos
from clients.gitlab_client import fetch_gitlab_repos
from clients.bitbucket_client import fetch_bitbucket_repos
from clients.tfs_client import fetch_tfs_repos


def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)


def build_code_json():
    config = load_config()

    default_contact = config["global"].get("default_contact_email", "opensource@cdc.gov")
    default_usage_type = config["global"].get("default_usage_type", "governmentWideReuse")

    releases = []

    github_repos = fetch_github_repos()
    gitlab_repos = fetch_gitlab_repos()
    bitbucket_repos = fetch_bitbucket_repos()
    tfs_repos = fetch_tfs_repos()

    all_repos = github_repos + gitlab_repos + bitbucket_repos + tfs_repos

    for repo in all_repos:
        releases.append({
            "name": repo["name"],
            "description": repo.get("description", "No description available."),
            "url": repo["url"],
            "permissions": {
                "usageType": repo.get("usageType", default_usage_type),
                "exemptionText": repo.get("exemptionText", "N/A")
            },
            "tags": repo.get("tags", []),
            "contact": {
                "email": repo.get("contact", default_contact)
            },
            "date": {
                "created": repo.get("created", "2023-01-01"),
                "lastModified": repo.get("lastModified", datetime.today().strftime('%Y-%m-%d'))
            }
        })

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

    with open("code.json", "w") as f:
        json.dump(code_json, f, indent=2)


if __name__ == "__main__":
    build_code_json()
