"""
SEE README.md
"""
import logging
import time

from ics_info import print_basic_info
from configurator import ProgramConfig
from isc_client import IcsClient
from commander import Commander
import argparse


def main():
    ...


if __name__ == "__main__":
    """
    TODO make it so starting from shell without commands uses the values defined by config and with some commands sends those
    TODO add argparse (see rad commander project)
    TODO cmd on off !
    """
    main()

    parser = argparse.ArgumentParser(
        prog="iseg HV Controller",
        description="CLI to apply configs and commands to the iseg High Voltage Crate",
    )

    parser.add_argument(
        "-f",
        "--filename",
        help="The file name to the toml config."
        "See the default config for options or look at the configurator class",
        default="parameter_config_v1.toml",  # TODO rename
    )
    parser.add_argument(
        "-c",
        "--command",
        help="sends a command to the server in the default or the supplied config"
        "multiple cmd instances allowed (eg.: -c ch1 on -c ch2 off)"
        "for syntax help see the interactive mode or the interpreter class",
        action="append",
    )
    parser.add_argument(
        "-i",
        "--interactive",
        help="starts the interactive mode"
        "for help type help or see the interpreter class",
        action="store_true",
    )
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s::%(levelname)s::%(filename)s:%(funcName)s:%(lineno)d::\t%(message)s",
        handlers=[logging.StreamHandler(), logging.FileHandler("hv_controller.log")],
    )
    logging.info("Started")

    config = ProgramConfig()

    ics_client = IcsClient(
        connection_name="ics_connection" + time.asctime(),
        connection_parameters=f"ws://{config.server.ip}:{config.server.port}",
        connection_login=config.server.username,
        connection_password=config.server.password,
    )

    ics_client.connect()

    print_basic_info(ics_client)

    commander = Commander(ics_client, config)

    # commander.modify_channel("0.0.0")
    commander.apply_channels_config()
