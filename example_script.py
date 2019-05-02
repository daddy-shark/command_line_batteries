#!/usr/bin/env python3
import sys

from clb import *


log = init_logger(__name__, get_log_level())

if __name__ == '__main__':
    if shell_commands.run_all_shell_commands():
        log.info('Local backup completed successfully')
        influxdb_client.write_status('Local backup completed successfully', 0)
    else:
        log.critical('Local backup failed')
        influxdb_client.write_status('Local backup failed', 1)
        sys.exit(1)

    if aws_s3.upload_all_files():
        log.info('Upload to s3 completed successfully')
        influxdb_client.write_status('Upload to s3 completed successfully', 0)
    else:
        log.error('Upload to s3 failed')
        influxdb_client.write_status('Upload to s3 failed', 1)
        sys.exit(2)

    log.info('Test backup completed successfully')
    influxdb_client.write_status('Test backup completed successfully', 0)
