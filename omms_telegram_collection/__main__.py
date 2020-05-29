"""omms_telegram_collection.

Usage:
omms_telegram_collection -h | --help
omms_telegram_collection --version

Options:

 -h --help    Show this screen.
 --version    Show the version.
"""

import sys
from omms_telegram_collection.from_docopt import from_docopt

from omms_telegram_collection.telegram import SyncTelegramClient
from omms_telegram_collection.models import TelegramTrackedPost


def matching_links(msg, tracked_sites):
    """ Find links from Telegram messages that match tracked news sources

    Arguments:
        msg {[type]} -- [description]
        tracked_sites {[type]} -- [description]
    """
    return ""


def tracked_channel_names():
    """ Get names of all tracked Telegram channels """
    return ["pjwnews"]


def tracked_news_sources(filename=""):
    return [{"domain": "infowars.com", "cat": "junk news"}]


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

    test = SyncTelegramClient()
    channel = test.get_channel_info("pjnews")
    msgs = test.fetch_messages("pjwnews", 100, 0)
    print("moi")

    tracked_telegram_channels = tracked_channel_names()
    tracked_sites = tracked_news_sources()

    matching_messages = []

    for channel in tracked_telegram_channels:
        recent_messages = test.fetch_messages(channel, 300, 0)
        for msg in recent_messages:
            (matching_site, matching_url) = matching_links(msg, tracked_sites)
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
