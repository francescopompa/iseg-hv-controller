import logging
from pydantic import BaseModel, validator, Field
from ipaddress import IPv4Address
from typing import Optional
from collections import Counter
import re

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib


def create_pydantic_validation_class():
    class ChannelConfigSection(BaseModel):
        addr: str
        voltage: Optional[float] = None
        ramp_speed: Optional[float] = None
        trip_current: Optional[float] = None

        @validator("addr")
        def addr_crate_module_channel_checker(cls, v):
            if re.match(r"\d{1,2}\.\d{1,2}\.\d{1,2}", v) is None:
                raise ValueError(
                    "not a correct iseg address \n"
                    '(must be like [crate_number].[module_number].[channel_number] eg. "0.1.2")'
                )
            return v

    class DefaultsConfigSection(BaseModel):
        voltage: float
        ramp_speed: float
        trip_current: float

    class ServerConfigSection(BaseModel):
        ip: IPv4Address
        port: int
        username: str
        password: str

    class ConfigValidatorModel(BaseModel):
        Server: ServerConfigSection
        Defaults: DefaultsConfigSection

    # dynamicly create entry for the 40 channel entries
    cls_annotations = {f"ch{i}": ChannelConfigSection for i in range(1, 40 + 1)}
    class_appendages = {
        "ch" + str(i): Field(ChannelConfigSection) for i in range(1, 40 + 1)
    }
    class_appendages.update({"__annotations__": cls_annotations})
    validation_cls = type(
        "ConfigValidationClass", (ConfigValidatorModel,), class_appendages
    )

    return validation_cls


class ProgramConfig:
    # validation class is dynamically created to reflect the 40 ch. else they'd have to be hardcoded
    # might have been cleaner that way
    validation_cls = create_pydantic_validation_class()
    config: validation_cls

    def __init__(self, file="parameter_config.toml"):
        self.file = file
        self.load()
        self.control_uniqueness_addresses()

    def load(self):
        with open(self.file, "rb") as f:
            try:
                data = tomllib.load(f)
                self.config = self.validation_cls(**data)
            except tomllib.TOMLDecodeError as e:
                logging.exception("Couldn't parse/load toml parameter config")

    def control_uniqueness_addresses(self):
        d = self.config.dict()
        channels = [d[f"ch{i}"] for i in range(1, 40 + 1)]
        channel_addresses = [ch['addr'] for ch in channels]
        counted = Counter(channel_addresses)
        for elem in counted:
            if counted[elem] > 1:
                logging.error(f"Address {elem} is not unique!!")
                raise ValueError(f"Address {elem} is not unique!!")

    def apply_config(self, ics_client):
        """
        apply the whole config
        """
        ...

if __name__ == "__main__":
    c = ProgramConfig()
    print(c.config)
