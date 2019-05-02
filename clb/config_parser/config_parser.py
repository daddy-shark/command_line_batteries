import sys
import argparse

import yaml

from clb import init_logger


log = init_logger(__name__, 'DEBUG')

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--config', required=True, type=argparse.FileType('r'), help='path to config file')
args = parser.parse_args()

try:
    log.info(f'Reading config file: {args.config.name}')
    with open(args.config.name, 'r') as yaml_file:
        CONFIG = yaml.safe_load(yaml_file)
except (
        FileNotFoundError,
        yaml.YAMLError,
)as e:
    log.critical({e})
    sys.exit(1)


def get_log_level() -> str:
    try:
        log_level = CONFIG['log_level']
    except KeyError as e:
        log.warning(f'Bad config file: Key {e} not found. Setting log level to DEBUG')
        log_level = 'DEBUG'

    return log_level
