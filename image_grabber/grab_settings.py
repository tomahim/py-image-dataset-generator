from enum import Enum

DEBUG_MODE = False

USER_AGENT_HEADER = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
}


class GrabSourceType(Enum):
    GOOGLE = 'Google'
    BING = 'Bing'


ALL_SOURCE = 'all'

DEFAULT_GRAB_SOURCE_TYPE = GrabSourceType.GOOGLE.value
DEFAULT_DOWNLOAD_LIMIT = 50
DEFAULT_DESTINATION_FOLDER = "images"
