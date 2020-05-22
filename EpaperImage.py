from __future__ import annotations
import copy

from PIL import Image

from Definitions import Definitions
from custom_errors.EpaperImageError import EpaperImageError


class EpaperImage(object):
    def __init__(self, image_black: Image = None, image_colour: Image = None):
        if image_black:
            self.size = image_black.size
        elif image_colour:
            self.size = image_colour.size
        else:
            self.size = Definitions.DISPLAY_SIZE
        self.image_black = None if image_black is None else copy.copy(image_black)
        self.image_colour = None if image_colour is None else copy.copy(image_colour)

    def paste_separate_images(self, black, colour, xy) -> EpaperImage:
        if black is not None:
            if self.image_black is None:
                raise EpaperImageError('Tried to paste to non-existent e-paper image')
            self.image_black.paste(black, xy)
        if colour is not None:
            if self.image_colour is None:
                raise EpaperImageError('Tried to paste to non-existent e-paper image')
            self.image_colour.paste(colour, xy)
        return self

    def paste(self, epaper_image, xy) -> EpaperImage:
        if isinstance(epaper_image, EpaperImage):
            return self.paste_separate_images(epaper_image.image_black, epaper_image.image_colour, xy)
        raise EpaperImageError('Tried to paste object as an EpaperImage')

    def __eq__(self, other):
        if isinstance(other, EpaperImage):
            return self.image_black == other.image_black and self.image_colour == other.image_colour
        return False
