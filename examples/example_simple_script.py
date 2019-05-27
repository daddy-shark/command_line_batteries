#!/usr/bin/env python3

from clb import *


if shell_commands.run_all_shell_commands():
    LOG.info('Commands completed')
else:
    LOG.critical('Commands failed')
    sys.exit(1)
