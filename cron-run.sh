#!/bin/bash

tracked_sites_fn=$1

cd ~/dcms/scripts/telegram_collection

source venv/bin/activate

export PYTHONPATH=~/dcms/scripts
export LOGURU_LEVEL=DEBUG

python -m telegram_collection --tracked-sites-csv-filename "$tracked_sites_fn"
