import sys

from clb.storages import aws_s3
from clb.notifiers import influxdb_client
from clb.config_parser import ConfigManager
from clb.logger import init_logger


LOG = init_logger(__name__, 'DEBUG')
if 'pytest' not in sys.modules:
    LOG.setLevel(ConfigManager.get_log_level())

__all__ = [
    'sys',
    'shell_commands',
    'aws_s3',
    'influxdb_client',
    'LOG',
]
