# cdc-shareit-scan/clients/gitlab_client.py

import requests
import os
import yaml
import json

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

GITLAB_BASE_URL = config["gitlab"]["base_url"]
GITLAB_GROUP = config["gitlab"]["group"]
GITLAB_TOKEN = os.getenv(config["gitlab"]["token_env_var"])

def fetch_gitlab_repos():
    headers = {
        "Private-Token": GITLAB_TOKEN
    }
    repos = []
    page = 1

    while True:
        url = f"{GITLAB_BASE_URL}/groups/{GITLAB_GROUP}/projects?per_page=100&page={page}&include_subgroups=true"
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch GitLab repos: {response.status_code}")
            break

        data = response.json()
        if not data:
            break

        for repo in data:
            repos.append({
                "name": repo["name"],
                "description": repo.get("description", ""),
                "url": repo["web_url"],
                "usageType": "governmentWideReuse" if repo["visibility"] != "public" else "openSource",
                "tags": ["gitlab", repo["namespace"]["name"]],
                "contact": f"{repo['namespace']['name']}@cdc.gov",
                "created": repo["created_at"].split("T")[0],
                "lastModified": repo["last_activity_at"].split("T")[0]
            })

        page += 1

    return repos

if __name__ == "__main__":
    repos = fetch_gitlab_repos()
    print(json.dumps(repos, indent=2))