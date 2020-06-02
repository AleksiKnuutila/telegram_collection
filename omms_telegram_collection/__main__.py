"""omms_telegram_collection.

Usage:
omms_telegram_collection -h | --help
omms_telegram_collection --version

Options:

 -h --help    Show this screen.
 --version    Show the version.
"""

from omms_telegram_collection.from_docopt import from_docopt
from omms_telegram_collection.common import config, logger
from omms_telegram_collection.telegram import (
    SyncTelegramClient,
    links_with_metadata,
    is_forwarded,
    match_links,
)
from omms_telegram_collection.models import TelegramTrackedPost

from dataclasses import make_dataclass, asdict
import itertools as it

from datetime import datetime, timedelta
import pandas as pd, csv
import re
import pytz
import sys, os


def tracked_news_sources(filename):
    # From dataframe to list of dicts
    return pd.read_csv(filename, encoding="ISO-8859-1").to_dict("records")


def write_messages_to_file(messages, filename):
    """[summary]

    Arguments:
        messages {[type]} -- [description]

    Keyword Arguments:
        filename {[type]} -- [description] (default: {None})
    """

    output = [list(asdict(messages[0]).keys())]
    output += [list(asdict(x).values()) for x in messages]

    with open(filename, "w") as f:
        writer = csv.writer(f)
        writer.writerows(output)


def main(inputargs=None):
    """Main entry point of omms_telegram_collection"""
    # if inputargs is None:
    #    inputargs = sys.argv[1:] if len(sys.argv) > 1 else ""
    #    args = from_docopt(argv=inputargs, docstring=__doc__)

    client = SyncTelegramClient()

    tracked_sites = tracked_news_sources(config["tracked_sites_csv_filename"])
    batch_start = to_date = datetime.now().replace(tzinfo=pytz.UTC)
    from_date = to_date - timedelta(days=7)

    all_matched_messages = []

    for channel_name in config["tracked_telegram_channels"]:

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
    filename = os.path.join(config["output_data_dir"], filename)
    logger.debug(
        "Writing CSV with %s records to %s" % (len(all_matched_messages), filename)
    )
    write_messages_to_file(all_matched_messages, filename)


if __name__ == "__main__":
    main()
