# cdc-shareit-scan/clients/bitbucket_client.py

import requests
import os
import yaml
from dotenv import load_dotenv
from datetime import datetime
import json
import argparse

# Load environment variables
load_dotenv()

# Load configuration
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

BITBUCKET_BASE_URL = config["bitbucket"]["base_url"]
BITBUCKET_PROJECT = config["bitbucket"]["project"]
BITBUCKET_USERNAME = os.getenv(config["bitbucket"]["username_env_var"])
BITBUCKET_TOKEN = os.getenv(config["bitbucket"]["token_env_var"])

def fetch_bitbucket_repos():
    headers = {
        "Accept": "application/json"
    }

    repos = []
    start = 0
    limit = 100

    while True:
        url = f"{BITBUCKET_BASE_URL}/projects/{BITBUCKET_PROJECT}/repos?limit={limit}&start={start}"
        response = requests.get(url, headers=headers, auth=(BITBUCKET_USERNAME, BITBUCKET_TOKEN))

        if response.status_code != 200:
            print(f"Failed to fetch Bitbucket repos: {response.status_code}")
            break

        data = response.json()
        values = data.get("values", [])
        if not values:
            break

        for repo in values:
            updated_epoch = repo.get("updatedDate", 0) // 1000
            last_modified = datetime.utcfromtimestamp(updated_epoch).strftime('%Y-%m-%d') if updated_epoch > 0 else datetime.today().strftime('%Y-%m-%d')

            repos.append({
                "name": repo["name"],
                "description": repo.get("description", ""),
                "url": repo["links"]["html"]["href"],
                "usageType": "governmentWideReuse",
                "tags": ["bitbucket"],
                "contact": f"{repo['project']['key'].lower()}@cdc.gov",
                "created": "2023-01-01",
                "lastModified": last_modified
            })

        if data.get("isLastPage", True):
            break
        start = data.get("nextPageStart", start + limit)

    return repos

def generate_code_json(repos, output_file):
    data = {
        "releases": repos
    }
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=str, default='code.json', help='Output file name')
    args = parser.parse_args()

    repos = fetch_bitbucket_repos()
    generate_code_json(repos, args.output)
    print(f"Generated {args.output} successfully.")
