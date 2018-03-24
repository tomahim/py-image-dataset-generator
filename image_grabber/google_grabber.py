import json
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from typing import List

from .abstract_grabber import AbstractGrabber
from .grabbed_image import GrabbedImage
from .grab_settings import *
from utils.utils import StringUtil


class GoogleGrabber(AbstractGrabber):
    """Grab images from google search"""

    full_image = True
    GOOGLE_URL = "https://www.google.co.in/search?q=%s&source=lnms&tbm=isch"

    def __init__(self):
        pass

    def get_images_url(self, keyword: str, nb_images: int) -> List[GrabbedImage]:
        query = keyword.split()
        query = '+'.join(query)
        url = self.GOOGLE_URL % query

        print('> searching image on Google : ' + url)

        options = webdriver.ChromeOptions()

        browser = webdriver.Chrome(chrome_options=options)

        browser.get(url)
        time.sleep(2)

        elem = browser.find_element_by_tag_name("body")

        # scroll to fire the infinite scroll event and load more images
        no_of_pages_down = 20 if nb_images < 300 else 100
        while no_of_pages_down:
            elem.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.2)
            no_of_pages_down -= 1
            try:
                show_more_btn = browser.find_element_by_id("smb")
                if show_more_btn.is_displayed():
                    show_more_btn.click()
            except Exception as e:
                pass


        images_objects = []
        if self.full_image:
            images = browser.find_elements_by_class_name("rg_meta")
            for image in images:
                image_obj = GrabbedImage()
                image_obj.source = GrabSourceType.GOOGLE.value
                json_content = image.get_attribute('innerHTML')
                # links for Large original image
                image_obj.url = json.loads(json_content)["ou"]
                image_obj.extension = json.loads(json_content)["ity"]
                images_objects.append(image_obj)
        else:
            images = browser.find_elements_by_class_name("rg_ic")
            for image in images:
                image_obj = GrabbedImage()
                image_obj.source = GrabSourceType.GOOGLE.value
                src = image.get_attribute('src')
                if StringUtil.is_http_url(src):
                    image_obj.url = src
                else:
                    image_obj.base64 = src
                # links for small image
                images_objects.append(image_obj)

        browser.close()

        return images_objects
