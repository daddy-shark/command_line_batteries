# Command line batteries (clb)
Plugin-driven Python program to improve the functionality of Bash commands without writing a too difficult Bash code.

Bash is good for backup pipelines like `mysqldump [options] | pigz [options] > mysqldump.gz` but there is no easy way to collect exit codes for every command in the pipeline, take care about commands environment, check for timeout, notify monitoring system, write awesome logs, upload backups to AWS S3 and so on. With Backup_tools you have all of this stuff out of the box. Just fill the YAML config file and change the Python script file for your needs.

## Features:
- Timeout for every shell command
- Check for exit code of every shell command, inclusive all commands in the pipeline
- PATH environment var for shell commands
- Informative logs
- Monitoring via influxdb metrics
- AWS S3 upload with expiration policy

## Usage
[example_script.py](example_script.py) -c [example_config.yml](example_config.yml)
Usage example:
```
example_script.py -c example_config.yml
2019-05-02 03:31:28,363 - INFO - clb.config_parser.config_parser - Reading config file: example_config.yml
2019-05-02 03:31:28,607 - INFO - clb.backups.shell_commands - Running shell command: mkdir -p /tmp/backups
2019-05-02 03:31:28,618 - INFO - clb.backups.shell_commands - Shell command success
2019-05-02 03:31:28,619 - INFO - clb.backups.shell_commands - Running shell command: echo 'THE BACKUP BASH COMMAND' | pigz -p 4 -4 > /tmp/backups/current_backup.gz
2019-05-02 03:31:28,634 - INFO - clb.backups.shell_commands - Shell command success
2019-05-02 03:31:28,634 - INFO - __main__ - Local backup completed successfully
2019-05-02 03:31:28,635 - INFO - clb.notifiers.influxdb_client - Adding point to InfluxDB: {'measurement': 'backups', 'tags': {'status': 'Local backup completed successfully', 'host': 'YOUR_HOST'}, 'fields': {'value': 0}}
2019-05-02 03:31:28,665 - INFO - clb.storages.aws_s3 - Upload /tmp/backups/current_backup.gz to s3/YOUR_HOST/2019-05-02-current_backup.gz
2019-05-02 03:31:29,542 - INFO - clb.storages.aws_s3 - Update bucket disaster-backups lifecycle rules
2019-05-02 03:31:30,511 - INFO - __main__ - Upload to s3 completed successfully
2019-05-02 03:31:30,511 - INFO - clb.notifiers.influxdb_client - Adding point to InfluxDB: {'measurement': 'backups', 'tags': {'status': 'Upload to s3 completed successfully', 'host': 'YOUR_HOST'}, 'fields': {'value': 0}}
2019-05-02 03:31:30,518 - INFO - __main__ - Test backup completed successfully
2019-05-02 03:31:30,519 - INFO - clb.notifiers.influxdb_client - Adding point to InfluxDB: {'measurement': 'backups', 'tags': {'status': 'Test backup completed successfully', 'host': 'YOUR_HOST'}, 'fields': {'value': 0}}
```

## Installation
The simplest way:
```
mkdir -p /opt/command_line_batteries
python3 -m pip install clb
wget -O /opt/command_line_batteries/example_script.py https://raw.githubusercontent.com/sharkman-devops/command_line_batteries/master/example_script.py
wget -O /opt/command_line_batteries/example_config.yml https://raw.githubusercontent.com/sharkman-devops/command_line_batteries/master/example_config.yml
```

The virtual environment way:
```
mkdir -p /opt/command_line_batteries
python3 -m venv /opt/command_line_batteries/venv
source /opt/command_line_batteries/venv/bin/python
pip install command_line_batteries
wget -O /opt/command_line_batteries/example_script.py https://raw.githubusercontent.com/sharkman-devops/command_line_batteries/master/example_script.py
wget -O /opt/command_line_batteries/example_config.yml https://raw.githubusercontent.com/sharkman-devops/command_line_batteries/master/example_config.yml
```

## Compatibility
Command line batteries tested on Linux with BASH shell and Python 3.6 & 3.7