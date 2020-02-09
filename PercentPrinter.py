from Images import Images
import EpaperImage
from Printer import Printer


class PercentPrinter(Printer):
    percent_per_chilli_segment = (100.0/9.0)

    def __init__(self, epaper_image, xy, percent):
        self.epaper_image = epaper_image
        self.__xy = xy
        self.chillies_to_print = []

        chilli_segments = int (percent / self.percent_per_chilli_segment)

        for i in range(chilli_segments, 2, -3):
            self.chillies_to_print.append(Images.epaper_100pc)
            chilli_segments -= 3

        if chilli_segments == 1:
            self.chillies_to_print.append(Images.epaper_33pc)
        if chilli_segments == 2:
            self.chillies_to_print.append(Images.epaper_66pc)

        while len(self.chillies_to_print) < 3:
            self.chillies_to_print.append(Images.epaper_00pc)

    def print(self, epaper_image: EpaperImage):
        for i, chilli_image in enumerate(self.chillies_to_print):
            epaper_image.paste(chilli_image, (self.__xy[0] + i * chilli_image.size[0], self.__xy[1]))

    def size(self):
        return sum([chilli.size[0] for chilli in self.chillies_to_print]), Images.epaper_100pc.size[1]
