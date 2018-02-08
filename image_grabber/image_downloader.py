import json
import os
import urllib2
from grab_source import GrabSourceType
from settings import *
from utils.string_utils import StringUtil

import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# TODO: split this into 3 classes: abstract grab class, google grab class and imageDownloader calling sub grab classes
class ImageDownloader:
    """Download images from a keyword and website sources"""

    keyword = None
    destination = 'images'
    limit = 50

    sources = [GrabSourceType.GOOGLE]
    file_prefix = None

    def __init__(self, destination='images', limit=50):
        """Constructor for ImageGrabber"""
        self.destination = destination
        self.limit = limit

    def download_images(self, keyword):
        self.keyword = keyword
        self.__set_default_file_prefix()
        self.__grab_from_google()

    def __grab_from_google(self):
        query = self.keyword.split()
        query = '+'.join(query)
        url = GOOGLE_URL % query

        print '> searching image on Google : ' + url

        options = webdriver.ChromeOptions()
        options.set_headless()

        browser = webdriver.Chrome(chrome_options=options)

        browser.get(url)
        time.sleep(2)

        elem = browser.find_element_by_tag_name("body")

        # scroll to fire the infinite scroll event and load more images
        no_of_pages_down = 20
        while no_of_pages_down:
            elem.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.2)
            no_of_pages_down -= 1

        images = browser.find_elements_by_class_name("rg_meta")

        images_urls = []
        for image in images:
            json_content = image.get_attribute('innerHTML')
            # links for Large original images, type of  image
            link, fileType = json.loads(json_content)["ou"], json.loads(json_content)["ity"]
            images_urls.append((link, fileType))

        browser.close()

        if len(images_urls) == 0:
            print "No image found on Google"
        else:
            print "\n %s images found on Google, limit to download set to %s \n" % (len(images_urls), self.limit)
            sub_folder_name = self.__create_destination_folder()
            self.__download_files(images_urls, sub_folder_name)

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
        """ save images in file system from list of urls """
        for i, (img, fileType) in enumerate(urls):
            if i == self.limit:
                break
            try:
                req = urllib2.Request(img, headers={'User-Agent': USER_AGENT_HEADER})
                raw_img = urllib2.urlopen(req).read()

                counter = len([i for i in os.listdir(folder_name) if self.file_prefix in i]) + 1
                extension = ".jpg" if len(fileType) == 0 else "." + fileType
                file_name = self.file_prefix + "_" + str(counter) + extension
                f = open(os.path.join(folder_name, file_name), 'wb')

                print "> grabbing %s \n >> saving file %s" % (img, file_name)

                f.write(raw_img)
                f.close()

            except Exception as e:
                print "could not load : " + img
                print e
