#!/usr/bin/python
# -*- coding:utf-8 -*-
import logging
import sys
import traceback
import time

import epd4in2bc

from ChilliGardenImageManager import ChilliGardenImageManager
from Definitions import Definitions
from TorrentDataManager import TorrentDataManager


class Main(object):
    def __init__(self, username, password):
        self.__epd = epd4in2bc.EPD()
        self.__torrent_data_manager = TorrentDataManager(username, password)
        self.__torrent_data_manager.fetch_torrent_data()

        self.__epd.init()
        # Initial clear reduces the risk of damage to the epaper:
        self.__epd.Clear()
        self.__epd.sleep()
        self.__image_manager = ChilliGardenImageManager(Definitions.TEXT_FONT, Definitions.BOLD_FONT)
        self.__refreshes = 0

    def update_epaper_image(self, torrents):
        image_manager = self.__image_manager
        epd = self.__epd
        image_manager.reset_image_to_background()

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

        image_manager.print_torrents_list()

        self.__refreshes += 1
        epd.init()

        if self.__refreshes > 5:
            epd.Clear()
            self.__refreshes = 0

        epd.display(epd.getbuffer(image_manager.get_black_image()), epd.getbuffer(image_manager.get_colour_image()))
        epd.sleep()

    def start(self):
        torrents = {}

        while True:
            try:
                logging.debug('Attempting to fetch torrents...')
                self.__torrent_data_manager.fetch_torrent_data()
                latest_torrents = self.__torrent_data_manager.get_torrents()

                if torrents != latest_torrents:
                    logging.debug('New torrents found. Updating image')
                    torrents = latest_torrents
                    self.update_epaper_image(torrents)

                time.sleep(60)

            except KeyboardInterrupt:
                logging.info('ctrl + c:')
                self.__epd.full_exit()
                exit()

            except:
                logging.error('Error:')
                logging.error(traceback.format_exc())
                self.__epd.full_exit()
                exit()


logging.basicConfig(level=logging.ERROR)
main = Main(sys.argv[1], sys.argv[2])
main.start()
