"""
This Class is used to talk to the iseg HV and give commands
"""
import json
import logging
import sys
import time
from typing import Optional, Dict
import ics_helper
from configurator import ProgramConfig
from ics_channel_abstraction import ICSChannelAbstraction


class IcsClient:
    """
    Object to talk with the isc of the iseg HV
    The isc library needs to be correctly setup see ics_helper.py for more
    """

    channels_dict: Dict[int, ICSChannelAbstraction] = {}

    def __init__(
        self,
        connection_name="ics_connection1",
        connection_parameters="ws://localhost:1234",
        connection_login="demo",
        connection_password="demo",
    ):
        # import icsClient module
        self.ics_api = ics_helper.import_from_path("", "")

        if not self.ics_api:
            logging.error("Failed to import icsClient module => Exit.")
            sys.exit(1)

        self.connection = None
        self.connection_name = connection_name
        self.connection_parameters = connection_parameters
        self.connection_login = connection_login
        self.connection_password = connection_password

    def __del__(self):
        def disconnect_all():
            all_connections = self.ics_api.getConnections()
            for connection in all_connections:
                connection.disconnect()

        disconnect_all()
        # end connection

    def connect(self):
        """
        connects to the actual crate with the param of this class
        """
        self.connection = self.__establish_connection(
            self.connection_name,
            self.connection_parameters,
            self.connection_login,
            self.connection_password,
        )
        if not isinstance(self.connection, self.ics_api.connection):
            logging.error("Failed to connect => Exit.")
            sys.exit(1)

        # Power on CC24 crate with websocket command
        power_frame = {
            "i": "<session_id>",
            "t": "request",
            "c": [
                {
                    "c": "getItem",
                    "p": {
                        "p": {"l": "0", "a": "1000", "c": ""},
                        "i": "Control.power",
                        "v": "",
                        "u": "",
                    },
                }
            ],
            "r": "websocket",
        }
        power_frame = json.dumps(power_frame)  # Convert to json string
        self.connection.rawCommand(power_frame)

        # Check the result of the previous power on command
        result_cmd = {
            "i": "<session_id>",
            "t": "request",
            "c": [
                {
                    "c": "setItem",
                    "p": {
                        "p": {"l": "0", "a": "1000", "c": ""},
                        "i": "Control.power",
                        "v": "1",
                        "u": "",
                    },
                }
            ],
            "r": "websocket",
        }
        result_cmd = json.dumps(result_cmd)
        result = self.connection.rawCommand(result_cmd)
        logging.info(result)

        time.sleep(5)

    def __wait_for_connection(self, connection_name, connection_ip):
        """
        demo code from iseg not that pretty
        Waits for a connection to be established and returns the connections object
        Can block the application for quite a while
        TODO: async?
        """
        # this might take a while.
        logging.info("Waiting for connection to be created ...")
        counter = 0
        connection = self.ics_api.findConnection(connection_name)
        while counter < 10 and not isinstance(connection, self.ics_api.connection):
            time.sleep(1)
            connection = self.ics_api.findConnection(connection_name)
            counter = counter + 1

        if not isinstance(connection, self.ics_api.connection):
            # list is empty
            logging.error('The connection "%s" couldn\'t be created.', connection_name)
            return 0

        # this might take a while.
        logging.info("Waiting for connection to %s to be ready ...", connection_ip)
        counter = 0
        status = connection.getStatusConnectionStatus()
        while counter < 10 and (status != "Configured" and status != "Connected"):
            time.sleep(1)
            new_status = connection.getStatusConnectionStatus()
            counter = counter + 1
            if new_status != status:
                status = new_status
                logging.info("%s sec : connection status == %s", counter, status)

        if status != "Configured" and status != "Connected":
            # list is empty
            logging.error("Connection to %s couldn't be established.", connection_ip)
            return 0

        logging.info('Connected to "%s"', connection)
        return connection

    def __establish_connection(
        self, connection_name, connection_ip, connection_login, connection_password
    ):
        """
        Establishes a connection waits for it and returns a connection object
        """
        error_msg = self.ics_api.connect(
            connection_name, connection_ip, connection_login, connection_password
        )
        if error_msg == "error":
            logging.warning('The connection "%s" already exists', connection_name)

        return self.__wait_for_connection(connection_name, connection_ip)

    def load_channels(self, address_channel_map):
        """
        has to be called with a valid mapping in  a config
         currently from commander
        """
        all_modules = self.connection.getModules()

        hardware_channels = {}
        for mod in all_modules:
            for channel in mod.channels:
                channel_address = str(channel)
                channel_id = address_channel_map[channel_address]
                hardware_channels[channel_id] = channel
        self.channels_dict = hardware_channels
