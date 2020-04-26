import threading

from epaper.drivers import epd4in2bc


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class EpaperDisplay(object):
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
            self.__epd.init()
            self.__epd.Clear()
            self.__epd.sleep()

    def safe_display(self, black_image, colour_image):
        with self.__lock:
            if self.__refreshes > 5:
                self.__epd.init()
                self.__epd.Clear()
                self.__refreshes = 0
            self.__refreshes += 1
            self.__epd.init()
            self.__epd.display(self.__epd.getbuffer(black_image),
                               self.__epd.getbuffer(colour_image))
            self.__epd.sleep()

    def full_exit(self):
        self.__epd.full_exit()

    def sleep(self):
        self.__epd.sleep()
