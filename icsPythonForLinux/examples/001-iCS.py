
## this python script can be used with icsClientPython_3
##      to test a connection to an scpi module connected at ttyS5



import sys
import time
import math
import argparse
import traceback
import importlib
import types

import clientCommon

connection_name = "new_iCS_connection"
connection_ip = "ws://ics.iseg-hv.com:8080"
#connection_ip = "ws://localhost:1234"
#connection_ip = "ws://192.168.0.101"
connection_login = "demo"
connection_password = "demo"

## import icsClient module 
icsClient = clientCommon.importFromPath("", "icsClientPython_3")
if icsClient == 0:
    print("Failed to import icsClient module => Exit.")
    exit(1)

## establish a connection and wait until it is ready (with timeout)
connection = clientCommon.establishConnection(icsClient, connection_name, connection_ip, connection_login, connection_password)
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

