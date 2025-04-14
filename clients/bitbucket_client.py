# cdc-shareit-scan/clients/bitbucket_client.py

import requests
import os
import yaml
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load configuration from config.yaml
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
            repos.append({
                "name": repo["name"],
                "description": repo.get("description", ""),
                "url": repo["links"]["html"]["href"],
                "usageType": "governmentWideReuse",  # Internal by default
                "tags": ["bitbucket"],
                "contact": f"{repo['project']['key'].lower()}@cdc.gov",
                "created": "2023-01-01",  # Bitbucket Server API doesn't provide this
                "lastModified": repo.get("updatedDate", 0) // 1000  # Epoch to YYYY-MM-DD
            })

        if data.get("isLastPage", True):
            break
        start = data.get("nextPageStart", start + limit)

    return repos


if __name__ == "__main__":
    import json
    from datetime import datetime

    repos = fetch_bitbucket_repos()
    # Convert epoch to readable date if available
    for r in repos:
        if isinstance(r["lastModified"], int) and r["lastModified"] > 0:
            r["lastModified"] = datetime.utcfromtimestamp(r["lastModified"]).strftime('%Y-%m-%d')

    print(json.dumps(repos, indent=2))
