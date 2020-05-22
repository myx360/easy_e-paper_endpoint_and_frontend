import subprocess
import logging

from Definitions import Definitions
from custom_errors.ScriptFailureError import ScriptFailureError


class Torrent(object):
    def __init__(self, name, percent, status):
        self.name = name
        self.percent = percent
        self.status = status

    def __eq__(self, other):
        if isinstance(other, Torrent):
            return self.name == other.name and self.percent == other.percent and self.status == other.status
        return False


class Torrents(object):
    def __init__(self):
        self.downloading = []
        self.completed = []
        self.stopped = []

    @staticmethod
    def __find_unmatched_torrents(list1, list2):
        for list1_torrent in list1:
            torrent_appeared = False
            for list2_torrent in list2:
                if list1_torrent == list2_torrent:
                    torrent_appeared = True
                    break
            if not torrent_appeared:
                return True
        return False

    # Todo: This guy is blind to duplicates. Should use set()
    def __eq__(self, other):
        if isinstance(other, Torrents):
            if len(self.downloading) is len(other.downloading) \
                    and len(self.completed) is len(other.completed) \
                    and len(self.stopped) is len(other.stopped):

                if self.__find_unmatched_torrents(self.completed, other.completed):
                    return False

                if self.__find_unmatched_torrents(self.downloading, other.downloading):
                    return False

                if self.__find_unmatched_torrents(self.stopped, other.stopped):
                    return False

                return True
        return False


class TorrentDataManager(object):
    """ Connects to the transmission torrent client and gets data on running torrents
    """
    def __init__(self, username, password):
        self.__username = username
        self.__password = password
        self.torrents = {}
        self.__return_code = -1
        self.__bash_command = Definitions.GET_TORRENT_SCRIPT_PATH + ' {0} {1}'.format(username, password)

    def __fetch_torrent_data(self):
        process = subprocess.run(self.__bash_command.split(), stdout=subprocess.PIPE)
        self.__return_code = process.returncode
        if self.__return_code is not 0:
            error_msg = 'Failed to get torrents via CLI, return code was {}. Try running the scripts/get_torrent_data.sh script to check it\'s working'\
                .format(self.__return_code)
            logging.error(error_msg)
            raise ScriptFailureError(error_msg)
        return process.stdout.decode('ascii')

    def __build_torrents_object(self, data):
        rows = [
            [w.strip() for w in l.split(' ') if w]
            for l in data.split('\n') if l
        ]

        torrents_list = [Torrent(row[2], row[0], row[1]) for row in rows]

        self.torrents = Torrents()

        for torrent in torrents_list:
            if torrent.status == 'Downloading':
                self.torrents.downloading.append(torrent)
            elif torrent.percent == '100%':
                self.torrents.completed.append(torrent)
            else:
                self.torrents.stopped.append(torrent)

        return self.torrents

    def get_torrents(self):
        data = self.__fetch_torrent_data()
        return self.__build_torrents_object(data)
