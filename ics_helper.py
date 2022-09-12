"""
This file contains various helper function to help with the iCS software
"""
import importlib
import os
import platform
import sys
import traceback


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

    # rel_module_path defines the location of the python module relative to this file
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
        print("".join('!! ' + line for line in lines))

        print(f"Failed to load the module \"{module_name}\"")
        print(f"   from path \"{rel_module_path}\"")
        full_path = os.path.join(rel_module_path, module_name)
        if check_is_linux_platform():
            full_path = full_path + ".so"
        if not os.path.exists(full_path):
            print(f"   {full_path} doesn't exist")
            print("   => make sure that the module is found at this location")
        print("= The Python modules links to shared Qt libraries")
        print("   => make sure the Qt libraries are found")
        if check_is_linux_platform():
            print(
                "   => make sure the LD_LIBRARY_PATH environment variable is set properly.")
            try:
                path = os.environ['LD_LIBRARY_PATH']
            except KeyError:
                path = "--undefined--"
            print(f"   => LD_LIBRARY_PATH == {path}")

        return 0

    print(
        f"Sucessfully imported module \"{module_name}\" "
        "(version {ics_client.getVersion()}) from path \"{rel_module_path}\"")
    return ics_client
