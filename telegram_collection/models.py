from datetime import datetime
from pydantic.dataclasses import dataclass


@dataclass
class TrackedPost:
    """ Parent class for data collected by scrapers for various platforms """

    batch_capture_time: datetime
    batch_capture_time_readable: str
    precise_capture_time: datetime
    precise_capture_time_readable: str
    cat: str
    found_link: str
    content_type: str
    description: str
    caption: str
    message: str
    sharing_account_handle: str
    sharing_account_id: int
    sharing_account_follower_count: int or None
    statistics_view_count: int or None
    created_time: str
    searched_site: str
    searched_link: str
    message_id: int

    # Variables that may be overwritten by subclasses (must come last in dataclasses)
    platform: str
    capture_type: str
    group_name: str
    sharing_account_statuses_count: int or None
    statistics_favourite_count: int or None
    statistics_retweet_count: int or None
    statistics_like_count: int or None
    statistics_love_count: int or None
    statistics_comment_count: int or None
    statistics_haha_count: int or None
    statistics_sad_count: int or None
    statistics_share_count: int or None
    statistics_thankful_count: int or None
    statistics_wow_count: int or None
    statistics_angry_count: int or None
    statistics_dislike_count: int or None
    postUrl: str
    page: str
    api_qtype: str


@dataclass
class TelegramTrackedPost(TrackedPost):
    platform: str = "Telegram"
    capture_type: str = "telegram_collection"
    group_name: str = ""
    page: str = ""
    api_qtype: str = "telethon"
    # No URLs for individual messages in Telegram
    postUrl: str = ""
    # These stats are undefined for Telegram
    sharing_account_statuses_count: int = None
    statistics_favourite_count: int = None
    statistics_retweet_count: int = None
    statistics_like_count: int = None
    statistics_love_count: int = None
    statistics_comment_count: int = None
    statistics_haha_count: int = None
    statistics_sad_count: int = None
    statistics_share_count: int = None
    statistics_thankful_count: int = None
    statistics_wow_count: int = None
    statistics_angry_count: int = None
    statistics_dislike_count: int = None

    @classmethod
    def from_telethon(
        cls, telethon_msg, *, channel, matched_link, news_source, batch_time=None
    ):
        """ Map Telethon's message object to the scraper's internal datastructure and construct new object """
        current_time = datetime.now()
        if not batch_time:
            batch_time = current_time

        return cls(
            batch_capture_time=str(current_time.timestamp()),
            batch_capture_time_readable=str(current_time),
            precise_capture_time=str(batch_time.timestamp()),
            precise_capture_time_readable=str(batch_time),
            # created_time=str(telethon_msg.date.timestamp()),
            created_time=str(telethon_msg.date),
            cat=news_source["cat"],
            message=telethon_msg.message,
            searched_site=news_source["short.link"],
            searched_link=news_source["short.link"],
            found_link=matched_link.url,
            content_type="link",
            caption=matched_link.caption,
            description=matched_link.description,
            page=channel["chats"][0]["username"],
            sharing_account_handle=channel["chats"][0]["username"],
            sharing_account_id=channel["full_chat"]["id"],
            sharing_account_follower_count=channel["full_chat"]["participants_count"],
            statistics_view_count=telethon_msg.views,
            message_id=telethon_msg.id,
        )
