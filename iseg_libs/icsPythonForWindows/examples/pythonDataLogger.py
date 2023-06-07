
#
# This example implements a data logger. Voltage and current measurements are written to a CSV file
#       in regular time intervals.
#
# The connection parameters must be given when the example is launched example:
#       python3 pythonDataLogger.py -c ws://192.168.0.25:8080
#
# It makes use of the icsClientPython_3 Python library.
#
# Some of the parameters below might have to be adjusted.
#

import sys
import os
import io
import time
import types
import traceback

import clientCommon

from datetime import date

class CsvDataLogger() :

    m_status = ""
    m_flagStopScript = False
    m_timeStampWriteToFile = 0.0
    m_iCSClient = 0
    m_iCSConnection = 0
    m_csvFile = 0

    ## the location of the icsClientPython_3 must be specified below
    m_pythonModulePath = ""

    ## adjust login and password to allow a connection to the iCSservice
    m_login = "demo"
    m_password = "demo"

    ## defines how and where the results are saved
    ##      <creation_time_stamp> will be replaced
    m_fileSavePath = "data_log_<creation_time_stamp>.csv"

    ## th measured values will be written every 10 seconds
    m_timeIntervalWriteToFile = 10.0

    ## defines a file where information and errors are logged to
    m_logFilePath = "debug.txt"

    ## debug, standard or none
    m_logFileLevel = "debug"

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
                print("exception caught in CsvDataLogger::logWithLevel()")
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
            connectionName = "iCS_csv_logger"
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

    ## get measured values and write them to csv file
    ##      in regular time intervals
    def writeCsvFile(self):
        ts = self.getCurrentTimeStamp()
        ## every 500 ms : get measurements, compute resistance, control hardware according to the current recipe
        if ts >= self.m_timeStampWriteToFile + self.m_timeIntervalWriteToFile:
            self.m_timeStampWriteToFile = ts
            if isinstance(self.m_csvFile, io.IOBase):
                self.m_csvFile.write("{0}".format(ts))
                allModules = self.m_iCSConnection.getModules()
                # print("allModules == {0}".format(allModules))
                for module in allModules:
                    for channel in module.channels:
                        self.m_csvFile.write(self.getColSeparator())
                        self.m_csvFile.write("{0}".format(channel.getStatusVoltageMeasure()))
                        self.m_csvFile.write(self.getColSeparator())
                        self.m_csvFile.write("{0}".format(channel.getStatusCurrentMeasure()))
                self.m_csvFile.write("\n")
                self.m_csvFile.flush()


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
                self.writeCsvFile()

                ## this makes sure ressources can be used by other processes.
                time.sleep(0.5)

        except Exception as exc:
            ## print traceback
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            self.logError("software error : exception caught in CsvDataLogger::singleStep()")
            for line in lines:
                self.logDebug(line.strip())
            self.m_status = "software error"

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
                    logFile.write("# Log File created for iCSPythonDataLogger.py on {0}".format(time.asctime()))
                    logFile.write("\n")
                    logFile.close()
                except Exception as exc:
                    ## print traceback
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
                    print("exception caught in CsvDataLogger::runMainLoop()")
                    for line in lines:
                        print(line.strip())

        ## establish connection
        if self.establishConnection(connectionParameters, sessionIdSupervisor):

            ## open CSV file and create column header
            try :
                ## adjust the name of the created CSV file
                today = date.today()
                timeStampStr = today.strftime("%Y%m%d")
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
                    self.m_csvFile.write("# CSV File created for iCSPythonDataLogger.py on {0}".format(time.asctime()))
                    self.m_csvFile.write("\n")

                    self.m_csvFile.write("\"time [s]\"")
                    allModules = self.m_iCSConnection.getModules()
                    # print("allModules == {0}".format(allModules))
                    for module in allModules:
                        for channel in module.channels:
                            stat = channel.getStatusRunningState()
                            self.m_csvFile.write(self.getColSeparator())
                            self.m_csvFile.write("\"Channel.{0}.Vmeas [V]\"".format(channel))
                            self.m_csvFile.write(self.getColSeparator())
                            self.m_csvFile.write("\"Channel.{0}.Imeas [A]\"".format(channel))
                    self.m_csvFile.write("\n")
                    self.m_csvFile.flush()

            except Exception as exc:
                ## print traceback
                exc_type, exc_value, exc_traceback = sys.exc_info()
                lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
                print("exception caught in CsvDataLogger::runMainLoop()")
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
                    print("exception caught in CsvDataLogger::runMainLoop()")


            self.logInfo("Execution loop left.")

        self.closeConnection()
        self.logInfo("Script stopped.")






# the connection parameters can be given on the command line
#connectionParameters = "ws://localhost:8080"
connectionParameters = "ws://ics.iseg.hv.com:8080"
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

app = CsvDataLogger()
## this must specify the location of the icsClientPython_3 python module
app.m_pythonModulePath = "../platform/linux/64/"
if clientCommon.checkIsWindowsPlatform():
    app.m_pythonModulePath = "../bin/"
app.m_pythonModulePath = os.path.abspath(app.m_pythonModulePath)
app.runMainLoop(connectionParameters, sessionIdSupervisor, configFileName)


