#!/usr/bin/python3
# -*- coding:utf-8 -*-
import logging
import sys
import traceback
import time
import yaml

import epd4in2bc

from ChilliGardenImageManager import ChilliGardenImageManager
from Definitions import Definitions
from Exceptions.ScriptFailureError import ScriptFailureError
from TorrentDataManager import TorrentDataManager


class Main(object):
    def __init__(self, username, password):
        self.__epd = epd4in2bc.EPD()
        self.__torrent_data_manager = TorrentDataManager(username, password)
        self.__torrent_data_manager.fetch_torrent_data()

        self.__epd.init()
        # Initial clear reduces the risk of damage to the e-paper:
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

            # using bare except rather than except Exception to avoid any possibility of leaving
            # the epd in full power mode. This is only acceptable because I exit the program here
            except:
                logging.error('Error:')
                logging.error(traceback.format_exc())
                self.__epd.full_exit()
                exit(1)


logging.basicConfig(level=logging.ERROR)

username, password = sys.argv[1], sys.argv[2]

if not username or not password:
    try:
        f = open(Definitions.CONFIG_FILE_PATH)
        config = yaml.safe_load(f)
        f.close()
        username, password = config['username'], config['password']
    except FileNotFoundError:
        logging.error('Config file, config.yml not found. Stopping.')
        exit(1)
    except yaml.YAMLError as e:
        logging.error('''Error reading the config.yml file. Stopping.
(Hint - The config.yml file should contain only the following (with username/password filled in)
username:
password:''')
        exit(1)
main = Main(username, password)
main.start()

