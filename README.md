# Command line batteries (clb)
Plugin-driven Python program to improve the functionality of Bash commands without writing a too difficult Bash code.

Bash is good for backup pipelines like `mysqldump [options] | pigz [options] > mysqldump.gz` but there is no easy way to collect exit codes for every command in the pipeline, take care about commands environment, check for timeout, notify monitoring system, write awesome logs, upload backups to AWS S3 and so on. With Command line batteries you have all of this stuff out of the box. Just fill the YAML config file and change the Python script file for your needs.

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
2019-05-06 13:05:06,962 INFO in clb.config_parser: Reading config file: /opt/command_line_batteries/example_config.yml
2019-05-06 13:05:07,176 INFO in clb.shell_commands: Running shell command: mkdir -p /tmp/backups
2019-05-06 13:05:07,182 INFO in clb.shell_commands: Shell command success
2019-05-06 13:05:07,183 INFO in clb.shell_commands: Running shell command: echo 'THE BACKUP BASH COMMAND' | pigz -p 4 -4 > /tmp/backups/current_backup.gz
2019-05-06 13:05:07,189 INFO in clb.shell_commands: Shell command success
2019-05-06 13:05:07,190 INFO in __main__: Backup files created successfully
2019-05-06 13:05:07,190 INFO in clb.notifiers.influxdb_client: Adding point to InfluxDB: {'measurement': 'backups', 'tags': {'status': 'Backup files created', 'host': 'EXAMPLE.HOST'}, 'fields': {'value': 0}}
2019-05-06 13:05:07,199 INFO in clb.storages.aws_s3: Upload /tmp/backups/current_backup.gz to s3/EXAMPLE.HOST/2019-05-06-current_backup.gz
2019-05-06 13:05:07,514 INFO in clb.storages.aws_s3: Update bucket YOUR_AWS_BUCKET_FOR_BACKUPS lifecycle rules
2019-05-06 13:05:08,131 INFO in __main__: Upload to s3 completed successfully
2019-05-06 13:05:08,131 INFO in clb.notifiers.influxdb_client: Adding point to InfluxDB: {'measurement': 'backups', 'tags': {'status': 'Upload to s3 completed', 'host': 'EXAMPLE.HOST'}, 'fields': {'value': 0}}
2019-05-06 13:05:08,135 INFO in __main__: Backup completed successfully
2019-05-06 13:05:08,135 INFO in clb.notifiers.influxdb_client: Adding point to InfluxDB: {'measurement': 'backups', 'tags': {'status': 'Backup completed', 'host': 'EXAMPLE.HOST'}, 'fields': {'value': 0}}
```
Grafana visualisation example:

[hosted_snapshot](https://snapshot.raintank.io/dashboard/snapshot/Dw3pSX5NL3yXlZPXMv37872R12mEsTQg)

[exported_json](grafana/backups_dashboard_example.json)

## Installation
#### The simplest way:
Create install directory:
```
mkdir -p /opt/command_line_batteries
```

Install command line batteries:
```
python3 -m pip install clb
```

Download example script and config:
```
wget -O /opt/command_line_batteries/example_script.py https://raw.githubusercontent.com/sharkman-devops/command_line_batteries/master/example_script.py
wget -O /opt/command_line_batteries/example_config.yml https://raw.githubusercontent.com/sharkman-devops/command_line_batteries/master/example_config.yml
```

Make example script executable:
```
chmod +x /opt/command_line_batteries/example_script.py
```

Create logs directory:
```
mkdir -p /var/log/command_line_batteries
```

Create cron job(crontab -e):
```
51 23 * * * /opt/command_line_batteries/example_script.py -c /opt/command_line_batteries/example_config.yml >> /var/log/command_line_batteries/example.log 2>&1
```
Don't forget to fill the example_config.yml and check the example_script.py for logic that your want!

#### The virtual environment way:
Create install directory:
```
mkdir -p /opt/command_line_batteries
```

Create virtual environment:
```
python3 -m venv /opt/command_line_batteries/venv
```

Activate virtual environment:
```
source /opt/command_line_batteries/venv/bin/activate
```

Install command line batteries:
```
pip install clb
```

Download example script and config:
```
wget -O /opt/command_line_batteries/example_script.py https://raw.githubusercontent.com/sharkman-devops/command_line_batteries/master/example_script.py
wget -O /opt/command_line_batteries/example_config.yml https://raw.githubusercontent.com/sharkman-devops/command_line_batteries/master/example_config.yml
```

Make example script executable:
```
chmod +x /opt/command_line_batteries/example_script.py
```

Create logs directory:
```
mkdir -p /var/log/command_line_batteries
```

Create cron job (crontab -e):
```
51 23 * * * /opt/command_line_batteries/venv/bin/python /opt/command_line_batteries/example_script.py -c /opt/command_line_batteries/example_config.yml >> /var/log/command_line_batteries/example.log 2>&1
```
Don't forget to fill the example_config.yml and check the example_script.py for logic that your want!


## Compatibility
Command line batteries tested on Linux with BASH shell and Python 3.6 & 3.7
