import os
import sys
import socket
import datetime

import boto3
import botocore

from clb import init_logger
from clb.config_parser import config_parser


log = init_logger(__name__, config_parser.get_log_level())
HOSTNAME = socket.gethostname()

try:
    AWS_ACCESS_KEY_ID = config_parser.CONFIG['aws_access_key_id']
    AWS_SECRET_ACCESS_KEY = config_parser.CONFIG['aws_secret_access_key']
    AWS_BUCKET_NAME = config_parser.CONFIG['aws_bucket']
    AWS_EXPIRE_AFTER_DAYS = config_parser.CONFIG['aws_expire_after_days']
    AWS_FILES_LIST = config_parser.CONFIG['aws_files_list']
except KeyError as e:
    log.error(f'Bad config file: Key {e} not found')
    sys.exit(1)


def upload_file(file_path):
    file_name = f'{str(datetime.date.today())}-{os.path.basename(file_path)}'
    short_hostname = HOSTNAME.split(".")[0]
    log.info(f'Upload {file_path} to s3/{short_hostname}/{file_name}')
    try:
        s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        s3.upload_file(file_path, AWS_BUCKET_NAME, f'{short_hostname}/{file_name}')
    except boto3.exceptions.S3UploadFailedError as e:
        log.error(e)
        return False

    if update_bucket_lifecycle_rules():
        return True


def update_bucket_lifecycle_rules():
    log.info(f'Update bucket {AWS_BUCKET_NAME} lifecycle rules')
    try:
        s3 = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        bucket_lifecycle_configuration = s3.BucketLifecycleConfiguration(AWS_BUCKET_NAME)
        lifecycle_rules = bucket_lifecycle_configuration.rules

        backup_lifecycle_rule = {
            'Expiration': {'Days': AWS_EXPIRE_AFTER_DAYS},
            'ID': f'{HOSTNAME.split(".")[0]} cleanup',
            'Filter': {'Prefix': f'{HOSTNAME.split(".")[0]}/'},
            'Status': 'Enabled',
            'NoncurrentVersionExpiration': {'NoncurrentDays': AWS_EXPIRE_AFTER_DAYS}
        }

        if backup_lifecycle_rule not in lifecycle_rules:
            lifecycle_rules.append(backup_lifecycle_rule)

        response = bucket_lifecycle_configuration.put(
            LifecycleConfiguration={
                'Rules': lifecycle_rules
            }
        )
        log.debug(f'AWS response HTTP status code: {response["ResponseMetadata"]["HTTPStatusCode"]}')

    except botocore.exceptions.BotoCoreError as e:
        log.error(e)
        return False

    return True


def upload_all_files() -> bool:
    for file in AWS_FILES_LIST:
        if not upload_file(file):
            return False

    return True
