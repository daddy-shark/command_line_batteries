import sys
import argparse
from typing import Union
import socket

import yaml

from clb.logger import init_logger


LOG = init_logger(__name__, 'DEBUG')

PARSER = argparse.ArgumentParser()
PARSER.add_argument(
    '-c', '--config',
    required=True,
    type=argparse.FileType('r'),
    help='path to config file'
)
ARGS = PARSER.parse_args()

try:
    LOG.info(f'Reading config file: {ARGS.config.name}')
    with open(ARGS.config.name, 'r') as yaml_file:
        CONFIG = yaml.safe_load(yaml_file)
except (
        FileNotFoundError,
        yaml.YAMLError,
)as error:
    LOG.critical({error})
    sys.exit(1)


def get_log_level() -> str:
    try:
        log_level = CONFIG['log_level']
    except KeyError as error:
        LOG.warning(f'Bad config file: Key {error} not found. Setting log level to DEBUG')
        log_level = 'DEBUG'

    return log_level


def get_config_value(key: str) -> Union[list, str, dict]:
    try:
        return CONFIG[key]
    except KeyError as error:
        LOG.error(f'Bad config file: Key {error} not found')
        sys.exit(1)


def get_hostname() -> str:
    return socket.gethostname()
