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
        """
        This function is called from init and applies the mapping of
        the channel address and channel id to the isc_client class.
        there a channel dict ist constructed
        TODO is there a better way todo this?
        """
        addr_to_id_map = {c.addr: ch_id for ch_id, c in self.config.channels.items()}
        self.isc_client.load_channels(addr_to_id_map)

    def reset_all_to_defaults(self):
        voltage = self.config.defaults.voltage
        ramp_speed = self.config.defaults.ramp_speed
        trip_current = self.config.defaults.trip_current
        power_status = self.config.defaults.power_status

        for channel in self.isc_client.channels_dict.values():
            # zero voltage doesn't matter
            if voltage:
                channel.setControlVoltageSet(voltage)
            if ramp_speed:
                channel.setControlVoltageRampspeedUp(ramp_speed)
            if trip_current:
                channel.setControlCurrentSet(
                    trip_current
                )  # not sure about this what units? maybe its also something else see web cmds
            if power_status is not None:
                channel.setControlOn(power_status)

    def apply_channels_config(self):
        """
        TODO ADD RESPONSE AND CHECK IF CHANGE successful
        """
        for ch_id in self.isc_client.channels_dict.keys():
            config_channel = self.config.channels[ch_id]
            voltage = config_channel.voltage
            ramp_speed = config_channel.ramp_speed
            trip_current = config_channel.trip_current
            power_status = config_channel.power_status
            self.modify_channel(ch_id, voltage, ramp_speed, trip_current, power_status)

    def modify_channel(
        self,
        channel_id,
        voltage=None,
        ramp_speed=None,
        trip_current=None,
        power_status=None,
    ):
        """
        takes the channel id and sets the values to either the supplied or the defaults.
        if both are None doesn't send the command
        """
        channel = self.isc_client.channels_dict[channel_id]
        default_channel_config = self.config.defaults

        if not voltage:
            voltage = default_channel_config.voltage
        if not ramp_speed:
            ramp_speed = default_channel_config.ramp_speed
        if not trip_current:
            trip_current = default_channel_config.trip_current
        if power_status is None:
            power_status = default_channel_config.power_status

        if voltage:
            channel.setControlVoltageSet(voltage)
        if ramp_speed:
            channel.setControlVoltageRampspeedUp(ramp_speed)
            channel.setControlVoltageRampspeedDown(ramp_speed)
        if trip_current:
            channel.setControlCurrentSet(trip_current)
        if power_status is not None:
            channel.setControlOn(power_status)

    def realtime_load_config(self, filename):
        """
        this method loads a config from file and returns the config object
        so it can be overwritten in mainloop. TODO also has to be set here
        """
        pass
        # TODO reload config
        config = None
        return config
