import logging

import slack
from slack import errors

from clb.config_parser import ConfigManager


LOG = logging.getLogger(__name__)


def send_message(message: str) -> None:
    slack_client = slack.WebClient(token=ConfigManager.get_config_value('slack_token'))
    slack_channel = ConfigManager.get_config_value('slack_channel')
    LOG.info(f'Sending message "{message}" to channel: {slack_channel}')
    try:
        response = slack_client.chat_postMessage(
            channel=slack_channel,
            text=message,
            username='CLB',
            icon_url='https://github.com/sharkman-devops/command_line_batteries/raw/master/icon/term.png',
        )
        if response.get('ok') and response.get('message') == message:
            LOG.info('Message sent successfully!')

    except errors.SlackApiError as error:
        LOG.error(error)
        LOG.error('Failed to send message!')
