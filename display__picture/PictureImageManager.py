import copy
import os

from PIL import Image

from Definitions import Definitions
from EpaperImage import EpaperImage
from ImageManager import ImageManager


class PictureImageManager(ImageManager):

    def __init__(self, size=Definitions.DISPLAY_SIZE):
        self.size = size
        self.__background = EpaperImage(Image.new('L', size, 'white'), Image.new('L', size, 'white'))
        self.__epaper_image = copy.deepcopy(self.__background)

    def reset_to_background(self):
        self.__epaper_image = copy.deepcopy(self.__background)

    def get_black_image(self) -> Image:
        return self.__epaper_image.image_black

    def get_colour_image(self) -> Image:
        return self.__epaper_image.image_colour

    def generate_display_image(self, black_image_path: str = None, colour_image_path: str = None) -> EpaperImage:
        if black_image_path:
            self.__epaper_image.image_black = self._generate_image(black_image_path)
        if colour_image_path:
            self.__epaper_image.image_colour = self._generate_image(colour_image_path)

        self.__epaper_image.image_black.save(Definitions.READY_IMAGE_BLACK)
        self.__epaper_image.image_colour.save(Definitions.READY_IMAGE_COLOUR)
        return self.__epaper_image

    def _generate_image(self, image_path: str) -> Image:
        if os.path.isfile(image_path):
            image = Image.open(image_path)
            return self.get_cropped_image(image).resize(self.size, Image.ANTIALIAS).convert('1')
        raise FileNotFoundError("Could not find a file at %s", image_path)

    def get_cropped_image(self, image) -> Image:
        width = image.size[0]
        height = image.size[1]

        aspect = width / float(height)

        target_width = self.size[0]
        target_height = self.size[1]

        target_aspect = target_width / float(target_height)

        if aspect > target_aspect:
            # Then crop the left and right edges:
            new_width = int(target_aspect * height)
            offset = (width - new_width) / 2
            resize = (offset, 0, width - offset, height)
        else:
            # ... crop the top and bottom:
            new_height = int(width / target_aspect)
            offset = (height - new_height) / 2
            resize = (0, offset, width, height - offset)
        return image.crop(resize)

