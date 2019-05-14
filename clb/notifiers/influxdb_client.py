import sys

from influxdb import InfluxDBClient, exceptions
import requests

from clb.config_parser import get_hostname, ConfigManager
from clb.logger import init_logger


LOG = init_logger(__name__)
if 'pytest' not in sys.modules:
    LOG.setLevel(ConfigManager.get_log_level())


class InfluxDBClientManager:
    __instance = None

    def __init__(self, connection_kwargs) -> None:
        LOG.debug(f'Creating client to InfluxDB database: '
                  f'{connection_kwargs.get("host")}:{connection_kwargs.get("port")}')
        try:
            self.influx_client = InfluxDBClient(**connection_kwargs)
        except (exceptions.InfluxDBClientError, requests.exceptions.ConnectionError) as error:
            LOG.error(f'InfluxDB error: {error}')
            sys.exit(2)

        LOG.debug(f'Creating {connection_kwargs.get("host")} database: {connection_kwargs.get("database")}')
        try:
            self.influx_client.create_database(connection_kwargs.get('database'))
        except (exceptions.InfluxDBClientError, requests.exceptions.ConnectionError) as error:
            LOG.error(f'InfluxDB error: {error}')
            sys.exit(3)

    @staticmethod
    def client() -> InfluxDBClient:
        if InfluxDBClientManager.__instance is None:
            InfluxDBClientManager.__instance = InfluxDBClientManager(ConfigManager.get_config_value('influxdb'))

        return InfluxDBClientManager.__instance.influx_client


def write_point(json_point: dict) -> None:
    LOG.info(f'Adding point to InfluxDB: {json_point}')
    try:
        InfluxDBClientManager.client().write_points([json_point])
    except (exceptions.InfluxDBClientError, requests.exceptions.ConnectionError) as error:
        LOG.error(f"Can't write to InfluxDB {InfluxDBClientManager.client()}: {error}")


def write_status(status_name: str, status_code: int) -> None:
    status_point = {
        'measurement': ConfigManager.get_config_value('influxdb_measurement'),
        'tags': {
            'status': status_name,
            'host': get_hostname()
        },
        'fields': {
            'value': status_code,
        },
    }

    write_point(status_point)
