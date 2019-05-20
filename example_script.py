#!/usr/bin/env python3

from clb import *


if __name__ == '__main__':
    if shell_commands.run_all_shell_commands():
        LOG.info('Backup files created successfully')
        influxdb_client.write_status('Backup files created', 0)
    else:
        LOG.critical('Failed to create backup files')
        influxdb_client.write_status('Backup files created', 1)
        sys.exit(1)

    if aws_s3.upload_all_files():
        LOG.info('Upload to s3 completed successfully')
        influxdb_client.write_status('Upload to s3 completed', 0)
    else:
        LOG.error('Upload to s3 failed')
        influxdb_client.write_status('Upload to s3 completed', 1)
        sys.exit(2)

    LOG.info('Backup completed successfully')
    influxdb_client.write_status('Backup completed', 0)
