#!/bin/bash
# USAGE:
# $> chmod +x generate_and_publish.sh
# $> ./generate_and_publish.sh
#
# Optional use Cron:
# $> crontab -e
# > 0 2 * * * /path/to/deploy/generate_and_publish.sh >> /var/log/cdc_shareit.log 2>&1
#
# Central Automation Script for CDC SHARE IT Act
INPUT_DIR="./submissions"          # Folder with individual code.json files
OUTPUT_PATH="/var/www/html/code.json"

echo "▶ Activating virtual environment..."
source ./venv/bin/activate

echo "▶ Merging code.json files from $INPUT_DIR..."
python code_json_generator.py --input_dir "$INPUT_DIR" --output "$OUTPUT_PATH"

echo "✅ code.json successfully published to $OUTPUT_PATH"
