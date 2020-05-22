import copy

from PIL import ImageFont, Image

from EpaperImage import EpaperImage
from ImageManager import ImageManager
from Images import Images
from display__torrents.TorrentListImagePaster import TorrentListImagePaster


class PlainTorrentImageManager(ImageManager):
    """ Creates and manages the black and the colour images for the torrent lists
        on a plain background
    """
    torrent_list_xy = (5, 5)
    line_width = 390
    line_height = 35

    def __init__(self, font_text: ImageFont, font_title=None):
        self.__epaper_image = copy.deepcopy(Images.epaper_plain_background)
        self.__background = Images.epaper_plain_background
        self.font = font_text
        self.font_bold = font_text if font_title is None else font_title
        self.__list_printer = TorrentListImagePaster(self.__epaper_image,
                                                     self.torrent_list_xy,
                                                     self.line_width,
                                                     self.line_height,
                                                     font_text,
                                                     font_title)

    def generate_display_image(self, **kwargs) -> EpaperImage:
        self.__list_printer.paste_image()
        return self.__epaper_image

    def get_black_image(self) -> Image:
        return self.__epaper_image.image_black

    def get_colour_image(self) -> Image:
        return self.__epaper_image.image_colour

    def get_epaper_image(self) -> EpaperImage:
        return self.__epaper_image

    def reset_to_background(self):
        self.__epaper_image = copy.deepcopy(self.__background)
        self.__list_printer = TorrentListImagePaster(self.__epaper_image, self.torrent_list_xy,
                                                     self.line_width, self.line_height, self.font,
                                                     self.font_bold)

    def add_torrent(self, text: str, percentage: float = None):
        """ Only adds torrents to the list if there is space on the display.
        :param text: Text to display for list item.
        :param percentage: will not add the percentage icons if None supplied.
        :return: True if torrent added, false if not added
        """
        return self.__list_printer.add_torrent(text, percentage)

    def add_title(self, text: str):
        return self.__list_printer.add_title(text)
