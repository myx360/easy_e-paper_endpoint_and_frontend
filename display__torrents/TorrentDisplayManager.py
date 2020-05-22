import logging
import sys
from threading import Lock

from Configuration import Configuration, ConfigKeys
from DisplayManager import DisplayManager, DisplayMode
from display__torrents.ChilliGardenImageManager import ChilliGardenImageManager
from Definitions import Definitions
from display__torrents.PlainTorrentImageManager import PlainTorrentImageManager
from display__torrents.TorrentDataManager import TorrentDataManager, Torrents
from epaper.EpaperDisplay import EpaperDisplay


class TorrentDisplayManager(DisplayManager):
    def __init__(self, config: Configuration, chilli_mode=True):
        self.__switch_image_manager_lock = Lock()
        self.__torrents = Torrents()
        self.config = config
        self.switch_manager_flag = False

        username, password = self.__get_user_and_pass()
        self.__ready = username and password

        if self.__ready:
            self.__torrent_data_manager = TorrentDataManager(username, password)
            with self.__switch_image_manager_lock:
                if chilli_mode:
                    self.__image_manager = ChilliGardenImageManager(Definitions.TEXT_FONT, Definitions.BOLD_FONT)
                else:
                    self.__image_manager = PlainTorrentImageManager(Definitions.TEXT_FONT, Definitions.BOLD_FONT)

    def __get_user_and_pass(self):
        try:
            return sys.argv[1], sys.argv[2]
        except IndexError:
            return self.config.get(ConfigKeys.transmission_user), self.config.get(ConfigKeys.transmission_password)

    @staticmethod
    def get_mode() -> DisplayMode:
        return DisplayMode.TORRENTS

    def can_register(self) -> bool:
        return self.__ready

    @staticmethod
    def printable_name() -> str:
        return 'Torrent display - displays torrents returned by Transmission client'

    def set_image_manager(self, chilli_mode: bool):
        with self.__switch_image_manager_lock:
            self.__image_manager = ChilliGardenImageManager(Definitions.TEXT_FONT, Definitions.BOLD_FONT)\
                if chilli_mode \
                else PlainTorrentImageManager(Definitions.TEXT_FONT, Definitions.BOLD_FONT)
            self.switch_manager_flag = True

    def update_display(self, epd: EpaperDisplay):
        with self.__switch_image_manager_lock:
            image_manager = self.__image_manager
            image_manager.reset_to_background()
            torrents = self.__torrents
            self.switch_manager_flag = False

            if len(torrents.downloading) > 0:
                image_manager.add_title('Downloading:')
                for torrent in torrents.downloading:
                    image_manager.add_torrent(torrent.name, float(torrent.percent.rstrip('%')))

            if len(torrents.completed) > 0:
                image_manager.add_title('Completed:')
                for torrent in torrents.completed:
                    image_manager.add_torrent(torrent.name, float(torrent.percent.rstrip('%')))

            if len(torrents.stopped) > 0:
                image_manager.add_title('Stopped:')
                for torrent in torrents.stopped:
                    image_manager.add_torrent(torrent.name, float(torrent.percent.rstrip('%')))

            epd.safe_display(image_manager.generate_display_image())

    def new_image_to_display(self) -> bool:
        logging.debug('Attempting to fetch torrents...')
        latest_torrents = self.__torrent_data_manager.get_torrents()
        requires_refresh = self.__torrents != latest_torrents
        if requires_refresh:
            logging.debug('Updating torrents image')
            self.__torrents = latest_torrents
        return requires_refresh or self.switch_manager_flag
