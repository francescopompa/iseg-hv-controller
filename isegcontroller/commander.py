from isegcontroller.ics_client import IcsClient
from isegcontroller.configurator import ProgramConfig
import logging
import time
from isegcontroller import ics_info


class Commander:
    ics_client: IcsClient
    config: ProgramConfig

    def __init__(self, config_file_name=None):
        if config_file_name:
            self.config = ProgramConfig(config_file_name)
        else:
            self.config = ProgramConfig()

        self.ics_client = IcsClient(
            connection_name="ics_connection" + time.asctime(),
            connection_parameters=f"ws://{self.config.server.ip}:{self.config.server.port}",
            connection_login=self.config.server.username,
            connection_password=self.config.server.password,
        )

        self.ics_client.connect()
        # Todo refactor this to external call print_basic_info(ics_client)
        self.compare_config_addresses_to_client()
        self._load_channel_map_()

    def compare_config_addresses_to_client(self):
        all_modules = self.ics_client.connection.getModules()

        hardware_channel_addresses = set()
        for mod in all_modules:
            for channel in mod.channels:
                hardware_channel_addresses.add(str(channel))
        config_channel_addresses = {str(channel.addr) for channel in self.config.channels.values()}
        if hardware_channel_addresses == config_channel_addresses:  # set have the same members
            return True
        else:
            difference_hardware = hardware_channel_addresses - config_channel_addresses  # set diff
            difference_config = config_channel_addresses - hardware_channel_addresses
            if difference_hardware:
                logging.warning("WARNING! Not all hardware channels are described with config addresses")
            if difference_config:
                logging.warning("WARNING! Not all channels addresses in config exists")
            if not difference_hardware and not difference_config:
                logging.warning("something went wrong while comparing config and hardware addresses")
            return False

    def _load_channel_map_(self):
        """
        This function is called from init and applies the mapping of
        the channel address and channel id to the ics_client class.
        there a channel dict ist constructed
        TODO is there a better way todo this?
        """
        addr_to_id_map = {c.addr: ch_id for ch_id, c in self.config.channels.items()}
        self.ics_client.load_channels_and_modules(addr_to_id_map)

    def reset_all_to_defaults(self):
        voltage = self.config.defaults.voltage
        ramp_speed = self.config.defaults.ramp_speed
        trip_current = self.config.defaults.trip_current
        power_status = self.config.defaults.power_status
        for module in self.ics_client.modules:
            module.setControlVoltageRampspeed(ramp_speed)
        for channel in self.ics_client.channels_dict.values():
            # zero voltage doesn't matter
            if voltage:
                channel.setControlVoltageSet(voltage)
            if trip_current:
                channel.setControlCurrentSet(
                    trip_current
                )  # not sure about this what units? maybe its also something else see web cmds
            if power_status is not None:
                channel.setControlOn(power_status)

    def apply_channels_config(self):
        """
        TODO ADD RESPONSE AND CHECK IF CHANGE successful
         really out of scope
        """
        for ch_id in self.ics_client.channels_dict.keys():
            config_channel = self.config.channels[ch_id]
            voltage = config_channel.voltage
            trip_current = config_channel.trip_current
            if config_channel.apply == False:
                power_status = None
            else:
                power_status = config_channel.power_status
            self.modify_channel(ch_id, voltage, trip_current, power_status)

    def modify_channel(
        self,
        channel_id,
        voltage=None,
        trip_current=None,
        power_status=None,
    ):
        """
        takes the channel id and sets the values to either the supplied or the defaults.
        if both are None doesn't send the command
        """
        try:
            channel = self.ics_client.channels_dict[channel_id]
        except KeyError as e:
            logging.exception("Channel with this id doesnt exist/is not configured")
            return False

        default_channel_config = self.config.defaults

        if not voltage:
            voltage = default_channel_config.voltage
        if not trip_current:
            trip_current = default_channel_config.trip_current

        if voltage:
            channel.setControlVoltageSet(voltage)
        if trip_current:
            channel.setControlCurrentSet(trip_current)
        if power_status is not None:
            channel.setControlOn(power_status)
        return True

    def read_channel_info(self, ch_id):
        """
        prints channel info and complete channel info. last function call can be removed if unwanted/TMI
        """
        try:
            channel = self.ics_client.channels_dict[ch_id]
        except KeyError as e:
            logging.exception("Channel with this id doesnt exist/is not configured")
            return False
        print(ics_info.get_channel_info(ch_id, channel))
        print(ics_info.get_complete_channel_info(channel))

    def set_ramp_speed(self, ramp_speed):
        for mod in self.ics_client.modules:
            mod.setControlCurrentRampspeed(ramp_speed)

    def realtime_load_config(self, config_file_name) -> bool:
        """
        this method loads a config from file and returns the config object
        so it can be overwritten in mainloop. TODO also has to be set here
        """
        new_config = ProgramConfig(config_file_name)
        if new_config:
            self.config = new_config
        else:
            logging.warning("New config wasn't applied!")
            return False

        self.apply_channels_config()
        return True
