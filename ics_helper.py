"""
This file contains various helper function to help with the iCS software
most importantly an import function for the api
"""
import importlib
import logging
import os
import platform
import sys
import traceback


def import_from_path(rel_module_path, module_name=""):
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
        if platform.system() == "Windows":
            rel_module_path = os.path.dirname(script_path)
            rel_module_path = os.path.join(
                rel_module_path, "icsPythonForWindows", "bin"
            )
        elif platform.system() == "Linux":
            rel_module_path = os.path.dirname(script_path)
            rel_module_path = os.path.join(
                rel_module_path, "icsPythonForLinux", "platform", "linux", "64"
            )

    if rel_module_path != "":
        sys.path.append(rel_module_path)

    # the module name (depends on the python version)
    if module_name == "":
        module_name = f"icsClientPython_{sys.version_info[0]}"

    # try to import the module
    try:
        ics_api = importlib.import_module(module_name)

    except ImportError:

        # print traceback
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        logging.error("".join("!! " + line for line in lines))

        logging.error(
            'Failed to load the module "%s" \n from path "%s"',
            module_name,
            rel_module_path,
        )
        full_path = os.path.join(rel_module_path, module_name)
        if platform.system() == "Linux":
            full_path = full_path + ".so"
        if not os.path.exists(full_path):
            logging.warning(
                "%s doesn't exist \n \t\t=> make sure that the module is found at this location",
                full_path,
            )
        logging.warning(
            "The Python modules links to shared Qt libraries\n\t\t  => make sure the Qt libraries are found"
        )
        if platform.system() == "Linux":
            error_msg = "   => make sure the LD_LIBRARY_PATH environment variable is set properly."
            try:
                path = os.environ["LD_LIBRARY_PATH"]
            except KeyError:
                path = "--undefined--"
            error_msg += f"   => LD_LIBRARY_PATH == {path}"

            logging.warning(error_msg)
        return 0

    logging.info(
        "Sucessfully imported module %s(version %s) from path %s",
        module_name,
        str(ics_api.getVersion()),
        rel_module_path,
    )
    return ics_api
