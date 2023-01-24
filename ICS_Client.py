"""
This Class is used to talk to the iseg HV and give commands
"""
import logging
import sys
import ICS_Helper
import time
import json


class IcsClient:
    """
    Object to talk with the isc of the iseg HV
    The isc library needs to be correctly setup see ics_helper.py for more
    """

    def __init__(
        self,
        connection_name="ics_connection1",
        connection_parameters="ws://localhost:1234",
        connection_login="demo",
        connection_password="demo",
    ):
        # import icsClient module
        self.ics_api = ICS_Helper.import_from_path("", "")

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
        self.connection = ICS_Helper.establish_connection(
            self.ics_api,
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
        print(power_frame)

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
        print(result)

        time.sleep(5)
