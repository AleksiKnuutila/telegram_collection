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
    capture_type: str
    batch_capture_time: str
    batch_capture_time_readable: str
    precise_capture_time: str
    precise_capture_time_readable: str
    created_time: str
    searched_site: str
    searched_link: str
    api_qtype: str
    cat: str
    page: str
    found_link: str
    postUrl: str
    content_type: str
    caption: str
    description: str
    message: str
    sharing_account_handle: str
    sharing_account_id: str
    sharing_account_follower_count: str
    sharing_account_statuses_count: str
    statistics_favourite_count: str
    statistics_retweet_count: str
    statistics_like_count: str
    statistics_love_count: str
    statistics_comment_count: str
    statistics_haha_count: str
    statistics_sad_count: str
    statistics_share_count: str
    statistics_thankful_count: str
    statistics_wow_count: str
    statistics_angry_count: str
    statistics_dislike_count: str
    statistics_view_count: str


@dataclass
class TelegramTrackedPost(TrackedPost):
    telegram_var: str
