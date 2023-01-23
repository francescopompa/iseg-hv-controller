import logging

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib


class Config:
    def __init__(self, file="parameter_config.toml"):
        self.file = file
        self.config_dict = {}
        self.load()

    def load(self):
        with open(self.file, 'rb') as f:
            try:
                self.config_dict = tomllib.load(f)
            except tomllib.TOMLDecodeError as e:
                logging.exception("Couldnt parse/load toml parameter config")

    def check_key_completeness(self):
        keys = self.config_dict.keys()

        # First check if the top level keys exist
        if 'Server' in keys and 'Defaults' in keys:

            # Then check the entries of Server
            for key in ['ip', 'port', 'username', 'password']:
                if key not in self.config_dict['Server'].keys():
                    return False

            # Check The Channel Defaults
            for key in ['voltage', 'trip_current']:
                if key not in self.config_dict['Defaults'].keys():
                    return False

            # Check if all 40 channel entrys exist and have an addr attribute
            for i in range(40+1):
                channel_key = 'ch' + str(i)
                if channel_key not in keys or 'addr' not in self.config_dict[channel_key].keys():
                    return False

    def check_server_values(self):
        # TODO connection parameters
        pass
    def check_channel_values(self):
        # TODO check defaults + channels
        # TODO especially check channel addresses
        pass