import sys
import argparse
from typing import Union
import socket

import yaml

from clb.logger import init_logger


LOG = init_logger(__name__, 'DEBUG')


def get_config_path() -> str:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c', '--config',
        required=True,
        type=argparse.FileType('r'),
        help='path to config file'
    )
    return parser.parse_args().config.name


def get_hostname() -> str:
    return socket.gethostname()


class ConfigManager:
    __instance = None

    def __init__(self, config_path: str) -> None:
        try:
            LOG.info(f'Reading config file: {config_path}')
            with open(config_path, 'r') as yaml_file:
                self.config = yaml.safe_load(yaml_file)
        except (
                FileNotFoundError,
                yaml.YAMLError,
        )as error:
            LOG.critical({error})
            sys.exit(1)

    @staticmethod
    def get_config() -> dict:
        if ConfigManager.__instance is None:
            ConfigManager.__instance = ConfigManager(get_config_path())

        return ConfigManager.__instance.config

    @staticmethod
    def get_log_level() -> str:
        try:
            log_level = ConfigManager.get_config()['log_level']
        except KeyError as error:
            LOG.warning(f'Bad config file: Key {error} not found. Setting log level to DEBUG')
            log_level = 'DEBUG'

        return log_level

    @staticmethod
    def get_config_value(key: str) -> Union[list, str, dict]:
        try:
            return ConfigManager.get_config()[key]
        except (KeyError, TypeError) as error:
            LOG.error(f'Bad config file: Key {error} not found')
            sys.exit(1)
