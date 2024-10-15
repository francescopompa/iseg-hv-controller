import cmd
import logging
import sys
from typing import Optional
from pydantic import BaseModel, validator, ValidationError
from isegcontroller.commander import Commander
import os
from isegcontroller import ics_info
import time


def validate_channel_args(args: list) -> dict | bool:
    """
    validates the channel command input
    """

    class ChannelCommandValidator(BaseModel):
        """
        pydantic validator class for the channel section of config toml file
        """

        voltage: Optional[float] = None
        trip_current: Optional[float] = None
        power_status: Optional[bool] = None
        apply: Optional[bool] = None

        @validator("voltage", allow_reuse=True)
        def add_voltage_range_checker(cls, v):
            if 0 <= v <= 2000:
                return v
            else:
                raise ValueError("Voltage out of range 0 to 2kV (V_nom)")

        @validator("trip_current", allow_reuse=True)
        def add_current_range_checker(cls, i):
            if 0 < i <= 4e-3:  # 4 mA
                return i
            else:
                raise ValueError("Trip Current out of range of up to 4mA (I_nom)")

    arg_dict = {}
    expecting_a_value = False
    expect_key = None
    if "on" in args and "off" in args:
        logging.warning("Error. Got both on and off flags")
        return False
    for arg in args:
        if expecting_a_value:  # handels key value pairs (eg.: v 100)
            arg_dict[expect_key] = arg
            expecting_a_value = False
            continue
        match arg:  # New in python 3.10 if older version used convert to if elif ...
            case "on":
                arg_dict["power_status"] = True
            case "off":
                arg_dict["power_status"] = False
            case "v" | "voltage":
                expect_key = "voltage"
                expecting_a_value = True
            case "i" | "current":
                expect_key = "trip_current"
                expecting_a_value = True
            case _:
                logging.warning(f"Error got unexpected argument: {arg}")
                return False

    try:
        channel_mod_values = ChannelCommandValidator(**arg_dict)
        return channel_mod_values.dict()
    except ValidationError as e:
        logging.warning(f"Error couldn't validate inputs: \n {e}")
        return False


class Interpreter(cmd.Cmd):
    """
    interactive command line interpreter based on pythons Cmd module
    """

    commander: Commander

    def __init__(self, commander: Commander):
        super().__init__()
        self.commander = commander

    intro = "Welcome to iseg HV isegcontroller shell. \nType help or ? for a list of available commands \n"
    prompt = "(iseg_hv)"

    @staticmethod
    def clean_line(line: str) -> list[str]:
        line = line.lower()
        args = line.split()
        args = [arg.strip(",.") for arg in args if arg.strip(",.")]
        return args

    def preloop(self) -> None:
        time.sleep(4)  # to remove annyong backup message from iseg
        logging.info("Started Interpreter Cmd Loop")

    def do_ch(self, line: str):
        """view or modify a channel with syntax:
        ch channel_id [v {voltage: float}] [i {trip_current: float}] [on|off]
        if only channel_id is provided defaults to listing all
        [arguments in brackets are optional]
        # maybe should have used an external cli parse/interpreter module that does this nicely
        for example docopt or click even argparse could have worked with some rearranging
        """
        args = self.clean_line(line)

        if len(args) == 0:
            logging.warning("Error Channel Id required")
            return

        try:
            channel_id = int(args[0], 0)  # parse int with base 0 allows for binary or hex
        except ValueError as e:
            logging.info(f"Error parsing channel id:\n {str(e)}")
            return

        if len(args) == 1:
            self.commander.read_channel_info(channel_id)
            return

        args_dict = validate_channel_args(args[1:])
        if not args_dict:
            logging.info("Error parsing cmd args")
            return

        self.commander.modify_channel(channel_id, **args_dict)

    def do_rampspeed(self, line):
        """
        set the crate wide rampspeed in percentage of nominal Voltage(2kV) per second
        default is 20V/s so 1% V_nom/s. maximum is 2% V_nom/sec or 40 V/s
        note: values over 2 are interpreted as V/s with a warning
        """
        args = self.clean_line(line)
        if len(args) != 1:
            logging.warning("Error takes exactly 1 argument ")
            return
        arg = args[0]

        try:
            number = float(arg)
        except ValueError as e:
            logging.warning(f"Error couldnt convert argument {arg} to float")
            return

        if 0 < number <= 2:
            percentage_v_nom_per_sec = number
        elif 2 < number <= 40:
            absolute_v_per_sec = number
            v_nom = 2e3
            percentage_v_nom_per_sec = absolute_v_per_sec / v_nom * 100
            logging.warning(
                f"Warning! input: {number} too large! \n"
                "interpreting it as absolute Volt/s and converting it "
                f"to {percentage_v_nom_per_sec} %V_nom/s"
            )
        else:
            logging.warning("Error input not in range 0  to 2 % V_nom per sec")
            return

        self.commander.set_ramp_speed(percentage_v_nom_per_sec)

    def do_reset(self, line):
        """
        re-applies the config
        """
        logging.info("Reapplying the config")
        self.commander.apply_channels_config()

    def do_config(self, line):
        """
        loads and applies another config
        """
        args = self.clean_line(line)
        if len(args) != 1:
            logging.warning("Error! takes only 1 argument ")
            return
        file_name = args[0]
        if not os.path.isfile(file_name):
            logging.warning("Error! File name seems to be incorrect")
        if self.commander.realtime_load_config(file_name):
            logging.info("Success loading config")
        else:
            logging.info("Something went wrong loading config")

    def do_info(self, line):
        """
        print all info
        last function call can be removed if TMI
        """
        ics_info.print_basic_info(self.commander.ics_client)
        _ = ics_info.get_all_channel_infos(self.commander.ics_client)
        data = ics_info.get_all_channel_infos(self.commander.ics_client)
        print(*data, sep="\n")
        return data

    def get_info(self):
        '''
        It only returns the info, to be used in the slow control
        '''
        _ = ics_info.get_all_channel_infos(self.commander.ics_client)
        data = ics_info.get_all_channel_infos(self.commander.ics_client)        
        return data


    def do_defaults(self, line):
        """
        applies the defaults section in the config to all channels
        """
        logging.info("Applying the default values to all channels")
        self.commander.reset_all_to_defaults()

    def do_all(self, line):
        """
        syntax see ch.
        applies the values to all channels
        """
        args = self.clean_line(line)
        if len(args) == 0:
            logging.warning("error not sufficient arguments provided")
            return
        args_dict = validate_channel_args(args)
        if not args_dict:
            logging.info("Error parsing cmd args")
            return

        logging.info("Applying these values to all channels:" + str(args_dict))

        for channel_id in self.commander.ics_client.channels_dict:
            self.commander.modify_channel(channel_id, **args_dict)

    def do_rawcmd(self, line):
        """
        send a raw command in json form maybe? dk
        """
        logging.warning("NOT IMPLEMENTED")

    def do_quit(self, line):
        """
        quits
        """
        sys.exit(0)
