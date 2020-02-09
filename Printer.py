from abc import abstractmethod
import EpaperImage


class Printer(object):
    @abstractmethod
    def print(self, epaper_image: EpaperImage):
        """Pastes an image onto the supplied epaper_image"""

    @abstractmethod
    def size(self):
        """Returns size of the image to be pasted as tuple (x,y)"""
