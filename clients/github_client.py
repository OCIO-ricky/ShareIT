# cdc-shareit-scan/clients/github_client.py
#
# Set environment variables:
# export GITHUB_ORG=cdcgov
# export GITHUB_TOKEN=your_github_pat

import requests
import os
import yaml
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Load configuration
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

GITHUB_API_URL = "https://api.github.com"
GITHUB_ORG = config["github"]["org"]
GITHUB_TOKEN = os.getenv(config["github"]["token_env_var"])

def fetch_github_repos():
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    repos = []
    page = 1
    per_page = 100

    while True:
        url = f"{GITHUB_API_URL}/orgs/{GITHUB_ORG}/repos?per_page={per_page}&page={page}"
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch GitHub repos: {response.status_code}")
            break

        data = response.json()
        if not data:
            break

        for repo in data:
            repos.append({
                "name": repo["name"],
                "description": repo.get("description", ""),
                "url": repo["html_url"],
                "usageType": "openSource" if not repo["private"] else "governmentWideReuse",
                "tags": ["github", repo["language"]] if repo["language"] else ["github"],
                "contact": f"{repo['owner']['login']}@cdc.gov",
                "created": repo["created_at"].split("T")[0],
                "lastModified": repo["updated_at"].split("T")[0]
            })

        page += 1

    return repos


if __name__ == "__main__":
    import json

    repos = fetch_github_repos()
    print(json.dumps(repos, indent=2))
