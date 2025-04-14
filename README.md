
# CDC SHARE IT Act Automation

This repository contains a Python-based solution for automating the discovery, metadata collection, and publication of CDC's custom-developed software repositories. The solution enables compliance with the SHARE IT Act by generating and deploying a `code.json` file in accordance with the [code.gov schema v2.0](https://code.gov/meta/schema/2.0.0/schema.json).

## 🚀 Features

- Scans repositories across:
  - GitHub
  - GitLab
  - Bitbucket (on-prem)
  - TFS / Azure DevOps
- Extracts standardized metadata
- Generates compliant `code.json`
- Deploys via shell script or Azure DevOps pipeline
- Includes governance guide and presentation deck for internal use

## 📁 Project Structure

```
cdc-shareit-scan/
├── clients/                  # Repository-specific scanners (GitHub, GitLab, etc.)
├── config.yaml               # Configuration for repo settings and tokens
├── .env                      # Environment variables for credentials
├── code_json_generator.py    # Main script to build code.json
├── requirements.txt          # Python dependencies
├── Makefile                  # Local automation commands
├── deploy/                   # Deployment scripts (e.g., publish to web)
└── docs/                     # Governance Word doc and presentation (optional)
```

## 🧰 Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 🔄 Run the Generator

```bash
python code_json_generator.py
```

## 🚢 Deploy to Web Server

```bash
sudo cp code.json /var/www/html/code.json
```

Or use the provided Makefile:

```bash
make deploy
```

## 🔐 Configuration

- `config.yaml`: Centralized repo + token config
- `.env`: Set API tokens and credentials

Example `.env`:
```
GITHUB_TOKEN=your_token
GITLAB_TOKEN=your_token
BITBUCKET_USERNAME=your_username
BITBUCKET_TOKEN=your_token
TFS_USERNAME=your_username
TFS_PAT=your_token
```

## 🧪 Test Clients Individually

```bash
python clients/github_client.py
python clients/gitlab_client.py
python clients/bitbucket_client.py
python clients/tfs_client.py
```

## 📤 CI/CD Automation

Included:
- `azure-pipelines.yml`: Publishes `code.json` to public web via Azure DevOps

## 📚 Documentation

- `CDC_Code_Metadata_Governance_Guide.docx`: Internal guidance for code owners
- `CDC_SHARE_IT_Act_Overview_Presentation.pptx`: Presentation deck for briefings

## ✅ Compliance Goal

Ensure CDC satisfies the SHARE IT Act requirement to publicly list and share custom-developed code metadata by publishing:

```
https://www.cdc.gov/code.json
```

## 🛠 Maintainers

- OCIO EA Team (Enterprise Architecture)
- CDC WebOps (for public site publishing)

