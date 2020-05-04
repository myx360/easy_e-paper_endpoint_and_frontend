import os
import logging

from Definitions import Definitions
from DisplayManager import DisplayManager, DisplayMode
from display__picture.PictureImageManager import PictureImageManager
from epaper.EpaperDisplay import EpaperDisplay
from EpaperImage import EpaperImage


class PictureDisplayManager(DisplayManager):

    def __init__(self, image_lock):
        self.__current_image = self.__proposed_image = EpaperImage()
        self.__image_manager = PictureImageManager()
        self.__lock = image_lock

    @staticmethod
    def get_mode():
        return DisplayMode.IMAGE

    def update_display(self, epd: EpaperDisplay):
        self.__current_image = self.__proposed_image
        if self.__current_image.image_black or self.__current_image.image_colour:
            with self.__lock:
                epd.safe_display(self.__current_image)
        elif os.path.isfile(Definitions.READY_IMAGE_BLACK):
            with self.__lock:
                self.__current_image = self.__proposed_image = self.__image_manager.generate_display_image(Definitions.READY_IMAGE_BLACK)
                epd.safe_display(self.__current_image)
        else:
            logging.error('No picture to display.')

    def new_image_to_display(self):
        with self.__lock:
            if os.path.isfile(Definitions.TEMP_IMAGE_BLACK):
                self.__image_manager.reset_to_background()
                self.__proposed_image = self.__image_manager.generate_display_image(Definitions.TEMP_IMAGE_BLACK, None)
                os.remove(Definitions.TEMP_IMAGE_BLACK)
                self.__image_manager.reset_to_background()
        return self.__proposed_image != self.__current_image
