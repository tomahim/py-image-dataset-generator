from abc import ABCMeta, abstractmethod


class AbstractGrabber:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_images_url(self, keyword):
        """it should return an array of images (url, extension) matching the keyword"""
        pass
