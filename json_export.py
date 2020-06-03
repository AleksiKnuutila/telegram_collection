"""json_export.

Usage:
json_export [--api-id ID] [--api-hash HASH] 
    [--tracked-sites-csv-filename FILENAME]
    [--output-data-dir DIR] 
    [--tracked-telegram-channels CHANNEL1,CHANNEL2]
json_export -h | --help
json_export --version

Options can be read from config.yaml and secret.yaml.

Options:

 -h --help                           Show this screen.
 --version                           Show the version.
 --api-id api_id                     Set API ID (can be read from config)
 --api-hash api_hash                 Set API hash
 --tracked-sites-csv-filename fn     Filename for CSV with tracked sites
 --output-data-dir dir               Directory where CSV files are written
 --tracked-telegram-channels c1,c2   Telegram channels to examine, comma-delimited
"""

import os
from datetime import datetime, timedelta
from dataclasses import asdict
import json

import pandas as pd
import pytz

from telegram_collection.common import config, logger
from telegram_collection.telegram import (
    SyncTelegramClient,
    is_forwarded,
    match_links,
)
from telegram_collection.models import TelegramTrackedPost


def write_messages_to_file(messages, filename):
    """Write JSON file with collected messages

    Arguments:
        messages {list of Telethon message objects} --
        filename {str} --
    """

    def date_format(message):
        if type(message) is datetime:
            return message.strftime("%Y-%m-%d %H:%M:%S")

    output = [x.to_dict() for x in messages]

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=4, default=date_format)


def main():
    """Main entry point of telegram_collection"""

    client = SyncTelegramClient()

    batch_start = to_date = datetime.now().replace(tzinfo=pytz.UTC)
    from_date = to_date - timedelta(days=7)

    all_messages = []

    for channel_name in config["tracked-telegram-channels"]:

        try:
            channel_info = client.get_channel_info(channel_name)
        except ValueError:
            logger.warning("Tracked channel %s doesn't exists" % channel_name)
            continue

        recent_messages = client.fetch_messages_since(channel_name, from_date)

        logger.debug(
            "From channel %s: %s messages" % (channel_name, len(recent_messages))
        )
        all_messages = all_messages + recent_messages

    filename = "telegram-{} to {}.json".format(
        from_date.strftime("%Y-%m-%d"), to_date.strftime("%Y-%m-%d")
    )
    filename = os.path.join(config["output-data-dir"], filename)
    logger.debug("Writing JSON with %s records to %s" % (len(all_messages), filename))
    write_messages_to_file(all_messages, filename)


if __name__ == "__main__":
    main()
