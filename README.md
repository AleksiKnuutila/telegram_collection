# Introduction

telegram_collection collects Telegram data from a defined set of channels

# Use

```
Usage:
telegram_collection [--api-id ID] [--api-hash HASH]
  [--tracked-sites-csv-filename FILENAME]
  [--output-data-dir DIR]
  [--tracked-telegram-channels CHANNEL1,CHANNEL2]
telegram_collection -h | --help
telegram_collection --version

Options can be read from config.yaml and secret.yaml.

Options:
  
  -h --help                           Show this screen.
  --version                           Show the version.
  --api-id api_id                     Set API ID (can be read from config)
  --api-hash api_hash                 Set API hash
  --tracked-sites-csv-filename fn     Filename for CSV with tracked sites
  --output-data-dir dir               Directory where CSV files are written
  --tracked-telegram-channels c1,c2   Telegram channels to examine, comma-delimited

Example:

python -m telegram_collection --tracked-telegram-channels bbcworldnews,infowars
```

Code for matching scraper data structure is in telegram_collection/__main__.py. json_exports.py writes data in JSON.

# Setting up

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

# Run tests

```
python -m pytest
```