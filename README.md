# Command line batteries (clb)
Plugin-driven Python program to improve the functionality of Bash commands without writing a too difficult Bash code.

[![PyPI version](https://badge.fury.io/py/clb.svg)](https://badge.fury.io/py/clb)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/clb.svg)

Bash is good for backup pipelines like `mysqldump [options] | pigz [options] > mysqldump.gz` but there is no easy way to collect exit codes for every command in the pipeline, take care about commands environment, check for timeout, notify monitoring system, write awesome logs, upload backups to AWS S3 and so on. With Command line batteries you have all of this stuff out of the box. Just fill the YAML config file and change the Python script file for your needs. These files are designed to be as simple as possible.

## Features:
- Timeout for every shell command
- Check for exit code of every shell command, inclusive all commands in the pipeline
- PATH environment var for shell commands
- Informative logs
- Monitoring via influxdb metrics
- AWS S3 upload with expiration policy

## Usage
#### Basic usage example:
[example_simple_script.py](examples/example_simple_script.py) -c [example_simple_config.yml](examples/example_simple_config.yml)
```
2019-05-06 13:38:29,930 INFO in clb.config_parser: Reading config file: example_simple_config.yml
2019-05-06 13:38:29,933 INFO in clb.shell_commands: Running shell command: mkdir -p /tmp/backups
2019-05-06 13:38:29,943 INFO in clb.shell_commands: Shell command success
2019-05-06 13:38:29,944 INFO in clb.shell_commands: Running shell command: echo 'THE BACKUP BASH COMMAND' | pigz -p 4 -4 > /tmp/backups/current_backup.gz
2019-05-06 13:38:29,963 INFO in clb.shell_commands: Shell command success
2019-05-06 13:38:29,964 INFO in clb: Commands completed
```

#### Advanced usage example:
[example_script.py](examples/example_script.py) -c [example_config.yml](examples/example_config.yml)
``` 
2019-05-06 13:05:06,962 INFO in clb.config_parser: Reading config file: /opt/command_line_batteries/example_config.yml
2019-05-06 13:05:07,176 INFO in clb.shell_commands: Running shell command: mkdir -p /tmp/backups
2019-05-06 13:05:07,182 INFO in clb.shell_commands: Shell command success
2019-05-06 13:05:07,183 INFO in clb.shell_commands: Running shell command: echo 'THE BACKUP BASH COMMAND' | pigz -p 4 -4 > /tmp/backups/current_backup.gz
2019-05-06 13:05:07,189 INFO in clb.shell_commands: Shell command success
2019-05-06 13:05:07,190 INFO in clb: Backup files created successfully
2019-05-06 13:05:07,190 INFO in clb.notifiers.influxdb_client: Adding point to InfluxDB: {'measurement': 'backups', 'tags': {'status': 'Backup files created', 'host': 'EXAMPLE.HOST'}, 'fields': {'value': 0}}
2019-05-06 13:05:07,199 INFO in clb.storages.aws_s3: Upload /tmp/backups/current_backup.gz to s3/EXAMPLE.HOST/2019-05-06-current_backup.gz
2019-05-06 13:05:07,514 INFO in clb.storages.aws_s3: Update bucket YOUR_AWS_BUCKET_FOR_BACKUPS lifecycle rules
2019-05-06 13:05:08,131 INFO in clb: Upload to s3 completed successfully
2019-05-06 13:05:08,131 INFO in clb.notifiers.influxdb_client: Adding point to InfluxDB: {'measurement': 'backups', 'tags': {'status': 'Upload to s3 completed', 'host': 'EXAMPLE.HOST'}, 'fields': {'value': 0}}
2019-05-06 13:05:08,135 INFO in clb: Backup completed successfully
2019-05-06 13:05:08,135 INFO in clb.notifiers.influxdb_client: Adding point to InfluxDB: {'measurement': 'backups', 'tags': {'status': 'Backup completed', 'host': 'EXAMPLE.HOST'}, 'fields': {'value': 0}}
```
#### Grafana visualisation example:

[hosted_snapshot](https://snapshot.raintank.io/dashboard/snapshot/Dw3pSX5NL3yXlZPXMv37872R12mEsTQg)

[exported_json](grafana/backups_dashboard_example.json)

## Installation
#### The simplest way:
Download and run installation script (python2/3):
```
$ wget -O /tmp/install_clb.py https://raw.githubusercontent.com/sharkman-devops/command_line_batteries/master/install_clb.py
$ sudo python /tmp/install_clb.py
```

Create a cron job(crontab -e):
```
51 23 * * * /opt/command_line_batteries/venv/bin/python /opt/command_line_batteries/example_script.py -c /opt/command_line_batteries/example_config.yml >> /var/log/command_line_batteries/example.log 2>&1
```
Don't forget to fill the example_config.yml and check the example_script.py for logic you want!

#### More flexible way:
Create an install directory:
```
mkdir -p /opt/command_line_batteries
```

Create a virtual environment:
```
python3 -m venv /opt/command_line_batteries/venv
```

Activate a virtual environment:
```
source /opt/command_line_batteries/venv/bin/activate
```

Install the command line batteries:
```
pip install clb --upgrade
```

Download example script and config:
```
wget -O /opt/command_line_batteries/example_script.py https://raw.githubusercontent.com/sharkman-devops/command_line_batteries/master/example_script.py
wget -O /opt/command_line_batteries/example_config.yml https://raw.githubusercontent.com/sharkman-devops/command_line_batteries/master/example_config.yml
```

Make the example script executable:
```
chmod +x /opt/command_line_batteries/example_script.py
```

Create a logs directory:
```
mkdir -p /var/log/command_line_batteries
```

Create a cron job (crontab -e):
```
51 23 * * * /opt/command_line_batteries/venv/bin/python /opt/command_line_batteries/example_script.py -c /opt/command_line_batteries/example_config.yml >> /var/log/command_line_batteries/example.log 2>&1
```
Don't forget to fill the example_config.yml and check the example_script.py for logic you want!


## Compatibility
Environment should include:
- BASH Shell
- Awk
- Python 3.6 or 3.7

Command line batteries tested on GNU Linux with GNU bash 4, GNU Awk 4 and Python 3.6 & 3.7
