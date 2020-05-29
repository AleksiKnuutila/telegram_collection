from datetime import datetime
from pydantic.dataclasses import dataclass

# fieldnames = ['platform', 'capture_type', 'group_name',
#               'batch_capture_time', 'batch_capture_time_readable', 'precise_capture_time', 'precise_capture_time_readable', 'created_time',
#               'searched_site', 'searched_link', 'api_qtype', 'cat', 'page',
#               'found_link', 'postUrl', 'content_type', 'caption', 'description', 'message',
#               'sharing_account_handle', 'sharing_account_id', 'sharing_account_follower_count', 'sharing_account_statuses_count',
#               'statistics_favourite_count', 'statistics_retweet_count', 'statistics_like_count', 'statistics_love_count',
#               'statistics_comment_count', 'statistics_haha_count', 'statistics_sad_count', 'statistics_share_count',
#               'statistics_thankful_count', 'statistics_wow_count', 'statistics_angry_count',
#              'statistics_reddit_awards', 'statistics_reddit_score', 'statistics_reddit_crossposts']


@dataclass
class TrackedPost:
    """ Parent class for data collected by OMMS scrapers for various platforms """

    platform: str


#    capture_type: str
#    batch_capture_time: str
#    batch_capture_time_readable: str
#    precise_capture_time: str
#    precise_capture_time_readable: str
#    created_time: str
#    searched_site: str
#    searched_link: str = ''
#    api_qtype: str = ''
#    cat: str
#    page: str
#    found_link: str
#    postUrl: str
#    content_type: str
#    caption: str
#    description: str
#    message: str
#    sharing_account_handle: str
#    sharing_account_id: str
#    sharing_account_follower_count: str
#    sharing_account_statuses_count: str
#    statistics_favourite_count: str
#    statistics_retweet_count: str
#    statistics_like_count: str
#    statistics_love_count: str
#    statistics_comment_count: str
#    statistics_haha_count: str
#    statistics_sad_count: str
#    statistics_share_count: str
#    statistics_thankful_count: str
#    statistics_wow_count: str
#    statistics_angry_count: str
#    statistics_dislike_count: str
#    statistics_view_count: str


@dataclass
class TelegramTrackedPost(TrackedPost):
    telegram_message: str
    # page: str = ''

    #    es_record = {
    #        "channel_id": message.to_id.channel_id,
    #        "message_id": message.id,
    #        "message": message.message,
    #        "date": int(message.date.timestamp()),
    #        "via_bot_id": message.via_bot_id,
    #        "channel_name": channel_name,
    #        "grouped_id": message.grouped_id,
    #        "post_author": message.post_author,
    #        "post": message.post,
    #        "silent": message.silent,
    #        "retrieved_utc": retrieved_utc,
    #        "updated_utc": retrieved_utc,
    #    }

    @classmethod
    def from_telethon(
        cls, telethon_msg, *, channel_name, matching_url, news_source, batch_time=None
    ):
        """ Map Telethon's message object to OMMS internal datastructure and construct new object """
        current_time = datetime.now()
        if not batch_time:
            batch_time = current_time

        #    searched_site: str
        #    searched_link: str
        #    api_qtype: str
        #    cat: str
        #    page: str
        #    found_link: str
        #    postUrl: str
        #    content_type: str
        #    caption: str
        #    description: str
        #    message: str
        #    sharing_account_handle: str

        attributes = {
            "platform": "Telegram",
            "batch_capture_time": str(current_time.timestamp()),
            "batch_capture_time_readable": str(current_time),
            "precise_capture_time": str(batch_time.timestamp()),
            "precise_capture_time_readable": str(batch_time),
            "created_time": str(telethon_msg.date.timestamp()),
            "searched_site": searched_site,
            "cat": news_source.cat,
            "page": channel_name,
            "message": telethon_msg.message,
        }
        return cls(**attributes)
