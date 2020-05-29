"""omms_telegram_collection.

Usage:
omms_telegram_collection -h | --help
omms_telegram_collection --version

Options:

 -h --help    Show this screen.
 --version    Show the version.
"""

from omms_telegram_collection.from_docopt import from_docopt
from omms_telegram_collection.common import config
from omms_telegram_collection.telegram import (
    SyncTelegramClient,
    links_with_metadata,
    is_forwarded,
)
from omms_telegram_collection.models import TelegramTrackedPost

from datetime import datetime
import pandas as pd
import sys


def matching_links(msg, tracked_sites):
    """ Find links from Telegram messages that match tracked news sources

    Arguments:
        msg {[type]} -- [description]
        tracked_sites {[type]} -- [description]
    """
    links = links_with_metadata(msg)
    return (tracked_sites[0], "google.com")


def tracked_channel_names():
    """ Get names of all tracked Telegram channels """
    return ["TommyRobinsonNews"]


def tracked_news_sources(filename):
    # From dataframe to list of dicts
    return pd.read_csv(filename, encoding="ISO-8859-1").to_dict("records")


def write_matches_to_file(messages, filename=None):
    """[summary]

    Arguments:
        messages {[type]} -- [description]

    Keyword Arguments:
        filename {[type]} -- [description] (default: {None})
    """
    pass


def main(inputargs=None):
    """Main entry point of omms_telegram_collection"""
    # if inputargs is None:
    #    inputargs = sys.argv[1:] if len(sys.argv) > 1 else ""
    #    args = from_docopt(argv=inputargs, docstring=__doc__)

    client = SyncTelegramClient()

    tracked_telegram_channels = tracked_channel_names()
    tracked_sites = tracked_news_sources(config["tracked_sites_csv_filename"])
    batch_start = datetime.now()

    matching_messages = []

    for channel in tracked_telegram_channels:
        recent_messages = client.fetch_messages(channel, 300, 0)
        for msg in recent_messages:
            # Skip forwarded messages to avoid doublecounting views
            if is_forwarded(msg):
                continue
            (matching_site, matching_links) = matching_links(msg, tracked_sites)
            if matching_site:
                matching_message = TelegramTrackedPost.from_telethon(
                    msg,
                    channel_name=channel,
                    matching_url=matching_url,
                    news_source=matching_site,
                    batch_time=batch_start,
                )
                matching_messages.append(matching_message)

    write_matches_to_file(matching_messages)


if __name__ == "__main__":
    main()
