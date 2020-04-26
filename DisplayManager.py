from abc import abstractmethod

from epaper.EpaperDisplay import EpaperDisplay


class DisplayManager(object):
    @abstractmethod
    def update_display(self, epd: EpaperDisplay):
        """Updates the display on the epaper"""

    @abstractmethod
    def new_image_to_display(self):
        """Returns True if there is a new image to display"""
