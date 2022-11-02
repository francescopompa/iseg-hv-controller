## this python script can be used with icsClientPython_3
##      to test a connection to an scpi module connected at ttyS5


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
# connectionParameters = "ws://localhost:1234"
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
# icsClient = icsClientCommon.importFromPath("", "icsClientPython_for_iCS_3")	#Library from last year
icsClient = clientCommon.importFromPath(
    pythonModulePath, "icsClientPython_3"
)  # Windows
# icsClient = icsClientCommon.importFromPath("/home/jr/iseg/isegcontrol_DEV_191021_64/platform/linux/64a/", "libicsClientPython3") #Ubuntu Linux 18.04
if icsClient == 0:
    print("Failed to import icsClient module => Exit.")
    exit(1)

## establish a connection and wait until it is ready (with timeout)
connection = clientCommon.establishConnection(
    icsClient, connectionName, connectionParameters, connectionLogin, connectionPassword
)
if type(connection) != icsClient.connection:
    print("Failed to connect => Exit.")
    exit(1)

##


power_frame = '{"i":"<session_id>","t":"request","c":[{"c":"getItem","p":{"p":{"l":"0","a":"1000","c":""},"i":"Control.power","v":"","u":""}}],"r":"websocket"}'

connection.rawCommand(power_frame)

print(power_frame)

result = connection.rawCommand(
    '{"i":"<session_id>","t":"request","c":[{"c":"setItem","p":{"p":{"l":"0","a":"1000","c":""},"i":"Control.power","v":"1","u":""}}],"r":"websocket"}'
)
print(result)

all_crates = connection.getCrates()
print("All crates {0}.".format(all_crates))

all_modules = connection.getModules()
print("All modules {0}.".format(all_modules))

all_channels = all_modules[0].channels
print("All channels {0}.".format(all_channels))
time.sleep(5)


def outputModule(item, function):
    time.sleep(0.01)
    print(item + str(function))


def outputModuleInt(item, function):
    time.sleep(0.01)
    print(item + str(int(function)))


outputModule("Firmwarename: ", all_modules[0].getStatusFirmwareName())
outputModuleInt("Seriennummer: ", all_modules[0].getStatusSerialNumber())
outputModule("Release: ", all_modules[0].getStatusFirmwareRelease())
outputModule("Temperatur: ", all_modules[0].getStatusTemperature())

# all_channels[1].setControlVoltageSet("123")


def output(channel, item, function):
    time.sleep(0.01)
    print(item + str(channel) + ": " + str(function))


def outputChannelItems():
    all_channels = all_modules[0].channels
    for channel in range(0, len(all_channels)):
        output(
            channel,
            "Status.voltageNominal",
            all_channels[channel].getStatusVoltageNominal(),
        )
    for channel in range(0, len(all_channels)):
        output(
            channel, "Control.voltageSet", all_channels[channel].getControlVoltageSet()
        )
    for channel in range(0, len(all_channels)):
        output(
            channel,
            "Status.voltageMeasure",
            all_channels[channel].getStatusVoltageMeasure(),
        )
    for channel in range(0, len(all_channels)):
        output(
            channel,
            "Status.currentNominal",
            all_channels[channel].getStatusCurrentNominal(),
        )
    #    for channel in range(0, len(all_channels)):
    #        output(channel, "Control.voltageBounds", all_channels[channel].getControlVoltageBounds())
    #    for channel in range(0, len(all_channels)):
    #        output(channel, "Control.voltageRampspeedDown", all_channels[channel].getControlVoltageRampspeedDown())
    #    for channel in range(0, len(all_channels)):
    #        output(channel, "Control.voltageRampspeedUp", all_channels[channel].getControlVoltageRampspeedUp())
    #    for channel in range(0, len(all_channels)):
    #        output(channel, "Status.voltageRampspeedMin", all_channels[channel].getStatusVoltageRampspeedMin())
    #    for channel in range(0, len(all_channels)):
    #        output(channel, "Status.voltageRampspeedMax", all_channels[channel].getStatusVoltageRampspeedMax())
    #    for channel in range(0, len(all_channels)):
    #       output(channel, "Control.voltageVctCoefficient", all_channels[channel].getControlVctCoefficient())
    for channel in range(0, len(all_channels)):
        output(
            channel, "Control.currentSet", all_channels[channel].getControlCurrentSet()
        )
    for channel in range(0, len(all_channels)):
        output(
            channel,
            "Status.currentMeasure",
            all_channels[channel].getStatusCurrentMeasure(),
        )
    #    for channel in range(0, len(all_channels)):
    #        output(channel, "Control.currentBounds", all_channels[channel].getControlCurrentBounds())
    #    for channel in range(0, len(all_channels)):
    #        output(channel, "Control.currentRampspeedDown", all_channels[channel].getControlCurrentRampspeedDown())
    #    for channel in range(0, len(all_channels)):
    #        output(channel, "Control.currentRampspeedUp", all_channels[channel].getControlCurrentRampspeedUp())
    #    for channel in range(0, len(all_channels)):
    #        output(channel, "Status.currentRampSpeedMin", all_channels[channel].getStatusCurrentRampspeedMin())
    #    for channel in range(0, len(all_channels)):
    #        output(channel, "Status.currentRampSpeedMax", all_channels[channel].getStatusCurrentRampspeedMax())
    for channel in range(0, len(all_channels)):
        output(
            channel,
            "Status.voltageLimitExceeded",
            all_channels[channel].getStatusVoltageLimitExceeded(),
        )
    for channel in range(0, len(all_channels)):
        output(
            channel,
            "Status.currentLimitExceeded",
            all_channels[channel].getStatusCurrentLimitExceeded(),
        )
    for channel in range(0, len(all_channels)):
        output(channel, "Status.currentTrip", all_channels[channel].getStatusTrip())
    for channel in range(0, len(all_channels)):
        output(channel, "Status.on", all_channels[channel].getStatusOn())
    for channel in range(0, len(all_channels)):
        output(channel, "Status.emergenc", all_channels[channel].getStatusEmergency())
    for channel in range(0, len(all_channels)):
        output(
            channel,
            "Setup.delayedTripAction",
            all_channels[channel].getSetupDelayedTripAction(),
        )
    for channel in range(0, len(all_channels)):
        output(
            channel,
            "Setup.delayedTripTime",
            all_channels[channel].getSetupDelayedTripTime(),
        )


outputChannelItems()


# sys.stdout = open("ics-python3-channel-items.txt", "w")
# print(help(all_channels[0]))
# sys.stdout.close()

# sys.stdout = open("ics-python3-module-items.txt", "w")
# print(help(all_modules[0]))
# sys.stdout.close()

# sys.stdout = open("ics-python3-crates-items.txt", "w")
# print(help(all_crates[0]))
# sys.stdout.close()

clientCommon.disconnectAll(icsClient)
