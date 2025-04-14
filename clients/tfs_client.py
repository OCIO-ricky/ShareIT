# cdc-shareit-scan/clients/tfs_client.py

import requests
import os
import yaml
from dotenv import load_dotenv
from base64 import b64encode
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Load configuration from config.yaml
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

TFS_BASE_URL = config["tfs"]["base_url"]
TFS_PROJECT = config["tfs"]["project"]
TFS_USERNAME = os.getenv(config["tfs"]["username_env_var"])
TFS_PAT = os.getenv(config["tfs"]["token_env_var"])

def fetch_tfs_repos():
    repos = []

    url = f"{TFS_BASE_URL}/{TFS_PROJECT}/_apis/git/repositories?api-version=6.0"

    auth = (TFS_USERNAME, TFS_PAT)

    headers = {
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers, auth=auth)

    if response.status_code != 200:
        print(f"Failed to fetch TFS repos: {response.status_code}")
        return repos

    data = response.json()
    values = data.get("value", [])

    for repo in values:
        repos.append({
            "name": repo["name"],
            "description": repo.get("description", ""),
            "url": repo["webUrl"],
            "usageType": "governmentWideReuse",
            "tags": ["tfs", repo["project"]["name"]],
            "contact": f"{repo['project']['name'].lower()}@cdc.gov",
            "created": "2023-01-01",  # Azure DevOps REST API doesn't provide creation date directly
            "lastModified": datetime.today().strftime('%Y-%m-%d')  # Optional improvement: Use commits API for last activity date
        })

    return repos


if __name__ == "__main__":
    import json

    repos = fetch_tfs_repos()
    print(json.dumps(repos, indent=2))
