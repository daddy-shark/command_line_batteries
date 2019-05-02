import sys
import requests
import socket

from influxdb import InfluxDBClient, exceptions

from clb import init_logger
from clb.config_parser import config_parser


log = init_logger(__name__, config_parser.get_log_level())
HOSTNAME = socket.gethostname()

try:
    INFLUXDB_CONNECTION_KVARGS = config_parser.CONFIG['influxdb']
    INFLUXDB_MEASUREMENT = config_parser.CONFIG['influxdb_measurement']
except KeyError as e:
    log.error(f'Bad config file: Key {e} not found')
    sys.exit(1)


class InfluxDBClientManager:
    __instance = None

    def __init__(self, connection_kwargs) -> None:
        log.debug(f'Creating client to InfluxDB database: {connection_kwargs.get("host")}:{connection_kwargs.get("port")}')
        try:
            self.influx_client = InfluxDBClient(**connection_kwargs)
        except (exceptions.InfluxDBClientError, requests.exceptions.ConnectionError) as e:
            log.error(f'InfluxDB error: {e}')
            sys.exit(2)

        log.debug(f'Creating {connection_kwargs.get("host")} database: {connection_kwargs.get("database")}')
        try:
            self.influx_client.create_database(connection_kwargs.get('database'))
        except (exceptions.InfluxDBClientError, requests.exceptions.ConnectionError) as e:
            log.error(f'InfluxDB error: {e}')
            sys.exit(3)

    @staticmethod
    def client() -> InfluxDBClient:
        if InfluxDBClientManager.__instance is None:
            InfluxDBClientManager.__instance = InfluxDBClientManager(INFLUXDB_CONNECTION_KVARGS)

        return InfluxDBClientManager.__instance.influx_client


def write_point(json_point: dict) -> None:
    log.info(f'Adding point to InfluxDB: {json_point}')
    try:
        InfluxDBClientManager.client().write_points([json_point])
    except (exceptions.InfluxDBClientError, requests.exceptions.ConnectionError) as e:
        log.error(f"Can't write to InfluxDB {InfluxDBClientManager.client()}: {e}")


def write_status(status_name: str, status_code: int) -> None:
    status_point = {
        'measurement': INFLUXDB_MEASUREMENT,
        'tags': {
            'status': status_name,
            'host': HOSTNAME
        },
        'fields': {
            'value': status_code,
        },
    }

    write_point(status_point)
