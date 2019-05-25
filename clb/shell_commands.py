import subprocess
import os
import logging

from clb.config_parser import ConfigManager


LOG = logging.getLogger(__name__)


def run_shell_command(command: str, timeout: float = None) -> bool:
    command_env = os.environ.copy()
    config_path = str(ConfigManager.get_config_value("shell_commands_env_path")).strip(':')
    command_env["PATH"] = f'{config_path}:{command_env["PATH"]}'
    LOG.debug(f'Using shell environment: {command_env}')
    LOG.info(f'Running shell command: {command}')
    child = subprocess.Popen(
        f"{command}; echo ${{PIPESTATUS[@]}} | "
        f"awk '{{sum = 0; for (i = 1; i <= NF; ++i) if ($i > sum) sum = $i}}; END{{exit sum}}'",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=True,
        executable='bash',
        env=command_env,
    )
    try:
        if timeout:
            stdout, stderr = child.communicate(timeout=float(timeout))
        else:
            stdout, stderr = child.communicate()
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
