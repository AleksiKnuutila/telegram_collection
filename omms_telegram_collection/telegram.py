"""Helper methods for data collection from telegram"""

import json

from telethon.errors import ChatAdminRequiredError
from telethon.sync import TelegramClient
from telethon.tl import functions

from omms_telegram_collection.common import logger, config

from dataclasses import make_dataclass
import itertools as it
import pytz
import re


def links_with_metadata(message):
    LC = make_dataclass("LinkMetaData", ["url", "caption", "description"])
    links = []

    # Links in Telegram messages can be embedded (then found in message.media), or part of the
    # text body of the message (when we can find them through message.entities)
    if hasattr(message.media, "webpage") and hasattr(message.media.webpage, "url"):
        webpage = message.media.webpage
        links.append(LC(webpage.url, webpage.title or "", webpage.description or ""))

    if not message.entities:
        return links
    for entity in message.entities:
        data = entity.to_dict()
        if data["_"] == "MessageEntityTextUrl":
            if not entity.url in [x.url for x in links]:
                # Pick out the link text based on offset and length in Telethon object
                link_text = message.message[
                    entity.offset : entity.offset + entity.length
                ]
                links.append(LC(entity.url, link_text, ""))

    return links


def match_links(msg, tracked_sites):
    """ Find links from Telegram messages that match tracked news sources

    Arguments:
        msg {[type]} -- [description]
        tracked_sites {[type]} -- [description]
    """
    links = links_with_metadata(msg)

    for link, site in it.product(links, tracked_sites):
        if re.search(
            "(^|[\.\/]){}(/|$)".format(site["short.link"]), link.url, re.IGNORECASE
        ):
            return make_dataclass("MatchedLink", ["link", "matched_site"])(link, site)

    return None


def is_forwarded(message):
    if hasattr(message, "fwd_from") and message.fwd_from:
        return True
    return False


class SyncTelegramClient:
    def __init__(self):
        self._client = TelegramClient("session", config["api_id"], config["api_hash"])

    def fetch_messages_since(self, channel, from_date, limit=1000):
        logger.debug(
            "Fetching messages since %s from channel %s" % (str(from_date), channel)
        )
        if not self._client.is_connected():
            self._client.connect()
        itermsgs = self._client.iter_messages(channel, limit)
        messages = it.takewhile(lambda x: x.date > from_date, itermsgs)
        return list(messages)

    def fetch_messages(
        self, channel, size=100, max_id=None, min_id=None, search=None, filter=None
    ):
        """Method to fetch messages from a specific channel / group"""

        logger.debug("Fetching up to %d messages from channel %s" % (size, channel))
        params = [channel, size]
        kwargs = {}

        # The telethon module has issues if a keyword passed is None, so we will add the keyword
        # only if it is not None
        for key in ["max_id", "min_id", "search", "filter"]:
            if locals()[key] is not None:
                kwargs[key] = locals()[key]

        with self._client as client:
            data = client.get_messages(*params, **kwargs)

        return data

    def get_channel_info(self, channel):
        with self._client as client:
            return client(
                functions.channels.GetFullChannelRequest(channel=channel)
            ).to_dict()
