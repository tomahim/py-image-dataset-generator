import json
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from abstract_grabber import AbstractGrabber
from settings import *


class GoogleGrabber(AbstractGrabber):
    """Grab images from google search"""

    def __init__(self):
        pass

    def get_images_url(self, keyword):
        query = keyword.split()
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
            link, file_type = json.loads(json_content)["ou"], json.loads(json_content)["ity"]
            images_urls.append((link, file_type))

        browser.close()
        return images_urls
