
## this python script can be used with icsClientPython_3
##      to test a connection to an scpi module connected at ttyS5

# The connection parameters must be given when the example is launched example:
#       python3 001-iCS.py -c ws://192.168.0.25:8080
#


import sys
import time
import math
import argparse
import traceback
import importlib
import types
import os

import clientCommon

connectionName = "new_iCS_connection"
#connectionParameters = "ws://ics.iseg-hv.com:8080"
connectionParameters = "ws://localhost:1234"
connectionLogin = "demo"
connectionPassword = "demo"

for argvIndex in range(0, len(sys.argv)):
    if argvIndex + 1 < len(sys.argv):
        if sys.argv[argvIndex] == "-c":
            connectionParameters = sys.argv[argvIndex + 1]

## this must specify the location of the icsClientPython_3 python module
pythonModulePath = "../platform/linux/64/"
if clientCommon.checkIsWindowsPlatform():
    pythonModulePath = "../bin/"
pythonModulePath = os.path.abspath(pythonModulePath)

## import icsClient module 
icsClient = clientCommon.importFromPath(pythonModulePath, "icsClientPython_3")
if icsClient == 0:
    print("Failed to import icsClient module => Exit.")
    exit(1)

## establish a connection and wait until it is ready (with timeout)
connection = clientCommon.establishConnection(icsClient, connectionName, connectionParameters, connectionLogin, connectionPassword)
if type(connection) != icsClient.connection:
    print("Failed to connect => Exit.")
    exit(1)

## 
connection.rawCommand("{\"i\":\"<session_id>\",\"t\":\"request\",\"c\":[{\"c\":\"getItem\",\"p\":{\"p\":{\"l\":\"0\",\"a\":\"1000\",\"c\":\"\"},\"i\":\"Control.power\",\"v\":\"\",\"u\":\"\"}}],\"r\":\"websocket\"}")

all_modules = connection.getModules()
print("All modules {0}.".format(all_modules))

all_crates = connection.getCrates()
print("All crates {0}.".format(all_crates))

clientCommon.disconnectAll(icsClient)

