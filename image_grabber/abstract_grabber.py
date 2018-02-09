from abc import ABCMeta, abstractmethod


class AbstractGrabber:
    __metaclass__ = ABCMeta

    @property
    def full_image(self):
        """ boolean representing if downloaded image is full size or thumbnail """
        raise NotImplementedError

    @abstractmethod
    def get_images_url(self, keyword):
        """ it should return an array of GrabbedImage objects with at least base64 or url defined """
        pass
