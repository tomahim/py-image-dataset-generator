import unicodedata

class StringUtil:
    def __init__(self):
        """Constructor for StringUtils"""

    @staticmethod
    def underscore_and_lowercase(words):
        return words.lower().replace(" ", "_")

    @staticmethod
    def is_http_url(src):
        result = unicodedata.normalize('NFKD', src).encode('ascii', 'ignore')
        return result[:4].decode() == "http"
