import os
import logging

from Definitions import Definitions
from DisplayManager import DisplayManager, DisplayMode
from display__picture.PictureImageManager import PictureImageManager
from epaper.EpaperDisplay import EpaperDisplay
from EpaperImage import EpaperImage


class PictureDisplayManager(DisplayManager):
    def __init__(self, image_lock):
        self.__current_image = EpaperImage()
        self.__image_manager = PictureImageManager()
        self.__image_lock = image_lock
        self.prepare_upload_folder()

    def can_register(self) -> bool:
        return True

    @staticmethod
    def printable_name() -> str:
        return 'Image display - crops, resizes and anti-aliases a black and/or a colour image.'

    @staticmethod
    def get_mode():
        logging.info('Proposed display mode: %s', DisplayMode.IMAGE.name)
        return DisplayMode.IMAGE

    @staticmethod
    def prepare_upload_folder():
        if not os.path.isdir(Definitions.UPLOAD_FOLDER):
            os.makedirs(Definitions.UPLOAD_FOLDER)
        for path in [Definitions.TEMP_IMAGE_BLACK, Definitions.TEMP_IMAGE_COLOUR]:
            if os.path.isfile(path):
                os.remove(path)

    def update_display(self, epd: EpaperDisplay):
        black_filepath = Definitions.READY_IMAGE_BLACK if os.path.isfile(Definitions.READY_IMAGE_BLACK) else None
        colour_filepath = Definitions.READY_IMAGE_COLOUR if os.path.isfile(Definitions.READY_IMAGE_COLOUR) else None

        self.__current_image = self.__image_manager.get_epaper_image()
        if self.__current_image.image_black or self.__current_image.image_colour:
            with self.__image_lock:
                epd.safe_display(self.__current_image)
        elif black_filepath or colour_filepath:
            with self.__image_lock:
                self.__current_image = self.__image_manager.generate_display_image(black_filepath, colour_filepath)
                epd.safe_display(self.__current_image)
        else:
            logging.error('No picture to display.')

    def new_image_to_display(self):
        with self.__image_lock:
            black_filepath = Definitions.TEMP_IMAGE_BLACK if os.path.isfile(Definitions.TEMP_IMAGE_BLACK) else None
            colour_filepath = Definitions.TEMP_IMAGE_COLOUR if os.path.isfile(Definitions.TEMP_IMAGE_COLOUR) else None

            if black_filepath or colour_filepath:
                self.__image_manager.reset_to_background()
                self.__image_manager.generate_display_image(black_filepath, colour_filepath)
                if black_filepath:
                    os.remove(Definitions.TEMP_IMAGE_BLACK)
                if colour_filepath:
                    os.remove(Definitions.TEMP_IMAGE_COLOUR)
        return self.__current_image != self.__image_manager.get_epaper_image()
