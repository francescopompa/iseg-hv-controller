import logging
import re
from collections import Counter
from ipaddress import IPv4Address
from typing import Optional, List, Dict

from pydantic import BaseModel, validator, Field

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib


class ChannelConfigSection(BaseModel):
    addr: str
    voltage: Optional[float] = None
    ramp_speed: Optional[float] = None
    trip_current: Optional[float] = None
    power_status: Optional[bool] = False

    @validator("addr")
    def addr_crate_module_channel_checker(cls, v):
        if re.match(r"\d{1,2}\.\d{1,2}\.\d{1,2}", v) is None:
            raise ValueError(
                "not a correct iseg address \n"
                '(must be like [crate_number].[module_number].[channel_number] eg. "0.1.2")'
            )
        return v


class DefaultsConfigSection(BaseModel):
    voltage: Optional[float] = None
    ramp_speed: Optional[float] = None
    trip_current: Optional[float] = None
    power_status: Optional[bool] = False


class ServerConfigSection(BaseModel):
    ip: IPv4Address
    port: int
    username: str
    password: str


class ConfigValidatorModel(BaseModel):
    Server: ServerConfigSection
    Defaults: DefaultsConfigSection
    Channels: Dict[int, ChannelConfigSection]


class ProgramConfig:
    """
    validation class is dynamically created to reflect the 40 ch. else they'd have to be hardcoded
    might have been cleaner that way
    """

    server: ServerConfigSection
    defaults: DefaultsConfigSection
    channels: Dict[int, ChannelConfigSection]

    def __init__(self, file="parameter_config_v1.toml"):
        self.file = file
        self.load()
        self.control_uniqueness_addresses()

    def load(self):
        with open(self.file, "rb") as f:
            try:
                data = tomllib.load(f)
                validated_config = ConfigValidatorModel(**data)
                self.server = validated_config.Server
                self.defaults = validated_config.Defaults
                self.channels = validated_config.Channels
            except tomllib.TOMLDecodeError as e:
                logging.exception("Couldn't parse/load toml parameter config")

    def control_uniqueness_addresses(self):
        channel_addresses = [c.addr for c in self.channels.values()]
        counted = Counter(channel_addresses)
        for elem in counted:
            if counted[elem] > 1:
                logging.error(f"Address {elem} is not unique!!")
                raise ValueError(f"Address {elem} is not unique!!")


if __name__ == "__main__":
    c = ProgramConfig()
    print(c.server)
    print(c.defaults)
    print(c.channels)
