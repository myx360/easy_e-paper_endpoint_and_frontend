#!/usr/bin/python3
# -*- coding:utf-8 -*-
import logging
import sys
import traceback
import time
import yaml


from Definitions import Definitions
from epaper.EpaperDisplay import EpaperDisplay
from torrent_display.TorrentDisplayManager import TorrentDisplayManager

CONFIG_FILE_HINT = '''

Hint:- If running as a service, the config.yml file should be owned by root with 400 permissions and contain the following \
(with <username> and <password> filled in)
username: <username>
password: <password>

or else if running just as a script, run with:
    python3 main.py <username> <password>
'''


class Main(object):
    def __init__(self, username, password):
        self.epd = EpaperDisplay()
        self.torrent_display = TorrentDisplayManager(username, password)

    def start(self):
        display = self.torrent_display
        epd = self.epd

        while True:
            try:
                if display.new_image_to_display():
                    display.update_display(epd)
                time.sleep(60)

            except KeyboardInterrupt:
                logging.info('ctrl + c:')
                epd.full_exit()
                exit()

            # using bare except rather than except Exception to avoid any possibility of leaving
            # the epd in full power mode. This is acceptable because I exit the program here
            except:
                logging.error('Error:')
                logging.error(traceback.format_exc())
                epd.full_exit()
                exit(1)


def get_transmission_login():
    try:
        return sys.argv[1], sys.argv[2]
    except IndexError:
        try:
            with open(Definitions.CONFIG_FILE_PATH) as f:
                config = yaml.safe_load(f)
            return config['username'], config['password']
        except FileNotFoundError:
            logging.error('Config file, config.yml not found. Stopping.')
            exit(1)
        except yaml.YAMLError as yaml_error:
            logging.error('Error reading the config.yml file. Stopping.' + CONFIG_FILE_HINT)
            logging.debug('Error reading config.yml file: %s', str(yaml_error))
            exit(1)
        except KeyError:
            logging.error('Could not find the transmission login details, please put them in the config.yml file' + CONFIG_FILE_HINT)
            exit(1)


logging.basicConfig(level=logging.INFO)

transmission_user, transmission_pass = get_transmission_login()
main = Main(transmission_user, transmission_pass)
main.start()
