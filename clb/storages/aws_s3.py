import os
import datetime
import sys

import boto3
import botocore

from clb.logger import init_logger
from clb.config_parser import get_hostname, ConfigManager


LOG = init_logger(__name__)
if 'pytest' not in sys.modules:
    LOG.setLevel(ConfigManager.get_log_level())


def upload_file(file_path: str) -> bool:
    file_name = f'{str(datetime.date.today())}-{os.path.basename(file_path)}'
    short_hostname = get_hostname().split(".")[0]
    LOG.info(f'Upload {file_path} to s3/{ConfigManager.get_config_value("aws_bucket")}/{short_hostname}/{file_name}')
    try:
        aws_s3 = boto3.client(
            's3',
            aws_access_key_id=ConfigManager.get_config_value('aws_access_key_id'),
            aws_secret_access_key=ConfigManager.get_config_value('aws_secret_access_key'),
        )
        aws_s3.upload_file(file_path, ConfigManager.get_config_value('aws_bucket'), f'{short_hostname}/{file_name}')
    except boto3.exceptions.S3UploadFailedError as error:
        LOG.error(error)
        return False

    if update_bucket_lifecycle_rules():
        return True

    return False


def update_bucket_lifecycle_rules() -> bool:
    LOG.info(f'Update bucket {ConfigManager.get_config_value("aws_bucket")} lifecycle rules')
    try:
        aws_s3 = boto3.resource(
            's3',
            aws_access_key_id=ConfigManager.get_config_value('aws_access_key_id'),
            aws_secret_access_key=ConfigManager.get_config_value('aws_secret_access_key'),
        )
        bucket_lifecycle_configuration = aws_s3.BucketLifecycleConfiguration(
            ConfigManager.get_config_value('aws_bucket')
        )
        lifecycle_rules = bucket_lifecycle_configuration.rules

        backup_lifecycle_rule = {
            'Expiration': {'Days': ConfigManager.get_config_value('aws_expire_after_days')},
            'ID': f'{get_hostname().split(".")[0]} cleanup',
            'Filter': {'Prefix': f'{get_hostname().split(".")[0]}/'},
            'Status': 'Enabled',
            'NoncurrentVersionExpiration': {'NoncurrentDays': ConfigManager.get_config_value('aws_expire_after_days')}
        }

        if backup_lifecycle_rule not in lifecycle_rules:
            lifecycle_rules.append(backup_lifecycle_rule)

        response = bucket_lifecycle_configuration.put(
            LifecycleConfiguration={
                'Rules': lifecycle_rules
            }
        )
        LOG.debug(f'AWS response HTTP status code: {response["ResponseMetadata"]["HTTPStatusCode"]}')

    except botocore.exceptions.BotoCoreError as error:
        LOG.error(error)
        return False

    return True


def upload_all_files() -> bool:
    for file in ConfigManager.get_config_value('aws_files_list'):
        if not upload_file(file):
            return False

    return True
