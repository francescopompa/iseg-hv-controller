from isc_client import IcsClient
from configurator import ProgramConfig
import logging


class Commander:
    def __init__(self, isc_client: IcsClient, config: ProgramConfig):
        self.isc_client = isc_client
        self.config = config
        self.compare_config_addresses_to_client()
        self._load_channel_map_()

    def compare_config_addresses_to_client(self):
        all_modules = self.isc_client.connection.getModules()

        hardware_channel_addresses = set()
        for mod in all_modules:
            for channel in mod.channels:
                hardware_channel_addresses.add(str(channel))
        config_channel_addresses = {
            str(channel.addr) for channel in self.config.channels.values()
        }
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

    def _load_channel_map_(self):
        addr_to_id_map = {c.addr: ch_id for ch_id, c in self.config.channels.items()}
        self.isc_client.load_channels(addr_to_id_map)

    def reset_all_to_defaults(self):
        voltage = self.config.defaults.voltage
        ramp_speed = self.config.defaults.voltage
        trip_current = self.config.defaults.voltage
        power_status = self.config.defaults.voltage

        for channel in self.isc_client.channels_dict.values():
            # zero voltage doesn't matter
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
        """
        TODO ADD RESPONSE AND CHECK IF CHANGEG
        :return:
        """
        for ch_id in self.isc_client.channels_dict.keys():
            voltage = self.config.channels[ch_id].voltage
            ramp_speed = self.config.channels[ch_id].ramp_speed
            trip_current = self.config.channels[ch_id].trip_current
            power_status = self.config.channels[ch_id].power_status
            self.modify_channel(ch_id, voltage, ramp_speed, trip_current, power_status)

    def modify_channel(
        self,
        channel_id,
        voltage=None,
        ramp_speed=None,
        trip_current=None,
        power_status=None,
    ):
        channel = self.isc_client.channels_dict[channel_id]

        if not voltage:
            voltage = self.config.defaults.voltage
        if not ramp_speed:
            ramp_speed = self.config.defaults.ramp_speed
        if not trip_current:
            trip_current = self.config.defaults.trip_current
        if power_status is None:
            power_status = self.config.defaults.power_status

        if voltage:
            channel.setControlVoltageSet(voltage)
        if ramp_speed:
            channel.setControlVoltageRampspeedUp(ramp_speed)
        if trip_current:
            channel.setControlCurrentSet(trip_current)
        if power_status is not None:
            channel.setControlOn(power_status)

    def reload_config(self, filename):
        pass
        # TODO
        config = None
        return config
