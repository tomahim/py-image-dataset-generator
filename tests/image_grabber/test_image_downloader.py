import unittest

import mock

from image_grabber.grab_settings import *
from image_grabber.image_downloader import ImageDownloader


class TestImageDownloader(unittest.TestCase):
    downloader = None

    def setUp(self):
        self.downloader = ImageDownloader()

    def test_init_defaults(self):
        """ ImageDownloader > it should load default values """
        self.assertIsNotNone(self.downloader)
        self.assertEqual(self.downloader.limit, DEFAULT_DOWNLOAD_LIMIT)
        self.assertEqual(self.downloader.full_image, True)
        self.assertEqual(self.downloader.destination, DEFAULT_DESTINATION_FOLDER)

    def test_download_with_no_keyword(self):
        """ Attempt to download images with no keyword should raise exception """
        try:
            self.downloader.download_images("")
        except Exception as e:
            pass
        else:
            self.fail("it should have raise an exception")

    @staticmethod
    def get_images_url(keyword):
        return []

    @mock.patch('image_grabber.bing_grabber.BingGrabber.get_images_url', new=get_images_url)
    def test_download_from_bing_only(self):
        self.downloader.sources = [GrabSourceType.BING.value]
        self.downloader.download_images("cats")


if __name__ == '__main__':
    unittest.main()
