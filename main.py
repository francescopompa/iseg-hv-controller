"""
SEE README.md
"""
import logging
import time

from ICS_Info import print_some_info
from config import ProgramConfig
from client import IcsClient
from commander import Commander


def main():
    """
    ...
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s::%(levelname)s::%(filename)s:%(funcName)s:%(lineno)d::\t%(message)s",
        handlers=[logging.StreamHandler(), logging.FileHandler("hv_controller.log")],
    )
    logging.info("Started")

    config = ProgramConfig()

    ics_client = IcsClient(
        connection_name="ics_connection" + time.asctime(),
        connection_parameters=f"ws://{config.config.Server.ip}:{config.config.Server.port}",
        connection_login=config.config.Server.username,
        connection_password=config.config.Server.password,
    )

    ics_client.connect()
    print_some_info(ics_client)
    commander = Commander(ics_client, config)
    commander.modify_channel("0.0.0")


if __name__ == "__main__":
    # TODO make it so starting from shell without commands uses the values defined by config and with some commands sends those
    # TODO add argparse (see rad commander project)
    # TODO gitlab
    # TODO cmd on off !!
    main()
