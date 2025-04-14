# CDC SHARE IT Act Automation - Makefile
#
# SETUP:
# $> make init
# $> make install
#
# RUN:
# $> make generate
#
# Deploy code.json to Web Server:
# $> sudo make deploy
#

VENV_DIR := venv
PYTHON := $(VENV_DIR)/bin/python
PIP := $(VENV_DIR)/bin/pip
CODE_JSON := code.json
DEPLOY_DIR := /var/www/html

.PHONY: help init install generate deploy clean test

help:
	@echo "CDC SHARE IT Automation - Available Commands:"
	@echo "  make init       - Create Python virtual environment"
	@echo "  make install    - Install dependencies"
	@echo "  make generate   - Generate code.json file"
	@echo "  make deploy     - Deploy code.json to web server"
	@echo "  make test       - Test individual clients"
	@echo "  make clean      - Remove virtual environment and artifacts"

init:
	python3 -m venv $(VENV_DIR)

install:
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

generate:
	$(PYTHON) code_json_generator.py

deploy: generate
	cp $(CODE_JSON) $(DEPLOY_DIR)/$(CODE_JSON)

clean:
	rm -rf $(VENV_DIR)
	rm -f $(CODE_JSON)

test:
	@echo "Testing GitHub Client..."
	$(PYTHON) clients/github_client.py
	@echo "Testing GitLab Client..."
	$(PYTHON) clients/gitlab_client.py
	@echo "Testing Bitbucket Client..."
	$(PYTHON) clients/bitbucket_client.py
	@echo "Testing TFS Client..."
	$(PYTHON) clients/tfs_client.py
