#!/bin/bash
#
# $> cd deploy
# $> chmod +x generate_and_publish.sh
# $> ./generate_and_publish.sh
#
# Optional use Cron:
# $> crontab -e
# > 0 2 * * * /path/to/deploy/generate_and_publish.sh >> /var/log/cdc_shareit.log 2>&1

echo "Activating virtual environment..."
source ../venv/bin/activate

echo "Generating code.json..."
python ../code_json_generator.py

echo "Publishing code.json to public web directory..."
cp ../code.json /var/www/html/code.json

echo "Deployment completed successfully."
