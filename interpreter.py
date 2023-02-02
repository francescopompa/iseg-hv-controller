import cmd
import argparse
import logging
from typing import Optional, List, Dict
from pydantic import BaseModel, validator, ValidationError
from commander import Commander


class ChannelCommandValidator(BaseModel):
    """
    pydantic validator class for the channel section of config toml file
    """

    v: Optional[float] = None
    i: Optional[float] = None
    power: Optional[bool] = None

    @validator("v")
    def add_voltage_range_checker(cls, v):
        if 0 < v <= 2000:
            return v
        else:
            raise ValueError("Voltage out of range 0 to 2kV (V_nom)")

    @validator("i")
    def add_current_range_checker(cls, i):
        if 0 < i <= 4e-3:  # 4 mA
            return i
        else:
            raise ValueError("Trip Current out of range 0 to 4mA (I_nom)")


class Interpreter(cmd.Cmd):
    """
    interactive command line interpreter based on pythons Cmd module
    """

    def __init__(self, commander: Commander = None):
        super().__init__()
        self.commander = commander  # our self written commander not the super class. stupid name ik

    intro = (
        "Welcome to iseg HV controller shell. \n"
        "Type help or ? for a list of available commands \n"
    )
    prompt = "(iseg_hv)"

    def preloop(self) -> None:
        logging.info("Started Interpreter Cmd Loop")

    def do_ch(self, line: str):
        """view or modify a channel with syntax:
        ch channel_id [v {voltage: float}] [i {trip_current: float}] [on|off]
        if only channel_id is provided defaults to listing all
        [arguments in brackets are optional]
        # maybe should have used an external cli parse/interpreter module that does this nicely
        for example docopt or click even argparse could have worked with some rearranging
        """
        line = line.lower()
        args = line.split()
        args = [arg.strip(",.") for arg in args if arg.strip(",.")]

        if len(args) == 0:
            print("Error Channel Id required")
            return
        try:
            channel_id = int(args[0], 0)  # parse int with base 0 allows for binary or hex
        except ValueError as e:
            print(f"Error parsing channel id:\n {str(e)}")
            logging.info(f"Error parsing channel id:\n {str(e)}")
            return

        arg_dict = {}
        expecting_a_value = False
        expect_key = None
        if "on" in args and "off" in args:
            print("Error. Got both on and off")
            return
        for arg in args[1:]:
            if expecting_a_value:  # handels key value pairs (v 100)
                arg_dict[expect_key] = arg
                expecting_a_value = False
                continue
            match arg:  # New in python 3.10 if older version used convert to if elif ...
                case "on":
                    arg_dict["power"] = True
                case "off":
                    arg_dict["power"] = False
                case "v" | "i":
                    expect_key = arg
                    expecting_a_value = True
                case _:
                    print(f"Error got unexpected argument: {arg}")

        try:
            channel_mod_values = ChannelCommandValidator(**arg_dict)
        except ValidationError as e:
            print(f"Error couldn't validate inputs: \n {e}")
            return
        print(channel_mod_values)


if __name__ == "__main__":
    interpreter = Interpreter()
    interpreter.cmdloop()
