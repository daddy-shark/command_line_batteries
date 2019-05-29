from typing import Union
import logging

from influxdb import InfluxDBClient, exceptions
import requests

from clb.config_parser import get_hostname, ConfigManager


LOG = logging.getLogger(__name__)


class InfluxDBClientManager:
    __instance = None

    def __init__(self, connection_kwargs) -> None:
        LOG.debug(f'Creating client to InfluxDB database: '
                  f'{connection_kwargs.get("host")}:{connection_kwargs.get("port")}')
        try:
            self.influx_client = InfluxDBClient(**connection_kwargs)
        except TypeError as error:
            LOG.error(f"Can't create InfluxDB client: {error}")
            self.influx_client = None
            return

        LOG.debug(f'Creating {connection_kwargs.get("host")} database: {connection_kwargs.get("database")}')
        try:
            self.influx_client.create_database(connection_kwargs.get('database'))
        except (exceptions.InfluxDBClientError, requests.exceptions.ConnectionError) as error:
            LOG.error(f"Can't create InfluxDB database: {error}")
            self.influx_client = None

    @staticmethod
    def client() -> Union[InfluxDBClient, None]:
        if InfluxDBClientManager.__instance is None or InfluxDBClientManager.__instance.influx_client is None:
            InfluxDBClientManager.__instance = InfluxDBClientManager(ConfigManager.get_config_value('influxdb'))

        return InfluxDBClientManager.__instance.influx_client

    @staticmethod
    def write_point(json_point: dict) -> None:
        LOG.info(f'Adding point to InfluxDB: {json_point}')
        client = InfluxDBClientManager.client()
        if client is None:
            return

        try:
            client.write_points([json_point])
        except (exceptions.InfluxDBClientError, requests.exceptions.ConnectionError) as error:
            LOG.error(f"Can't write to InfluxDB {InfluxDBClientManager.client()}: {error}")
        except AttributeError as error:
            LOG.error(f"Can't write to InfluxDB: {error}")


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

    InfluxDBClientManager.write_point(status_point)
