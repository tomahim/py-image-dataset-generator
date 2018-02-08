import os
import urllib2

from google_grabber import GoogleGrabber
from grab_source import GrabSourceType
from settings import *
from utils.string_utils import StringUtil


class ImageDownloader:
    """Download images from a keyword and website sources"""

    keyword = None
    destination = 'images'
    limit = 50
    file_prefix = None

    sources = [GrabSourceType.GOOGLE]

    def __init__(self, destination='images', limit=50):
        """Constructor for ImageGrabber"""
        self.destination = destination
        self.limit = limit

    def download_images(self, keyword):
        self.keyword = keyword
        self.__set_default_file_prefix()
        urls = []
        if GrabSourceType.GOOGLE in self.sources:
            google_grabber = GoogleGrabber()
            urls.extend(google_grabber.get_images_url(self.keyword))

        if len(urls) == 0:
            print "No image found on sources " + self.sources
        else:
            sub_folder_name = self.__create_destination_folder()
            print "\n %s images found on %s, limit to download set to %s \n" % (len(urls), self.sources, self.limit)
            self.__download_files(urls[:self.limit], sub_folder_name)

    def __set_default_file_prefix(self):
        """if no specified file prefix, build one from keyword"""
        if self.file_prefix is None:
            self.file_prefix = StringUtil.underscore_and_lowercase(self.keyword)

    def __create_destination_folder(self):
        """ set default destination to 'images', create and return sub_folder based on keyword name """
        if self.destination is None:
            self.destination = 'images'

        if not os.path.exists(self.destination):
            os.mkdir(self.destination)
        sub_folder = os.path.join(self.destination, StringUtil.underscore_and_lowercase(self.keyword))

        if not os.path.exists(sub_folder):
            os.mkdir(sub_folder)
        return sub_folder

    def __download_files(self, urls, folder_name):
        """urls param is a list of url / extension tuples"""
        for i, (img, file_type) in enumerate(urls):
            if i == self.limit:
                break
            try:
                req = urllib2.Request(img, headers={'User-Agent': USER_AGENT_HEADER})
                raw_img = urllib2.urlopen(req).read()

                counter = len([i for i in os.listdir(folder_name) if self.file_prefix in i]) + 1
                extension = ".jpg" if len(file_type) == 0 else "." + file_type
                file_name = self.file_prefix + "_" + str(counter) + extension
                f = open(os.path.join(folder_name, file_name), 'wb')

                print "> grabbing %s \n >> saving file %s" % (img, file_name)

                f.write(raw_img)
                f.close()

            except Exception as e:
                print "could not load : " + img
                print e
