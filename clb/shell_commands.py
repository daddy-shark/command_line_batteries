import subprocess
import os
import sys

from clb.logger import init_logger
from clb.config_parser import ConfigManager


LOG = init_logger(__name__)
if 'pytest' not in sys.modules:
    LOG.setLevel(ConfigManager.get_log_level())


def run_shell_command(command: str, timeout: float) -> bool:
    backup_env = os.environ.copy()
    backup_env["PATH"] = str(ConfigManager.get_config_value('shell_commands_env_path')) + backup_env["PATH"]
    LOG.debug(f'Using shell environment: {backup_env}')
    LOG.info(f'Running shell command: {command}')
    child = subprocess.Popen(
        f"{command}; echo ${{PIPESTATUS[@]}} | "
        f"awk '{{sum = 0; for (i = 1; i <= NF; ++i) if ($i > sum) sum = $i}}; END{{exit sum}}'",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=True,
        executable='bash',
        env=backup_env,
    )
    try:
        stdout, stderr = child.communicate(timeout=float(timeout))
    except subprocess.TimeoutExpired:
        LOG.critical(f'Shell command timeout exceeded')
        child.kill()
        return False

    if child.returncode == 0 and stderr is None:
        LOG.info('Shell command success')
        return True

    if stderr:
        stderr = stderr.decode("utf-8")

    if stdout:
        stdout = stdout.decode("utf-8")

    LOG.critical(f'Shell command failed with return code: {child.returncode}, stderr: {stderr}, stdout: {stdout}')
    return False


def run_all_shell_commands() -> bool:
    for item in list(ConfigManager.get_config_value('shell_commands_list')):
        if not run_shell_command(item.get('command'), item.get('timeout_s')):
            return False

    return True
