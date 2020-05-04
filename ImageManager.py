import abc

from PIL import Image

from EpaperImage import EpaperImage


class ImageManager(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def reset_to_background(self):
        """resets to the background image, often blank"""

    @abc.abstractmethod
    def get_black_image(self) -> Image:
        """"""

    @abc.abstractmethod
    def get_colour_image(self) -> Image:
        """"""

    @abc.abstractmethod
    def generate_display_image(self, args) -> EpaperImage:
        """returns the final generated image"""
