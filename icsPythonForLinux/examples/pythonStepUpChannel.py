
#
# This example steps up a channel that has to be specified. Voltage and current measurements are written to a CSV file
#       in regular time intervals.
#
# It makes use of the icsClientPython_3 Python library.
#
# The following parameters below might have to be adjusted.
#
# For the connection to the iCS :
#       
#    m_login
#    m_password
#
# The connection parameters must be given when the example is launched example:
#       python3 pythonStepUpChannel.py -c ws://192.168.0.25:8080
#
#
# Define the channel that will be stepped up :
#    m_lineIndex
#    m_moduleAddress
#    m_channelIndex
#
# Define how the voltage will be stepped up:
#
#    m_firstVoltage
#    m_lastVoltage
#    m_deltaVoltage
#
#

import sys
import os
import io
import time
import types
import traceback

import clientCommon

from datetime import date

class StepUpChannel() :

    m_status = ""
    m_flagStopScript = False
    m_timeStampWriteToFile = 0.0
    m_iCSClient = 0
    m_iCSConnection = 0
    m_csvFile = 0

    ## the location of the icsClientPython_3 must be specified below
    m_pythonModulePath = ""

    ## This has to be adjusted : 
    ##      defines the line index
    m_lineIndex = 0

    ## This has to be adjusted : 
    ##      defines the module index
    m_moduleAddress = 0

    ## This has to be adjusted : 
    ##      defines the channel index
    m_channelIndex = 0

    ## adjust login and password to allow a connection to the iCSservice
    m_login = "demo"
    m_password = "demo"

    ## defines how and where the results are saved
    ##      <creation_time_stamp> will be replaced
    m_fileSavePath = "data_step_up_<creation_time_stamp>.csv"

    ## defines the number of measurements performed for each step
    m_numberOfMeasurements = 5

    ## defines the voltage steps
    m_firstVoltage = 100.0
    m_lastVoltage = 1000.0
    m_deltaVoltage = 100.0
    m_currentVoltage = 0.0

    ## defines the maximum allowed current
    ## (warning) this means no protection to your hardware. To protect your hardware, please define a trip current.
    m_maximumCurrent = 1.0e-3

    ## defines a file where information and errors are logged to
    m_logFilePath = "debug.txt"

    ## debug, standard or none
    m_logFileLevel = "debug"

    ## internal timestamp used for stepping up channel in regular intervals
    m_delayFirstMeasurement = 4.0
    m_delayNextMeasurement = 2.0
    m_delayTimestamp = 0

    ## internal status used for stepping up channel in regular intervals
    # 0 : starting
    # 1 : ramping up to new voltage
    # 2 : delay, waiting for voltage to stabilize
    # 3 : done => exit
    # 4 ... 4 + n : perform n measurements
    m_stepStatus = 0

    def __init__(self):
        self.m_status = ""

    def checkStatusConnectionFailed(self):
        if self.m_status == "connection failed":
            return True
        return False

    def checkLogFileDebugModeEnabled(self):
        if self.m_logFileLevel == "debug":
            return True
        return False

    def checkLogFileStandardModeEnabled(self):
        if self.m_logFileLevel == "standard":
            return True
        return False

    def logWithLevel(self, level, msg):
        if self.m_logFilePath != "":
            try :
                logFile = open(self.m_logFilePath, "a")
                logFile.write("# {0} {1} : {2}".format(level, time.asctime(), msg))
                logFile.write("\n")
                logFile.close()
            except Exception as exc:
                ## print traceback
                exc_type, exc_value, exc_traceback = sys.exc_info()
                lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
                print("exception caught in StepUpChannel::logWithLevel()")
                for line in lines:
                    print(line.strip())

    def logInfo(self, msg):
        if self.checkLogFileDebugModeEnabled() or self.checkLogFileStandardModeEnabled():
            self.logWithLevel("info", msg)

    def logError(self, msg):
        if self.checkLogFileDebugModeEnabled() or self.checkLogFileStandardModeEnabled():
            self.logWithLevel("error", msg)

    def logDebug(self, msg):
        if self.checkLogFileDebugModeEnabled():
            self.logWithLevel("debug", msg)

    ## as soon as this script is launched a connection to the iCS is established
    ##      In addition to the standard connection parameters the session id "sessionIdSupervisor" that was passed as an argument to the script is also required.
    ##      This makes sure that we always know how the scrpit is supervised.
    def establishScriptConnection(self, connectionParameters, sessionIdSupervisor):
        self.logInfo("Script name == {0}".format(clientCommon.getScriptName()))
        if not isinstance(self.m_iCSClient, types.ModuleType):
            self.m_iCSClient = clientCommon.importFromPath(self.m_pythonModulePath, "icsClientPython_3")
            if not isinstance(self.m_iCSClient, types.ModuleType):
                self.m_errorMessage = "Failed to import icsClient module."
                self.logError(self.m_errorMessage)
        if isinstance(self.m_iCSClient, types.ModuleType):
            connectionName = "iCS_step up channel"
            self.m_iCSConnection = clientCommon.establishScriptConnection(self.m_iCSClient, connectionName, connectionParameters, sessionIdSupervisor, self.m_login, self.m_password)
            if not isinstance(self.m_iCSConnection, self.m_iCSClient.connection):
                self.m_errorMessage = "Failed to connect to {0}.".format(connectionParameters)
                self.logError(self.m_errorMessage)
        if self.checkIsConnected():
            self.logInfo("Connection to {0} established with supervisor session ID {1}.".format(connectionParameters, sessionIdSupervisor))
            mySessionId = self.m_iCSConnection.getStatusSessionId()
            self.logInfo("mySessionId == {0}".format(mySessionId))
        else:
            self.logError("Failed to establish connection to {0} with supervisor session ID {1}, login \"{2}\" and password \"{3}\".".format(connectionParameters, sessionIdSupervisor, self.m_login, self.m_password))

    def checkIsConnected(self):
        if isinstance(self.m_iCSClient, types.ModuleType):
            if isinstance(self.m_iCSConnection, self.m_iCSClient.connection):
                return True
        return False

    def closeConnection(self):
        clientCommon.disconnectAll(self.m_iCSClient)
        self.m_iCSConnection = 0

    def sendRawCommand(self, json):
        if self.checkIsConnected():
            self.m_iCSConnection.rawCommand(json)
            return True
        return False

    def establishConnection(self, connectionParameters, sessionIdSupervisor):
        ## check if connection is already OK
        if self.checkIsConnected():
            return True
        ## previous attempt failed
        if self.checkStatusConnectionFailed():
            return False
        ## attempt to connect
        rc = self.establishScriptConnection(connectionParameters, sessionIdSupervisor)
        if self.checkIsConnected():
            self.m_status = "connection established"
            return True
        self.m_status = "connection failed"
        return False

    ## generates a message that will be sent to the script supervisor.
    def generateJsonStringWithPayload(self, payload):
        json = "{{\"i\":\"<session_id>\",\"t\":\"script\",\"c\":{{\"e\": \"scriptData\",\"d\":{0},\"n\":\"<script_file_name>\",\"i\":\"<session_id_script_supervisor>\"}}}}".format(payload)
        return json

    ## processes the messages received from iCS
    def processNextMessage(self, icsMsg):
        rc = False

        if isinstance(icsMsg, self.m_iCSClient.dataFrame):
            ## handle the message appropriately
            # self.logDebug("processing message {0}".format(msg.m_icsMsg))
            if icsMsg.item == "script.stop":
                self.m_flagStopScript = True
                rc = True
            if icsMsg.item == "script.status":
                payload = "{{\"s\":\"{0}\"}}".format(self.m_status)
                json = self.generateJsonStringWithPayload(payload)
                self.sendRawCommand(json)
                self.logDebug("Script status response == {0}.".format(json))
                return True

        return rc

    def getCurrentTimeStamp(self):
        ts = int(round(time.time() * 1000))
        floatTime = float(ts)
        floatTime = floatTime / 1000.0
        return floatTime

    def getColSeparator(self):
        return ";"

    def findModule(self, line, moduleAddress):
        if self.checkIsConnected():
            allModules = self.m_iCSConnection.getModules()
            # print("allModules == {0}".format(allModules))
            for module in allModules:
                if module.address == moduleAddress:
                    if module.line == line: 
                        # print("   module found {0}".format(module))
                        return module
        return 0

    def findChannel(self, line, moduleAddress, channelIndex):
        module = self.findModule(line, moduleAddress)
        if not isinstance(module, int):
            if channelIndex < len(module.channels):
                # print("   channel found {0}".format(module.channels[channelIndex]))
                return module.channels[channelIndex]
            # print("   channel not found {0}".format(channelIndex))
            return 0
        # print("   module not found {0}.{1}".format(line, moduleAddress))
        return 0


    ## get measured values and write them to csv file
    ##      in regular time intervals
    def writeCsvFile(self, ts, channel):
        if isinstance(self.m_csvFile, io.IOBase):
            self.m_csvFile.write("{0}".format(ts))
            self.m_csvFile.write(self.getColSeparator())
            self.m_csvFile.write("{0:.5}".format(channel.getStatusVoltageMeasure()))
            self.m_csvFile.write(self.getColSeparator())
            self.m_csvFile.write("{0:.5}".format(channel.getStatusCurrentMeasure() * 1.0e6))
            self.m_csvFile.write("\n")
            self.m_csvFile.flush()

    def stepUpChannel(self):
        channel = self.findChannel(self.m_lineIndex, self.m_moduleAddress, self.m_channelIndex)
        if isinstance(channel, int):
            self.logDebug("The channel {0}.{1}.{2} was not found.".format(self.m_lineIndex, self.m_moduleAddress, self.m_channelIndex))
            self.m_flagStopScript = True
        else:
            print("m_stepStatus == {0}, m_currentVoltage == {1}".format(self.m_stepStatus, self.m_currentVoltage))
            if self.m_stepStatus == 0:
                ## STARTING
                self.m_currentVoltage = self.m_firstVoltage
                channel.setControlVoltageSet(self.m_currentVoltage)
                ## clear status flags
                channel.setControlClearAll(1)
                ## switch channel on
                channel.setControlOn(1)
                self.m_stepStatus = 1
            elif self.m_stepStatus >= 4 + self.m_numberOfMeasurements - 1:
                ## NEXT STEP
                self.m_currentVoltage = self.m_currentVoltage + self.m_deltaVoltage
                if self.m_currentVoltage > self.m_lastVoltage:
                    ## DONE, SWITCH OFF
                    channel.setControlOn(0)
                    self.m_stepStatus = 3
                    self.m_flagStopScript = True
                else:
                    channel.setControlVoltageSet(self.m_currentVoltage)
                    self.m_stepStatus = 1
            elif self.m_stepStatus == 1:
                ## RAMPING UP
                flagRamping = channel.getStatusRamping()
                flagEndOfRamp = channel.getEventEndOfRamp()
                flagConstantVoltage = channel.getStatusConstantVoltage()
                if not flagRamping and flagEndOfRamp and flagConstantVoltage:
                    # print("channel {0} has reached constant voltage".format(channel))
                    self.m_stepStatus = 2
                    self.m_delayTimestamp = self.getCurrentTimeStamp()
            elif self.m_stepStatus == 2:
                ## DELAY MEASUREMENTS
                ts = self.getCurrentTimeStamp()
                if self.m_delayTimestamp + self.m_delayFirstMeasurement < ts:
                    self.m_delayTimestamp = ts
                    self.m_stepStatus = 4
                    self.writeCsvFile(ts, channel)
                    measCurrent = channel.getStatusCurrentMeasure()
                    if measCurrent > self.m_maximumCurrent:
                        ## DONE, SWITCH OFF
                        self.logDebug("The maximum current of {0} was exceeded (measured : {1}).".format(self.m_maximumCurrent, measCurrent))
                        channel.setControlOn(0)
                        self.m_stepStatus = 3
                        self.m_flagStopScript = True
            elif self.m_stepStatus >= 4:
                ## NEXT MEASUREMENT
                ts = self.getCurrentTimeStamp()
                if self.m_delayTimestamp + self.m_delayNextMeasurement < ts:
                    self.m_delayTimestamp = ts
                    self.m_stepStatus = self.m_stepStatus + 1
                    self.writeCsvFile(ts, channel)
                    measCurrent = channel.getStatusCurrentMeasure()
                    if measCurrent > self.m_maximumCurrent:
                        ## DONE, SWITCH OFF
                        self.logDebug("The maximum current of {0} was exceeded (measured : {1}).".format(self.m_maximumCurrent, measCurrent))
                        channel.setControlOn(0)
                        self.m_stepStatus = 3
                        self.m_flagStopScript = True


    ## this is 1 step in the main loop of the Python script
    def singleStep(self):

        ## catch exceptions
        try :

            if self.checkIsConnected():
                ## get a message from the iCS (iCSservice or user interface)
                icsMsg = self.m_iCSConnection.getNextPassThroughMessage()

                ## process messages passed from the user interface of iCS
                ##      until the "script.stop" command is issued
                self.processNextMessage(icsMsg)

            if not self.m_flagStopScript:
                ## get measurements and write data to CSV file
                self.stepUpChannel()

                ## this makes sure ressources can be used by other processes.
                time.sleep(0.5)

        except Exception as exc:
            ## print traceback
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            self.logError("software error : exception caught in StepUpChannel::singleStep()")
            for line in lines:
                self.logDebug(line.strip())
            self.m_status = "software error"
            self.m_flagStopScript = True

    ## this is the main loop of the Python script
    ##
    ##      it runs until the "script.stop" command is issued
    def runMainLoop(self, connectionParameters, sessionIdSupervisor, configFileName):

        ## clear log file
        if self.checkLogFileDebugModeEnabled() or self.checkLogFileStandardModeEnabled():
            ## disable generation of log file if the directory doesn't exist
            if self.m_logFilePath != "":
                self.m_logFilePath = os.path.abspath(self.m_logFilePath)
                parentPath = os.path.dirname(self.m_logFilePath)
                if not os.path.exists(parentPath) :
                    print("ERROR : the parent directory of the log file file {0} doesn't exist.".format(self.m_logFilePath))
                    print("ERROR : writing to log file is disabled.")
                    self.m_logFilePath  = ""
            if self.m_logFilePath != "":
                ## always catch exceptions to make sure that the script doesn't close unexpectedly
                try :
                    logFile = open(self.m_logFilePath, "w")
                    logFile.write("# Log File created for iCSPythonStepUpChannel.py on {0}".format(time.asctime()))
                    logFile.write("\n")
                    logFile.close()
                except Exception as exc:
                    ## print traceback
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
                    print("exception caught in StepUpChannel::runMainLoop()")
                    for line in lines:
                        print(line.strip())

        ## establish connection
        if self.establishConnection(connectionParameters, sessionIdSupervisor):

            ## open CSV file and create column header
            try :
                ## adjust the name of the created CSV file
                now = time.time()
                timeStampStr = time.strftime("%Y_%m_%d__%H_%M")
                self.m_fileSavePath = self.m_fileSavePath.replace("<creation_time_stamp>", timeStampStr);
                self.m_fileSavePath = os.path.abspath(self.m_fileSavePath)

                self.logInfo("writing CSV file {0}".format(self.m_fileSavePath))

                ## disable generation of csv file if the directory doesn't exist
                if self.m_fileSavePath != "":
                    parentPath = os.path.dirname(self.m_fileSavePath)
                    if not os.path.exists(parentPath) :
                        self.m_fileSavePath  = ""
                        self.logError("the parent directory of the CSV file {0} doesn't exist.".format(self.m_fileSavePath))
                        self.logError("writing to CSV file is disabled.")

                if self.m_fileSavePath != "":
                    self.m_csvFile = open(self.m_fileSavePath, "w")
                    self.m_csvFile.write("# CSV File created for iCSPythonStepUpChannel.py on {0}".format(time.asctime()))
                    self.m_csvFile.write("\n")

                    self.m_csvFile.write("\"time [s]\"")
                    channel = self.findChannel(self.m_lineIndex, self.m_moduleAddress, self.m_channelIndex)
                    if isinstance(channel, int):
                        self.logDebug("The channel {0}.{1}.{2} was not found.".format(self.m_lineIndex, self.m_moduleAddress, self.m_channelIndex))
                        self.m_flagStopScript = True
                    else:
                        self.m_csvFile.write(self.getColSeparator())
                        self.m_csvFile.write("\"Channel.{0}.Vmeas [V]\"".format(channel))
                        self.m_csvFile.write(self.getColSeparator())
                        self.m_csvFile.write("\"Channel.{0}.Imeas [\u00b5A]\"".format(channel))
                    self.m_csvFile.write("\n")
                    self.m_csvFile.flush()

            except Exception as exc:
                ## print traceback
                exc_type, exc_value, exc_traceback = sys.exc_info()
                lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
                print("exception caught in StepUpChannel::runMainLoop()")
                for line in lines:
                    print(line.strip())

            self.logInfo("Entering execution loop.")

            # now the main loop can be executed
            self.m_flagStopScript = False
            while not self.m_flagStopScript:
                self.singleStep()


            if isinstance(self.m_csvFile, io.IOBase):
                try :
                    self.m_csvFile.close()
                except Exception as exc:
                    print("exception caught in StepUpChannel::runMainLoop()")


            self.logInfo("Execution loop left.")

        self.closeConnection()
        self.logInfo("Script stopped.")






# the connection parameters can be given on the command line
connectionParameters = "ws://ics.iseg-hv.com:8080"
# connectionParameters = "ws://ics.iseg-hv.com:8080"
# isn't required in normal operation
sessionIdSupervisor = ""
# isn't required in normal operation
configFileName = ""

for argvIndex in range(0, len(sys.argv)):
    # print("argument[{0}] == {1}".format(argvIndex, sys.argv[argvIndex]))
    if argvIndex + 1 < len(sys.argv):
        if sys.argv[argvIndex] == "-i":
            sessionIdSupervisor = sys.argv[argvIndex + 1]
        if sys.argv[argvIndex] == "-c":
            connectionParameters = sys.argv[argvIndex + 1]

app = StepUpChannel()
## this must specify the location of the icsClientPython_3 python module
app.m_pythonModulePath = "../platform/linux/64/"
if clientCommon.checkIsWindowsPlatform():
    app.m_pythonModulePath = "../bin/"
app.m_pythonModulePath = os.path.abspath(app.m_pythonModulePath)
app.runMainLoop(connectionParameters, sessionIdSupervisor, configFileName)


