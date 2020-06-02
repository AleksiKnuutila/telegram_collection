import pytest

# import omms_telegram_collection
from omms_telegram_collection.telegram import (
    SyncTelegramClient,
    links_with_metadata,
    is_forwarded,
    links_with_metadata,
    match_links,
)

from omms_telegram_collection.__main__ import tracked_news_sources

from omms_telegram_collection.common import config
from urllib.request import urlopen
from telethon.tl.types import InputMessagesFilterUrl
from datetime import datetime, timedelta
import pytz


@pytest.fixture
def telethon_messages_with_link():
    client = SyncTelegramClient()
    return client.fetch_messages(
        "TommyRobinsonNews", 1, search="tr.news", filter=InputMessagesFilterUrl
    )[0]


def test_match_links(telethon_messages_with_link):
    tracked_sites = tracked_news_sources(config["tracked_sites_csv_filename"])
    match = match_links(telethon_messages_with_link, tracked_sites)
    assert "tr.news" in match.link.url
    assert match.link.description or match.link.caption
    assert match.matched_site["short.link"] == "tr.news"


def test_links_with_metadata(telethon_messages_with_link):
    link = links_with_metadata(telethon_messages_with_link)[0]
    assert "tr.news" in link.url
    assert link.description or link.caption


def test_fetch_messages_since():
    to_date = datetime.now().replace(tzinfo=pytz.UTC)
    from_date1 = to_date - timedelta(days=1)
    client = SyncTelegramClient()
    msgs1 = client.fetch_messages_since("TommyRobinsonNews", from_date1)
    from_date2 = to_date - timedelta(days=10)
    msgs2 = client.fetch_messages_since("TommyRobinsonNews", from_date2)
    assert len(msgs1) < len(msgs2)
    assert not any([x.date < from_date1 for x in msgs1])
    assert not any([x.date < from_date2 for x in msgs2])


def test_integration_in_main_function():
    pass
