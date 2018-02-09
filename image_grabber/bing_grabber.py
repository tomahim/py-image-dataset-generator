import json
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from grab_settings import *

from abstract_grabber import AbstractGrabber
from grabbed_image import GrabbedImage
import unicodedata


class BingGrabber(AbstractGrabber):
    """Grab images from google search"""

    full_image = True

    BING_URL = "https://www.bing.com/images/search?q=%s"

    def __init__(self):
        pass

    def get_images_url(self, keyword):
        query = keyword.split()
        query = '+'.join(query)
        url = self.BING_URL % query

        print '> searching image on Bing : ' + url

        options = webdriver.ChromeOptions()

        browser = webdriver.Chrome(chrome_options=options)

        browser.get(url)
        print browser.get_window_size()
        browser.maximize_window()
        time.sleep(2)

        elem = browser.find_element_by_tag_name("body")

        # scroll to fire the infinite scroll event and load more images
        no_of_pages_down = 20
        while no_of_pages_down:
            elem.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.2)
            no_of_pages_down -= 1

        images_objects = []
        if self.full_image:
            images = browser.find_elements_by_class_name("iusc")
            for image in images:
                image_obj = GrabbedImage()
                image_obj.source = GrabSourceType.BING.value
                json_content = image.get_attribute('m')
                # links for Large original image
                image_obj.url = json.loads(json_content)["murl"]
                if image_obj.url.split('.')[-1] is not None:
                    image_obj.extension = image_obj.url.split('.')[-1]
                images_objects.append(image_obj)
        else:
            images = browser.find_elements_by_class_name("mimg")
            for image in images:
                image_obj = GrabbedImage()
                image_obj.source = GrabSourceType.BING.value
                src = image.get_attribute('src')
                if self.__is_http_url(src):
                    image_obj.url = src
                else:
                    image_obj.base64 = src
                # links for small image
                images_objects.append(image_obj)

        browser.close()

        return images_objects

    def __is_http_url(self, src):
        result = unicodedata.normalize('NFKD', src).encode('ascii', 'ignore')
        return result[:4] == "http"