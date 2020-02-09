import copy


class EpaperImage(object):
    def __init__(self, image_black, image_colour):
        self.size = image_black.size
        self.image_black = None if image_black is None else copy.copy(image_black)
        self.image_colour = None if image_colour is None else copy.copy(image_colour)

    def paste_separate_images(self, black, colour, xy):
        if black is not None:
            if self.image_black is None:
                raise Exception('Tried to print to non-existent epaper image')
            self.image_black.paste(black, xy)
        if colour is not None:
            if self.image_colour is None:
                raise Exception('Tried to print to non-existent epaper image')
            self.image_colour.paste(colour, xy)
        return self

    def paste(self, epaper_image, xy):
        if isinstance(epaper_image, EpaperImage):
            return self.paste_separate_images(epaper_image.image_black, epaper_image.image_colour, xy)
        raise Exception('Tried to paste something as an EpaperImage')
