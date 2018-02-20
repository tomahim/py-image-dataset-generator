import unicodedata

import os


class StringUtil:
    def __init__(self):
        """Constructor for StringUtil"""

    @staticmethod
    def underscore_and_lowercase(words: str) -> str:
        return words.lower().replace(" ", "_")

    @staticmethod
    def is_http_url(src) -> bool:
        result = unicodedata.normalize('NFKD', src).encode('ascii', 'ignore')
        return result[:4].decode() == "http"


class FileUtil:
    image_extensions = ['.bmp', '.gif', '.jpeg', '.jpg', '.png', '.raw', '.tiff']

    def __init__(self):
        """Constructor for FileUtil"""

    @staticmethod
    def nb_file_in_folder(folder_path: str) -> int:
        num_files = len([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))
                         and FileUtil.is_image(os.path.join(folder_path, f))])
        return num_files

    @staticmethod
    def get_file_extension(path: str) -> str:
        return os.path.splitext(path)[1]

    @staticmethod
    def is_image(path: str) -> bool:
        return FileUtil.get_file_extension(path).lower() in FileUtil.image_extensions
