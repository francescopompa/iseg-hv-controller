"""
This Class is used to talk to the iseg HV and give commands
"""
import logging
import sys
import ics_helper


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
            connection_password="demo"):
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
        connection = ics_helper.establish_connection(self.ics_api, self.connection_name, self.connection_parameters, self.connection_login,
                                                      self.connection_password)
        if type(connection) != self.ics_api.connection:
            logging.error("Failed to connect => Exit.")
            sys.exit(1)
