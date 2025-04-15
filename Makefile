# CDC SHARE IT Act Automation - Makefile
#
# SETUP: Run once to install environment
# $> make setup   
# $> make install
#
# RUN: ( Merge code.json files )
# $> make merge 
#
# PUBLISH: (Output file is now live at /var/www/html/code.json)
# $> make publish   
#
# Full merge and publish:
# $> make all        
#

# Central Automation Makefile for CDC SHARE IT Act

INPUT_DIR := submissions  # Change to your shared folder path
OUTPUT := /var/www/html/code.json

VENV := venv
PYTHON := $(VENV)/bin/python

.PHONY: all setup merge publish clean

all: merge publish

setup:
	python3 -m venv $(VENV)
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt

merge:
	$(PYTHON) code_json_generator.py --input_dir $(INPUT_DIR) --output $(OUTPUT)

publish:
	@echo "✅ code.json published to $(OUTPUT)"

clean:
	rm -rf $(VENV)
	rm -f code.json
