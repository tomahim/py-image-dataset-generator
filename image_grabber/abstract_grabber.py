from abc import ABCMeta, abstractmethod
from .grabbed_image import GrabbedImage
from typing import List


class AbstractGrabber:
    __metaclass__ = ABCMeta

    @property
    def full_image(self) -> bool:
        """ If true grab the full image size, if false the thumbnail (if available) """
        raise NotImplementedError

    @abstractmethod
    def get_images_url(self, keyword: str, nb_images: int) -> List[GrabbedImage]:
        """ it should return extracted data with at least base64 or url defined """
        pass
