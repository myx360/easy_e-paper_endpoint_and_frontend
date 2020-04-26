import numpy
from PIL import Image, ImageDraw

from EpaperImage import EpaperImage
from torrent_display.PercentImagePaster import PercentImagePaster
from ImagePaster import ImagePaster
from utils.TextWrapper import TextWrapper


class TorrentList(object):
    def __init__(self, max_size: int):
        self.max_size = max_size
        self.height = 0
        self.size = (max_size[0], self.height)
        blank_image = Image.new('1', max_size, 255)
        self.list_image = EpaperImage(blank_image, blank_image)

    def add_item_to_list(self, line_image: EpaperImage):
        if self.height + line_image.image_black.size[1] <= self.max_size[1]:
            self.list_image.paste(line_image, (0, self.height))
            self.height += line_image.image_black.size[1]
            return True
        return False


class TorrentListImagePaster(ImagePaster):
    def __init__(self, epaper_image: EpaperImage, xy, line_width: int, line_height: int, font_text, font_title):
        max_size_of_list = (line_width, numpy.subtract(epaper_image.size, xy)[1])
        self.torrent_list = TorrentList(max_size_of_list)
        self.epaper_image = epaper_image
        self.__font_text = font_text
        self.__font_title = font_text if font_title is None else font_title
        self.__top_left = xy
        self.__line_width = line_width
        self.__line_height = line_height

    def size(self):
        return self.torrent_list.size

    def paste_image(self):
        self.epaper_image.paste(self.torrent_list.list_image, self.__top_left)

    def add_torrent(self, text: str, percentage: float = None, font=None, line_height=None):
        if font is None:
            font = self.__font_text
        if line_height is None:
            line_height = self.__line_height
        blank_image = Image.new('1', (self.__line_width, line_height), 255)
        line_image = EpaperImage(blank_image, blank_image)
        xy = (1, 0)  # get from percent image

        if percentage is not None:
            percent_paster = PercentImagePaster(line_image, xy, percentage)
            percent_paster.paste_image()
            xy = (percent_paster.size()[0] + 5, 4)

        self.draw_text_image(line_image, text, font, xy)
        return self.torrent_list.add_item_to_list(line_image)

    def add_title(self, text: str, font=None, line_height=None):
        if font is None:
            font = self.__font_title
        f_size_x, f_size_y = font.getsize(text)
        if line_height is None and self.torrent_list.height is 0:
            line_height = f_size_y + 8
        elif line_height is None:
            line_height = f_size_y + 10

        blank_image = Image.new('1', (self.__line_width, line_height), 255)
        line_image = EpaperImage(blank_image, blank_image)
        xy = (0, 1)
        if self.torrent_list.height > 0:
            xy = (0, 5)
        self.draw_text_image(line_image, text, font, xy)
        return self.torrent_list.add_item_to_list(line_image)

    def draw_text_image(self, line_image: EpaperImage, text: str, font, xy):
        max_text_width = self.__line_width - xy[0]
        draw = ImageDraw.Draw(line_image.image_black)
        wrapper = TextWrapper(text, font, max_text_width)
        wrapped_text = wrapper.generate_wrapped_text()
        draw.multiline_text(xy, wrapped_text, font=font, fill=0)

