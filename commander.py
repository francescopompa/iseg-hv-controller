from client import IcsClient
from config import ProgramConfig
import logging


class Commander:
    def __init__(self, isc_client: IcsClient, config: ProgramConfig):
        self.isc_client = isc_client
        self.config = config
        self.compare_config_addresses_to_client()
        self.load_channel_map()

    def compare_config_addresses_to_client(self):
        all_modules = self.isc_client.connection.getModules()

        hardware_channel_addresses = set()
        for mod in all_modules:
            for channel in mod.channels:
                hardware_channel_addresses.add(str(channel))
        config_channel_addresses = {str(addr) for addr in self.config.channels}
        if hardware_channel_addresses == config_channel_addresses:
            return True
        else:
            difference_hardware = hardware_channel_addresses - config_channel_addresses
            difference_config = config_channel_addresses - hardware_channel_addresses
            if difference_hardware:
                logging.warning(
                    "WARNING! Not all hardware channels are described with config addresses"
                )
            if difference_config:
                logging.warning("WARNING! Not all channels addresses in config exists")
            if not difference_hardware and not difference_config:
                logging.warning(
                    "something went wrong while comparing config and hardware addresses"
                )
            return False

    def load_channel_map(self):
        addr_to_id_map = {c.addr: c.ch for c in self.config.channels}
        self.isc_client.load_channels(addr_to_id_map)

    def apply_config_defaults(self):
        voltage = self.config.defaults.voltage
        ramp_speed = self.config.defaults.voltage
        trip_current = self.config.defaults.voltage
        power_status = self.config.defaults.voltage

        # zero voltage doesn't matter
        for channel in self.isc_client.channels_dict.values():
            if voltage:
                channel.setControlVoltageSet(voltage)
            if ramp_speed:
                channel.setControlVoltageRampspeedup(ramp_speed)
            if trip_current:
                channel.setControlCurrentSet(
                    trip_current
                )  # not sure about this what units? maybe its also something else see web cmds
            if power_status:
                channel.setControlOn(power_status)

    def apply_channels_config(self):
        for id, channel in self.isc_client.channels_dict.items():
            ...
            # self.config.channels.
