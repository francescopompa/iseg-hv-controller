"""
SEE README.md
"""
import logging
import time
import json
import difflib
import ICS_Client
from config import ProgramConfig
from ICS_Info import print_some_info


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

    ics_bridge = ICS_Client.IcsClient(
        connection_name="ics_connection" + time.asctime(),
        connection_parameters=f"ws://{config.config.Server.ip}:{config.config.Server.port}",
        connection_login=config.config.Server.username,
        connection_password=config.config.Server.password,
    )

    ics_bridge.connect()
    print_some_info(ics_bridge)
    # test_channel = all_channels[0]
    # test_channel.setControlCurrentSet(1)
    # test_channel.setControlVoltageSet(200)
    # test_channel.setControlOn(1)


if __name__ == "__main__":
    # TODO make it so starting from shell without commands uses the values defined by config and with some commands sends those
    # TODO add argparse (see sphe_processor scripts project)
    # TODO gitlab
    # TODO cmd on off !!
    main()
