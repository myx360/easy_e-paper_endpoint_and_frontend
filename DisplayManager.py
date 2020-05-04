import abc
from enum import Enum
from threading import Lock

from epaper.EpaperDisplay import EpaperDisplay
from Singleton import Singleton


class DisplayMode(Enum):
    IMAGE = 1
    TORRENTS = 2


class DisplayManager(object, metaclass=abc.ABCMeta):
    @staticmethod
    @abc.abstractmethod
    def get_mode() -> DisplayMode:
        """Shows this manager's representative DisplayMode"""

    @abc.abstractmethod
    def update_display(self, epd: EpaperDisplay):
        """Updates the display on the epaper"""

    @abc.abstractmethod
    def new_image_to_display(self) -> bool:
        """Returns True if there is a new image to display"""


class DisplayManagerSwitcher(object, metaclass=Singleton):
    def __init__(self, switch_mode_lock: Lock, starting_mode=DisplayMode.TORRENTS):
        self.__display_managers = {}
        self.__current_mode = starting_mode
        self.__proposed_mode = starting_mode
        self.__switch_mode_lock = switch_mode_lock

    def register(self, display_manager: DisplayManager):
        self.__display_managers[display_manager.get_mode()] = display_manager

    def get_manager(self) -> DisplayManager:
        with self.__switch_mode_lock:
            self.__current_mode = self.__proposed_mode
            return self.__display_managers[self.__current_mode]

    def propose_mode(self, display_mode: DisplayMode):
        with self.__switch_mode_lock:
            self.__proposed_mode = display_mode

    def has_mode_proposal(self) -> bool:
        return self.__proposed_mode != self.__current_mode
