class ICSModuleAbstraction:
    """
    class to make the members of the ics_api.channel visible
    TODO currently only used as type hinting class make its so ics_client uses this?
    see stackoverflow discuccsion for more:
    https://stackoverflow.com/questions/1443129/completely-wrap-an-object-in-python/31437314
    there seem to be edge cases? with __getattr__and __slots__. see link for that
    """

    def __init__(self, channel_object):
        self.__channel_object = channel_object
        # self.__class__ = type(
        #     channel_object.__class__.__name__,
        #     (self.__class__, channel_object.__class__),
        #     {},
        # )
        # self.__dict__ = channel_object.__dict__

        if hasattr(self.__channel_object, "__dict__"):
            self.__dict__ = channel_object.__dict__

        if hasattr(self.__channel_object, "connection"):
            self.connection = self.__channel_object.connection

        if hasattr(self.__channel_object, "index"):
            self.index = self.__channel_object.index

        if hasattr(self.__channel_object, "channels"):
            self.module = self.__channel_object.channels

    def getControlAdjustment(self, *args):
        return self.__channel_object.getControlAdjustment(*args)

    def getControlCurrentRampspeed(self, percent_inom_per_sec):
        """
        gets the Current(I) Ramp speed in Percent of Inom per seccond
        """
        return self.__channel_object.getControlCurrentRampspeed(percent_inom_per_sec)

    def getControlKill(self, *args):
        return self.__channel_object.getControlKill(*args)

    def getControlModuleChannelEventMask(self, *args):
        return self.__channel_object.getControlModuleChannelEventMask(*args)

    def getControlModuleEventMask(self, *args):
        return self.__channel_object.getControlModuleEventMask(*args)

    def getControlUserHardwareCheck(self, *args):
        return self.__channel_object.getControlUserHardwareCheck(*args)

    def getControlVoltageRampspeed(self, percent_vnom_per_sec):
        """
        get the Voltage(V) Ramp speed in Percent of Vnom per second
        """
        return self.__channel_object.getControlVoltageRampspeed(percent_vnom_per_sec)

    def getErrorInterlockOut(self, *args):
        return self.__channel_object.getErrorInterlockOut(*args)

    def getErrorNeedService(self, *args):
        return self.__channel_object.getErrorNeedService(*args)

    def getErrorNeedUserHardwareCheck(self, *args):
        return self.__channel_object.getErrorNeedUserHardwareCheck(*args)

    def getErrorSafetyLoopWasOpened(self, *args):
        return self.__channel_object.getErrorSafetyLoopWasOpened(*args)

    def getErrorSupplyNotGood(self, *args):
        return self.__channel_object.getErrorSupplyNotGood(*args)

    def getErrorTemperatureNotGood(self, *args):
        return self.__channel_object.getErrorTemperatureNotGood(*args)

    def getEventInterlockOut(self, *args):
        return self.__channel_object.getEventInterlockOut(*args)

    def getEventSafetyLoopWasOpened(self, *args):
        return self.__channel_object.getEventSafetyLoopWasOpened(*args)

    def getEventSupplyNotGood(self, *args):
        return self.__channel_object.getEventSupplyNotGood(*args)

    def getEventTemperatureNotGood(self, *args):
        return self.__channel_object.getEventTemperatureNotGood(*args)

    def getSetupAdcSampleRate(self, *args):
        return self.__channel_object.getSetupAdcSampleRate(*args)

    def getSetupDigitalFilter(self, *args):
        return self.__channel_object.getSetupDigitalFilter(*args)

    def getStatusAdjustment(self, *args):
        return self.__channel_object.getStatusAdjustment(*args)

    def getStatusErrorCounter(self, *args):
        return self.__channel_object.getStatusErrorCounter(*args)

    def getStatusEventCounter(self, *args):
        return self.__channel_object.getStatusEventCounter(*args)

    def getStatusFirmwareName(self, *args):
        return self.__channel_object.getStatusFirmwareName(*args)

    def getStatusFirmwareRelease(self, *args):
        return self.__channel_object.getStatusFirmwareRelease(*args)

    def getStatusInterlockOut(self, *args):
        return self.__channel_object.getStatusInterlockOut(*args)

    def getStatusIsAlive(self, *args):
        return self.__channel_object.getStatusIsAlive(*args)

    def getStatusNeedService(self, *args):
        return self.__channel_object.getStatusNeedService(*args)

    def getStatusRunningState(self, *args):
        return self.__channel_object.getStatusRunningState(*args)

    def getStatusSafetyLoopClosed(self, *args):
        return self.__channel_object.getStatusSafetyLoopClosed(*args)

    def getStatusSerialNumber(self, *args):
        return self.__channel_object.getStatusSerialNumber(*args)

    def getStatusSupplyGood(self, *args):
        return self.__channel_object.getStatusSupplyGood(*args)

    def getStatusTemperature(self, *args):
        return self.__channel_object.getStatusTemperature(*args)

    def getStatusTemperatureGood(self, *args):
        return self.__channel_object.getStatusTemperatureGood(*args)

    def setControlAdjustment(self, *args):
        return self.__channel_object.setControlAdjustment(*args)

    def setControlClearAll(self, *args):
        return self.__channel_object.setControlClearAll(*args)

    def setControlClearErrors(self, *args):
        return self.__channel_object.setControlClearErrors(*args)

    def setControlClearEvents(self, *args):
        return self.__channel_object.setControlClearEvents(*args)

    def setControlCurrentRampspeed(self, percent_inom_per_sec):
        """
        set the Current(I) Ramp speed in Percent of Inom per seccond
        """
        return self.__channel_object.setControlCurrentRampspeed(percent_inom_per_sec)

    def setControlInstallFirmware(self, *args):
        return self.__channel_object.setControlInstallFirmware(*args)

    def setControlKill(self, *args):
        return self.__channel_object.setControlKill(*args)

    def setControlModuleChannelEventMask(self, *args):
        return self.__channel_object.setControlModuleChannelEventMask(*args)

    def setControlModuleEventMask(self, *args):
        return self.__channel_object.setControlModuleEventMask(*args)

    def setControlUserHardwareCheck(self, *args):
        return self.__channel_object.setControlUserHardwareCheck(*args)

    def setControlVoltageRampspeed(self, percent_vnom_per_se):
        """
        set the Voltage(V) Ramp speed in Percent of Vnom per second
        """
        return self.__channel_object.setControlVoltageRampspeed(percent_vnom_per_se)

    def setSetupAdcSampleRate(self, *args):
        return self.__channel_object.setSetupAdcSampleRate(*args)

    def setSetupDigitalFilter(self, *args):
        return self.__channel_object.setSetupDigitalFilter(*args)
