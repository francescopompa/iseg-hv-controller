"""
SEE README.md
"""
import logging
from isegcontroller.commander import Commander
from isegcontroller.interpreter import Interpreter
import argparse
from pathlib import Path


def create_interpreter(file_name: Path) -> Interpreter:
    """
    creates and returns the cmdline interpreter.
    cmds can the be given with interpreter.onecmd('cmd_string') like from the cli
    :param file_name: Path
    :return: interpreter: isegcontroller.interpreter.Interpreter
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s::%(filename)s:\t%(message)s",
        handlers=[logging.StreamHandler(), logging.FileHandler("hv_controller.log")],
    )
    logging.info("Started")

    commander = Commander(file_name)
    interpreter = Interpreter(commander)
    commander.apply_channels_config()
    return interpreter


def main():
    parser = argparse.ArgumentParser(
        prog="iseg HV Controller",
        description="CLI to apply configs and send commands to the iseg High Voltage Crate",
    )

    rel_path = Path(__file__).parent.parent.absolute()
    parser.add_argument(
        "-f",
        "--filename",
        help="The file name to the toml config.See the default config for options or look at the configurator class",
        default=f"{rel_path}/iseg_libs/default_config.toml",
    )
    parser.add_argument(
        "-c",
        "--command",
        help=(
            "sends a command to the server in the default or the supplied config"
            "multiple cmd instances allowed (eg.: -c ch 1 on -c ch 2 off -c ch5 v 100)"
            "for syntax help see the interactive mode or the interpreter class"
        ),
        nargs="*",
        action="append",
    )
    parser.add_argument(
        "-i",
        "--interactive",
        help="starts the interactive modefor help type help or see the interpreter class",
        action="store_true",
    )
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s::%(filename)s:\t%(message)s",
        handlers=[logging.StreamHandler(), logging.FileHandler("hv_controller.log")],
    )
    logging.info("Started")

    args = parser.parse_args()

    commander = Commander(args.filename)
    interpreter = Interpreter(commander)
    commander.apply_channels_config()

    if args.command:
        for sep_cmd in args.command:
            "-c 'sep_cmd_as_list' - c  'other_cmd_as_list' for example"
            joined_cmd = " ".join(sep_cmd)
            interpreter.onecmd(joined_cmd)
    if args.interactive:
        interpreter.cmdloop()


if __name__ == "__main__":
    main()
