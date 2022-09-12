"""
This file contains various helper function to help with the iCS software
"""
import importlib
import os
import platform
import time
import sys
import traceback
import logging


def check_is_linux_platform():
    """
    checks for Linux platform
    """
    return platform.system() == 'Linux'


def check_is_win_platform():
    """
    checks for windows platform
    """
    return platform.system() == 'Windows'


def import_from_path(rel_module_path, module_name):
    """
    this function imports the icsClient Python module
    the path and module name are defined here if they aren't given above
    :param rel_module_path: path to the ics lib relative to this file
    :param module_name:  module named can usually be left empty
    :return: the ics module
    """
    # get dir of THIS file
    # cwd is not defined to be file dir
    script_path = os.path.realpath(__file__)
    script_path = os.path.abspath(script_path)

    # rel_module_path defines the location of the python module relative to
    # this file
    if rel_module_path == "":
        if check_is_win_platform():
            rel_module_path = os.path.dirname(script_path)
            rel_module_path = os.path.join(
                rel_module_path, "icsPythonForWindows", "bin")
        elif check_is_linux_platform():
            rel_module_path = os.path.dirname(script_path)
            rel_module_path = os.path.join(
                rel_module_path,
                "icsPythonForLinux",
                "platform",
                "linux",
                "64")

    if rel_module_path != "":
        sys.path.append(rel_module_path)

    # the module name (depends on the python version)
    if module_name == "":
        module_name = f"icsClientPython_{sys.version_info[0]}"

    # try to import the module
    try:
        ics_client = importlib.import_module(module_name)

    except ImportError:

        # print traceback
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        logging.error("".join('!! ' + line for line in lines))

        logging.error(
            "Failed to load the module \"%s\" \n from path \"%s\"",
            module_name,
            rel_module_path)
        full_path = os.path.join(rel_module_path, module_name)
        if check_is_linux_platform():
            full_path = full_path + ".so"
        if not os.path.exists(full_path):
            logging.warning(
                "%s doesn't exist \n \t\t=> make sure that the module is found at this location",
                full_path)
        logging.warning(
            "The Python modules links to shared Qt libraries\n\t\t  => make sure the Qt libraries are found")
        if check_is_linux_platform():
            error_msg = "   => make sure the LD_LIBRARY_PATH environment variable is set properly."
            try:
                path = os.environ['LD_LIBRARY_PATH']
            except KeyError:
                path = "--undefined--"
            error_msg += f"   => LD_LIBRARY_PATH == {path}"

            logging.warning(error_msg)
        return 0

    logging.info(
        "Sucessfully imported module %s(version %s) from path %s",
        module_name,
        str(ics_client.getVersion()),
        rel_module_path)
    return ics_client


def establish_connection(ics_api,
                         connection_name,
                         connection_ip,
                         connection_login,
                         connection_password):
    """
    Establishes a connection waits for it and returns a connection object
    """
    error_msg = ics_api.connect(connection_name,
                                connection_ip,
                                connection_login,
                                connection_password)
    if error_msg == 'error':
        logging.warning(
            "The connection \"%s\" already exists", connection_name)

    return ics_api.wait_for_connection(connection_name, connection_ip)


def wait_for_connection(ics_api, connection_name, connection_ip):
    """
    Waits for a connection to be established and returns the connections object
    Can block the application for quite a while
    TODO: async?
    """
    # this might take a while.
    logging.info("Waiting for connection to be created ...")
    counter = 0
    connection = ics_api.findConnection(connection_name)
    while counter < 10 and not isinstance(connection, ics_api.connection):
        time.sleep(1)
        connection = ics_api.findConnection(connection_name)
        counter = counter + 1

    if not isinstance(connection, ics_api.connection):
        # list is empty
        logging.error(
            "The connection \"%s\" couldn't be created.", connection_name)
        return 0

    # this might take a while.
    logging.info("Waiting for connection to %s to be ready ...", connection_ip)
    counter = 0
    status = connection.getStatusConnectionStatus()
    while counter < 10 and status != "Configured":
        time.sleep(1)
        new_status = connection.getStatusConnectionStatus()
        counter = counter + 1
        if new_status != status:
            status = new_status
            logging.info("%s sec : connection status == %s", counter, status)

    if status != "Configured":
        # list is empty
        logging.error(
            "Connection to %s couldn't be established.",
            connection_ip)
        return 0

    logging.info("Connected to \"%s\"", connection)
    return connection
