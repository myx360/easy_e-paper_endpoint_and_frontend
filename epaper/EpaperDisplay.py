import logging
import threading

from epaper.drivers import epd4in2bc
from EpaperImage import EpaperImage
from Singleton import Singleton


class EpaperDisplay(object, metaclass=Singleton):
    """Wraps the display drivers with logic preventing unsafe behaviour. Probably overkill making it a singleton
    """
    def __init__(self):
        self.__lock = threading.Lock()
        self.__refreshes = 0
        self.__epd = epd4in2bc.EPD()
        # Initial clear reduces the risk of damage to the e-paper:
        self.safe_clear()

    def safe_clear(self):
        with self.__lock:
            try:
                self.__epd.init()
                logging.debug("Safely clearing e-paper")
                self.__epd.Clear()
                self.__epd.sleep()
            except:
                self.__epd.sleep()
                raise

    def safe_display(self, epaper_image: EpaperImage):
        with self.__lock:
            try:
                if self.__refreshes > 5:
                    self.__epd.init()
                    self.__epd.Clear()
                    self.__refreshes = 0
                self.__refreshes += 1
                self.__epd.init()
                self.__epd.display(self.__epd.getbuffer(epaper_image.image_black),
                                   self.__epd.getbuffer(epaper_image.image_colour))
                self.__epd.sleep()
            except:
                self.__epd.sleep()
                raise

    def full_exit(self):
        logging.info("Safely shutting down e-paper")
        self.__epd.full_exit()

    def sleep(self):
        self.__epd.sleep()
