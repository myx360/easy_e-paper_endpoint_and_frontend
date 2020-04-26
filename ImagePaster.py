from abc import abstractmethod


class ImagePaster(object):
    @abstractmethod
    def paste_image(self):
        """Pastes an image on top of the supplied epaper_image"""

    @abstractmethod
    def size(self):
        """Returns size of the image to be pasted as tuple (x,y)"""
