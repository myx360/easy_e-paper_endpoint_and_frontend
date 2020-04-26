import logging

from DisplayManager import DisplayManager
from torrent_display.ChilliGardenImageManager import ChilliGardenImageManager
from Definitions import Definitions
from torrent_display.PlainTorrentImageManager import PlainTorrentImageManager
from torrent_display.TorrentDataManager import TorrentDataManager, Torrents


class TorrentDisplayManager(DisplayManager):
    def __init__(self, username, password, chilli_mode=True):
        if chilli_mode:
            self.__image_manager = ChilliGardenImageManager(Definitions.TEXT_FONT, Definitions.BOLD_FONT)
        else:
            self.__image_manager = PlainTorrentImageManager(Definitions.TEXT_FONT, Definitions.BOLD_FONT)
        self.__torrents = Torrents()
        self.__torrent_data_manager = TorrentDataManager(username, password)

    def update_display(self, epd):
        image_manager = self.__image_manager
        image_manager.reset_image_to_background()
        torrents = self.__torrents

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

        image_manager.generate_display_image()

        epd.safe_display(image_manager.get_black_image(), image_manager.get_colour_image())

    def new_image_to_display(self):
        logging.debug('Attempting to fetch torrents...')
        latest_torrents = self.__torrent_data_manager.get_torrents()
        requires_refresh = self.__torrents != latest_torrents
        if requires_refresh:
            logging.debug('New torrents found. Updating image')
            self.__torrents = latest_torrents
        return requires_refresh
