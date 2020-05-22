import abc
import logging
from enum import Enum
from threading import Lock

from custom_errors.DisplayManagerError import DisplayManagerError
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

    @staticmethod
    @abc.abstractmethod
    def printable_name() -> str:
        """Returns the name of this display manager"""

    @abc.abstractmethod
    def can_register(self) -> bool:
        """Returns true if display manager is set up and ready to be registered"""

    @abc.abstractmethod
    def update_display(self, epd: EpaperDisplay):
        """Updates the display on the epaper"""

    @abc.abstractmethod
    def new_image_to_display(self, force_update: bool) -> bool:
        """Returns True if there is a new image to display"""


class DisplayManagerSwitcher(object, metaclass=Singleton):
    """
        Thread-safe switching of display managers.
    """

    def __init__(self, switch_mode_lock: Lock, display_manager: DisplayManager):
        if not display_manager.can_register():
            raise DisplayManagerError('Failed to initialise display manager, cannot register DM: %s'
                                      .format(display_manager.printable_name()))
        self.__display_managers = {display_manager.get_mode(): display_manager}
        self.__current_mode = display_manager.get_mode()
        self.__proposed_mode = display_manager.get_mode()
        self.__switch_mode_lock = switch_mode_lock

    def register(self, display_manager: DisplayManager):
        if display_manager.can_register():
            self.__display_managers[display_manager.get_mode()] = display_manager
            logging.info('Registered display manager: %s', display_manager.printable_name())
        else:
            logging.info('Unable to register display manager: %s', display_manager.printable_name())

    def pick_writing_manager(self) -> DisplayManager:
        with self.__switch_mode_lock:
            self.__current_mode = self.__proposed_mode
            return self.__display_managers[self.__current_mode]

    def get_manager(self, display_mode: DisplayMode):
        """Beware, not thread-safe. Handle carefully."""
        return self.__display_managers[display_mode]

    def propose_mode(self, display_mode: DisplayMode):
        if self.__display_managers.get(display_mode, None) is not None:
            with self.__switch_mode_lock:
                self.__proposed_mode = display_mode
            logging.info('Proposed display mode: %s', display_mode.name)
        else:
            error_msg = 'Proposed unregistered display mode {}'.format(display_mode.name)
            logging.error(error_msg)
            raise KeyError(error_msg)

    def has_mode_proposal(self) -> bool:
        return self.__proposed_mode != self.__current_mode
