# cdc-shareit-scan/clients/github_client.py
#
# $> python github_client.py --output myproject_code.json
#
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

GITHUB_API_URL = "https://api.github.com"
GITHUB_ORG = config["github"]["org"]
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

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

    repos = fetch_github_repos()
    generate_code_json(repos, args.output)
    print(f"Generated {args.output} successfully.")
