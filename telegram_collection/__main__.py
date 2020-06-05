"""telegram_collection.

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
"""

import os
import csv
from datetime import datetime, timedelta
from dataclasses import asdict

import pandas as pd
import pytz

from telegram_collection.common import config, logger
from telegram_collection.telegram import (
    SyncTelegramClient,
    is_forwarded,
    match_links,
)
from telegram_collection.models import TelegramTrackedPost


def tracked_news_sources(filename):
    """Return list of news sources tracked by project

    Arguments:
        filename {str} -- CSV file with list

    Returns:
        list of dicts -- sources with metadata
    """
    # From dataframe to list of dicts
    return pd.read_csv(filename, encoding="ISO-8859-1").to_dict("records")


def write_messages_to_file(messages, filename):
    """Write CSV file with collected messages

    Arguments:
        messages {list of Telethon message objects} --
        filename {str} --
    """
    output = [list(asdict(messages[0]).keys())]
    output += [list(asdict(x).values()) for x in messages]

    with open(filename, "w") as f:
        writer = csv.writer(f)
        writer.writerows(output)


def main():
    """Main entry point of telegram_collection"""

    client = SyncTelegramClient()

    tracked_sites = tracked_news_sources(config["tracked-sites-csv-filename"])
    batch_start = to_date = datetime.now().replace(tzinfo=pytz.UTC)
    from_date = to_date - timedelta(days=7)

    all_matched_messages = []

    for channel_name in config["tracked-telegram-channels"]:

        try:
            channel_info = client.get_channel_info(channel_name)
        except ValueError:
            logger.warning("Tracked channel %s doesn't exists" % channel_name)
            continue

        recent_messages = client.fetch_messages_since(channel_name, from_date)
        # Skip forwarded messages to avoid doublecounting views (cf. how Telegram views are calculated)
        original_messages = [msg for msg in recent_messages if not is_forwarded(msg)]

        matching_messages = zip(
            original_messages,
            [match_links(msg, tracked_sites) for msg in original_messages],
        )
        matching_messages = [
            TelegramTrackedPost.from_telethon(
                msg[0],
                matched_link=msg[1].link,
                news_source=msg[1].matched_site,
                channel=channel_info,
                batch_time=batch_start,
            )
            for msg in matching_messages
            # match_links returns None if there is no match, and this is saved in second item of tuple
            if msg[1]
        ]

        logger.debug(
            "From channels %s: total %s messages, %s matching tracked sites"
            % (channel_name, len(recent_messages), len(matching_messages))
        )
        all_matched_messages = all_matched_messages + matching_messages

    filename = "telegram_matches-{} to {}.csv".format(
        from_date.strftime("%Y-%m-%d"), to_date.strftime("%Y-%m-%d")
    )
    filename = os.path.join(config["output-data-dir"], filename)
    logger.debug(
        "Writing CSV with %s records to %s" % (len(all_matched_messages), filename)
    )
    write_messages_to_file(all_matched_messages, filename)


if __name__ == "__main__":
    main()
