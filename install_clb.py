#!/usr/bin/env python

import os
import stat
import logging
import sys
import subprocess
try:
    from urllib import urlretrieve
except ImportError:
    from urllib.request import urlretrieve


INSTALL_PATH = '/opt/command_line_batteries'
LOG_PATH = '/var/log/command_line_batteries'
EXAMPLES = (
    'example_config.yml',
    'example_script.py',
    'example_simple_config.yml',
    'example_simple_script.py',
)


def create_dir(path):
    try:
        os.mkdir(path, 0o755)
    except OSError as error:
        if 'File exists' not in str(error):
            LOG.critical('Can not create dir: {}. {}'.format(path, error))
            sys.exit(1)


def download_file(url, path):
    try:
        urlretrieve(url, path)
    except IOError as error:
        LOG.critical('Can not download file: {} to {}. {}'.format(url, path, error))
        sys.exit(1)


def add_exec_bit(path):
    try:
        st_path = os.stat(path)
        os.chmod(path, st_path.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    except OSError as error:
        LOG.error(error)
        sys.exit(1)


def run_command(command):
    command_env = os.environ.copy()
    command_env['PATH'] = '/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:{}'.format(command_env['PATH'])
    child = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=True,
        executable='bash',
        env=command_env,
    )
    try:
        child.communicate()
        if child.returncode == 0:
            return True

    except subprocess.SubprocessError as error:
        LOG.error(error)
        return False

    return False


def get_logger(name):
    logger = logging.getLogger(name)
    s_h = logging.StreamHandler()
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter('%(asctime)s %(levelname)s in %(name)s: %(message)s')
    s_h.setFormatter(fmt)
    logger.addHandler(s_h)
    return logger


if __name__ == '__main__':
    LOG = get_logger('installation')

    if run_command('which python3') is False or run_command('which pip3') is False:
        LOG.critical('Please install python3 and pip3 first!')
        LOG.info('''
            On Debian/Ubuntu, you can install it with this command:
               $ sudo apt-get install python3-pip
               
            On CentOS 7:
               $ sudo yum install python36-pip
        ''')
        sys.exit(1)

    create_dir(INSTALL_PATH)
    create_dir(LOG_PATH)

    if run_command('python3 -m pip install virtualenv') is False:
        LOG.critical('Can not install module virtualenv!')
        sys.exit(1)

    if run_command('python3 -m venv {}/venv'.format(INSTALL_PATH)) is False:
        LOG.critical('Can not install virtualenv to {}/venv'.format(INSTALL_PATH))
        sys.exit(1)

    if run_command('source {}/venv/bin/activate && pip install clb --upgrade'.format(INSTALL_PATH)) is False:
        LOG.critical('Can not activate venv ({}/venv/bin/activate) or install clb package'.format(INSTALL_PATH))
        sys.exit(1)

    for file in EXAMPLES:
        download_file(
            'https://raw.githubusercontent.com/daddy-shark/command_line_batteries/master/examples/{}'.format(file),
            '{}/{}'.format(INSTALL_PATH, file)
        )
        if '.py' in file:
            add_exec_bit('{}/{}'.format(INSTALL_PATH, file))

    LOG.info('Installation complete')
