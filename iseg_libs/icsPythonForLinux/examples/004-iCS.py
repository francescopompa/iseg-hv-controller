##Here is a small example to start writing your your own scripts:
import argparse
import time
import traceback
import importlib
import types
import os

import clientCommon

connectionName = "new_iCS_connection"
#connectionParameters = "ws://localhost"
connectionParameters = "ws://ics.iseg-hv.com:8080"
connectionLogin = "demo"
connectionPassword = "demo"

## import icsClient module
#icsClient = clientCommon.importFromPath("/usr/lib", "libicsClientPython3")
icsClient = clientCommon.importFromPath("", "icsClientPython_3") 
if icsClient == 0:
	print("Failed to import icsClient module => Exit.")
	exit(1)

## establish a connection and wait until it is ready (with timeout)
connection = clientCommon.establishConnection(icsClient, connectionName, connectionParameters, connectionLogin, connectionPassword)
if type(connection) != icsClient.connection:
	print("Failed to connect => Exit.")
	exit(1)

## Power on CC24 crate
power_frame = "{\"i\":\"<session_id>\",\"t\":\"request\",\"c\":[{\"c\":\"getItem\",\"p\":{\"p\":{\"l\":\"0\",\"a\":\"1000\",\"c\":\"\"},\"i\":\"Control.power\",\"v\":\"\",\"u\":\"\"}}],\"r\":\"websocket\"}"

connection.rawCommand(power_frame)
print(power_frame)

result = connection.rawCommand("{\"i\":\"<session_id>\",\"t\":\"request\",\"c\":[{\"c\":\"setItem\",\"p\":{\"p\":	{\"l\":\"0\",\"a\":\"1000\",\"c\":\"\"},\"i\":\"Control.power\",\"v\":\"1\",\"u\":\"\"}}],\"r\":\"websocket\"}")
print(result)

all_crates = connection.getCrates()
print("All crates {0}.".format(all_crates))

all_modules = connection.getModules()
print("All modules {0}.".format(all_modules))

all_channels = all_modules[0].channels
print("All channels {0}.".format(all_channels))

##time to fill the cache from iCSservice
time.sleep(5)

def outputModule(item, function):
	print(item  + str(function))

def outputModuleInt(item, function):
	print(item  + str(int(function)))

outputModule("Firmwarename: ", all_modules[0].getStatusFirmwareName())
outputModuleInt("Seriennummer: ", all_modules[0].getStatusSerialNumber())
outputModule("Release: ", all_modules[0].getStatusFirmwareRelease())
outputModule("Temperatur: ", all_modules[0].getStatusTemperature())
#all_channels[1].setControlVoltageSet("123")

def output(channel, item, function):
	print(item + str(channel) + ": " + str(function))

def outputChannelItems():
	all_channels = all_modules[0].channels
	for channel in range(0, len(all_channels)):
		output(channel, "Status.voltageNominal", all_channels[channel].getStatusVoltageNominal())
	for channel in range(0, len(all_channels)):
		output(channel, "Control.voltageSet", all_channels[channel].getControlVoltageSet())
	for channel in range(0, len(all_channels)):
		output(channel, "Status.voltageMeasure", all_channels[channel].getStatusVoltageMeasure())
	for channel in range(0, len(all_channels)):
		output(channel, "Status.currentNominal", all_channels[channel].getStatusCurrentNominal())
	for channel in range(0, len(all_channels)):
		output(channel, "Control.currentSet", all_channels[channel].getControlCurrentSet())
	for channel in range(0, len(all_channels)):
		output(channel, "Status.currentMeasure", all_channels[channel].getStatusCurrentMeasure())
	for channel in range(0, len(all_channels)):
		output(channel, "Status.voltageLimitExceeded", all_channels[channel].getStatusVoltageLimitExceeded())
	for channel in range(0, len(all_channels)):
		output(channel, "Status.currentLimitExceeded", all_channels[channel].getStatusCurrentLimitExceeded())
	for channel in range(0, len(all_channels)):
		output(channel, "Status.currentTrip", all_channels[channel].getStatusTrip())
	for channel in range(0, len(all_channels)):
		output(channel, "Status.on", all_channels[channel].getStatusOn())
	for channel in range(0, len(all_channels)):
		output(channel, "Status.emergenc", all_channels[channel].getStatusEmergency())
	for channel in range(0, len(all_channels)):
		output(channel, "Setup.delayedTripAction", all_channels[channel].getSetupDelayedTripAction())
	for channel in range(0, len(all_channels)):
		output(channel, "Setup.delayedTripTime", all_channels[channel].getSetupDelayedTripTime())

outputChannelItems()

clientCommon.disconnectAll(icsClient)
