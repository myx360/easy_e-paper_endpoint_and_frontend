#!/usr/bin/python3
# -*- coding:utf-8 -*-
import logging
import threading
import traceback
import time

from PIL import Image
from flask import Flask, request
from threading import Lock

from werkzeug.exceptions import BadRequestKeyError

from Configuration import Configuration, ConfigKeys
from Definitions import Definitions
from DisplayManager import DisplayMode, DisplayManagerSwitcher
from display__picture.PictureDisplayManager import PictureDisplayManager
from epaper.EpaperDisplay import EpaperDisplay
from display__torrents.TorrentDisplayManager import TorrentDisplayManager


class Main(object):
    def __init__(self, dm_holder: DisplayManagerSwitcher):
        self.__epd = EpaperDisplay()
        self.__dm_holder = dm_holder

    def display_loop(self):
        epd = self.__epd

        while True:
            try:
                switching_manager = self.__dm_holder.has_mode_proposal()
                display_manager = dm_switcher.pick_writing_manager()

                if display_manager.new_image_to_display(switching_manager):
                    display_manager.update_display(epd)
                time.sleep(2)

            except KeyboardInterrupt:
                logging.info('ctrl + c:')
                epd.full_exit()
                exit()

            # using bare except rather than except Exception to avoid any possibility of leaving
            # the epd in full power mode.
            except:
                logging.error('Error:')
                logging.error(traceback.format_exc())
                epd.full_exit()
                exit(1)


logging.basicConfig(filename='torrent_box.log', level=logging.INFO)
config = Configuration()


# Setup display manager switcher and add PictureDisplayManager
image_lock = Lock()
switch_mode_lock = Lock()
dm_switcher = DisplayManagerSwitcher(switch_mode_lock, PictureDisplayManager(image_lock))

dm_switcher.register(TorrentDisplayManager(config, config.get(ConfigKeys.chilli_display_mode)))

# Set starting mode, if available
starting_display_mode = DisplayMode[config.get(ConfigKeys.default_display_mode)]
if starting_display_mode:
    try:
        dm_switcher.propose_mode(starting_display_mode)
    except KeyError:
        logging.error("default_display_mode is %s but this was not accepted, is it configured in config.yml ?", config.get(ConfigKeys.default_display_mode))


main = Main(dm_switcher)
app = Flask(__name__)


upload_lock = Lock()


def propose_image(image_black=None, image_colour=None):
    try:
        with image_lock:
            if image_black:
                image_black.save(Definitions.TEMP_IMAGE_BLACK)
            if image_colour:
                image_colour.save(Definitions.TEMP_IMAGE_COLOUR)
        if image_black or image_colour:
            dm_switcher.propose_mode(DisplayMode.IMAGE)
    except FileNotFoundError:
        logging.error('Could not write image to the upload folder')


@app.route('/display_image', methods=['POST'])
def display_image():
    try:
        if request.files:
            try:
                image_black = Image.open(request.files['image_black']).copy()
            except BadRequestKeyError:
                image_black = None
            except IOError:
                return 'Bad request, not an image file', 400

            try:
                image_colour = Image.open(request.files['image_colour']).copy()
            except BadRequestKeyError:
                image_colour = None
            except IOError:
                return 'Bad request, not an image file', 400

            if image_black or image_colour:
                threading.Thread(target=propose_image,
                                 kwargs={'image_black': image_black,
                                         'image_colour': image_colour}
                                 ).start()
                return 'OK', 202
    except KeyError:
        return 'Image display manager unavailable', 500
    return 'Bad request', 400


@app.route('/torrents', methods=['POST'])
def display_torrents():
    if request.args.get('chilli') is not None:
        dm_switcher.get_manager(DisplayMode.TORRENTS).set_image_manager(request.args.get('chilli') == 'True')
    try:
        dm_switcher.propose_mode(DisplayMode.TORRENTS)
        return 'ACCEPTED', 202
    except KeyError:
        return 'DISPLAY MODE UNAVAILABLE', 500


if __name__ == '__main__':
    if config.get(ConfigKeys.enable_api):
        hostname = config.get(ConfigKeys.flask_hostname)
        port = config.get(ConfigKeys.flask_port)
        threading.Thread(target=app.run, args=(hostname, port), daemon=True).start()
    main.display_loop()
