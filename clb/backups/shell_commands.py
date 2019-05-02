import subprocess
import os
import sys

from clb import init_logger
from clb.config_parser import config_parser


log = init_logger(__name__, config_parser.get_log_level())

try:
    SHELL_COMMANDS_LIST = config_parser.CONFIG['shell_commands_list']
    SHELL_COMMANDS_ENV_PATH = config_parser.CONFIG['shell_commands_env_path']
except KeyError as e:
    log.error(f'Bad config file: Key {e} not found')
    sys.exit(1)


def run_shell_command(command: str, timeout: float) -> bool:
    backup_env = os.environ.copy()
    backup_env["PATH"] = SHELL_COMMANDS_ENV_PATH + backup_env["PATH"]
    log.debug(f'Using shell environment: {backup_env}')
    log.info(f'Running shell command: {command}')
    child = subprocess.Popen(
        f"{command}; echo ${{PIPESTATUS[@]}} | awk '{{sum = 0; for (i = 1; i <= NF; ++i) if ($i > sum) sum = $i}}; END{{exit sum}}'",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=True,
        executable='bash',
        env=backup_env,
    )
    try:
        stdout, stderr = child.communicate(timeout=float(timeout))
    except subprocess.TimeoutExpired:
        log.critical(f'Shell command timeout exceeded')
        child.kill()
        return False

    if child.returncode == 0 and stderr is None:
        log.info('Shell command success')
        return True

    if stderr:
        stderr = stderr.decode("utf-8")

    if stdout:
        stdout = stdout.decode("utf-8")

    log.critical(f'Shell command failed with return code: {child.returncode}, stderr: {stderr}, stdout: {stdout}')
    return False


def run_all_shell_commands() -> bool:
    for item in SHELL_COMMANDS_LIST:
        if not run_shell_command(item.get('command'), item.get('timeout_s')):
            return False

    return True
