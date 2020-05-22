import logging
from enum import Enum

import yaml

from Definitions import Definitions
from Singleton import Singleton


CONFIG_FILE_HINT = '''

Hint:- If running as a service, the config.yml file should be owned by root with 400 permissions and contain the following \
(with <username> and <password> filled in)
username: <username>
password: <password>

or else if running just as a script, run with:
    python3 main.py <username> <password>
'''


class ConfigKeys(Enum):
    transmission_user = 1
    transmission_password = 2
    default_display_mode = 3
    chilli_display_mode = 4
    enable_api = 5
    flask_hostname = 6
    flask_port = 7


class Configuration(object, metaclass=Singleton):
    def __init__(self):
        try:
            with open(Definitions.CONFIG_FILE_PATH) as f:
                self.__config = yaml.safe_load(f)
        except FileNotFoundError:
            logging.error('Config file, config.yml not found. Stopping.')
            exit(1)
        except yaml.YAMLError as yaml_error:
            logging.error('Error reading the config.yml file. Stopping.' + CONFIG_FILE_HINT)
            logging.debug('Error reading config.yml file: %s', str(yaml_error))
            exit(1)

    def get(self, config_key: ConfigKeys):
        try:
            return self.__config[config_key.name]
        except KeyError:
            logging.warning('Could not find %s property within config.yml', config_key.name)
            return None

