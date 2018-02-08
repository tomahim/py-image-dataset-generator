class StringUtil:
    def __init__(self):
        """Constructor for StringUtils"""

    @staticmethod
    def underscore_and_lowercase(words):
        return words.lower().replace(" ", "_")
