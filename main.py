#!/usr/bin/python3
# -*- coding:utf-8 -*-
import logging
import sys
import threading
import traceback
import time
from flask import Flask, request
import yaml

from threading import Lock

from Definitions import Definitions
from DisplayManager import DisplayMode, DisplayManagerSwitcher
from display__picture.PictureDisplayManager import PictureDisplayManager
from epaper.EpaperDisplay import EpaperDisplay
from display__torrents.TorrentDisplayManager import TorrentDisplayManager

CONFIG_FILE_HINT = '''

Hint:- If running as a service, the config.yml file should be owned by root with 400 permissions and contain the following \
(with <username> and <password> filled in)
username: <username>
password: <password>

or else if running just as a script, run with:
    python3 main.py <username> <password>
'''


class Main(object):
    def __init__(self, dm_holder: DisplayManagerSwitcher):
        self.__epd = EpaperDisplay()
        self.__dm_holder = dm_holder
        self.last_image_displayed = None

    def display_loop(self):
        epd = self.__epd

        while True:
            try:
                switching_manager = self.__dm_holder.has_mode_proposal()
                display_manager = dm_switcher.get_manager()

                if switching_manager:
                    display_manager.new_image_to_display()
                    display_manager.update_display(epd)
                elif display_manager.new_image_to_display():
                    self.last_image_displayed = display_manager.update_display(epd)
                time.sleep(10)

            except KeyboardInterrupt:
                logging.info('ctrl + c:')
                epd.full_exit()
                exit()

            # using bare except rather than except Exception to avoid any possibility of leaving
            # the epd in full power mode. This is acceptable because I exit the program here
            except:
                logging.error('Error:')
                logging.error(traceback.format_exc())
                logging.info('Safely stopping screen.')
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

switch_mode_lock = Lock()
dm_switcher = DisplayManagerSwitcher(switch_mode_lock)

transmission_user, transmission_pass = get_transmission_login()
dm_switcher.register(TorrentDisplayManager(transmission_user, transmission_pass))

image_lock = Lock()
dm_switcher.register(PictureDisplayManager(image_lock))

main = Main(dm_switcher)

app = Flask(__name__)


@app.route("/display_image", methods=['POST'])
def display_image():
    if request.files:
        image = request.files["image_black"]
        # propose new image to display manager
        # todo: check file type
        with image_lock:
            image.save(Definitions.TEMP_IMAGE_BLACK)
            dm_switcher.propose_mode(DisplayMode.IMAGE)
        return "OK", 202
    return "Bad request", 400


@app.route("/torrents", methods=['POST'])
def display_torrents():
    dm_switcher.propose_mode(DisplayMode.TORRENTS)
    return "OK", 202


if __name__ == '__main__':
    threading.Thread(target=app.run, args=("0.0.0.0", 5001), daemon=True).start()
    main.display_loop()
