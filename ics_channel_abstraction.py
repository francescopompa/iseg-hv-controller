class ICSChannelAbstraction:
    """
    class to make the members of the ics_api.channel visible
    TODO currently only used as type hinting class make its so ics_client uses this?
    """

    def __init__(self, channel_object):
        self.__channel_object = channel_object

        self.connection = self.__channel_object.connection

        self.index = self.__channel_object.index

        self.line = self.__channel_object.line

        self.module = self.__channel_object.module

    def __delattr__(self, *args):
        return self.__channel_object.__delattr__(*args)

    def __dir__(self, *args):
        return self.__channel_object.__dir__(*args)

    def __doc__(self, *args):
        return self.__channel_object.__doc__(*args)

    def __eq__(self, *args):
        return self.__channel_object.__eq__(*args)

    def __format__(self, *args):
        return self.__channel_object.__format__(*args)

    def __ge__(self, *args):
        return self.__channel_object.__ge__(*args)

    def __getattribute__(self, *args):
        return self.__channel_object.__getattribute__(*args)

    def __gt__(self, *args):
        return self.__channel_object.__gt__(*args)

    def __hash__(self, *args):
        return self.__channel_object.__hash__(*args)

    def __init_subclass__(self, *args):
        return self.__channel_object.__init_subclass__(*args)

    def __le__(self, *args):
        return self.__channel_object.__le__(*args)

    def __lt__(self, *args):
        return self.__channel_object.__lt__(*args)

    def __module__(self, *args):
        return self.__channel_object.__module__(*args)

    def __ne__(self, *args):
        return self.__channel_object.__ne__(*args)

    def __new__(self, *args):
        return self.__channel_object.__new__(*args)

    def __reduce__(self, *args):
        return self.__channel_object.__reduce__(*args)

    def __reduce_ex__(self, *args):
        return self.__channel_object.__reduce_ex__(*args)

    def __repr__(self, *args):
        return self.__channel_object.__repr__(*args)

    def __setattr__(self, *args):
        return self.__channel_object.__setattr__(*args)

    def __sizeof__(self, *args):
        return self.__channel_object.__sizeof__(*args)

    def __str__(self, *args):
        return self.__channel_object.__str__(*args)

    def __subclasshook__(self, *args):
        return self.__channel_object.__subclasshook__(*args)

    def getControlChannelEventMask(self, *args):
        return self.__channel_object.getControlChannelEventMask(*args)

    def getControlCurrentBounds(self, *args):
        return self.__channel_object.getControlCurrentBounds(*args)

    def getControlCurrentRampspeedDown(self, *args):
        return self.__channel_object.getControlCurrentRampspeedDown(*args)

    def getControlCurrentRampspeedUp(self, *args):
        return self.__channel_object.getControlCurrentRampspeedUp(*args)

    def getControlCurrentSet(self, *args):
        return self.__channel_object.getControlCurrentSet(*args)

    def getControlEmergency(self, *args):
        return self.__channel_object.getControlEmergency(*args)

    def getControlOn(self, *args):
        return self.__channel_object.getControlOn(*args)

    def getControlVctCoefficient(self, *args):
        return self.__channel_object.getControlVctCoefficient(*args)

    def getControlVoltageBounds(self, *args):
        return self.__channel_object.getControlVoltageBounds(*args)

    def getControlVoltageRampspeedDown(self, *args):
        return self.__channel_object.getControlVoltageRampspeedDown(*args)

    def getControlVoltageRampspeedUp(self, *args):
        return self.__channel_object.getControlVoltageRampspeedUp(*args)

    def getControlVoltageSet(self, *args):
        return self.__channel_object.getControlVoltageSet(*args)

    def getErrorArc(self, *args):
        return self.__channel_object.getErrorArc(*args)

    def getErrorCurrentBoundExceeded(self, *args):
        return self.__channel_object.getErrorCurrentBoundExceeded(*args)

    def getErrorCurrentLimitExceeded(self, *args):
        return self.__channel_object.getErrorCurrentLimitExceeded(*args)

    def getErrorEmergency(self, *args):
        return self.__channel_object.getErrorEmergency(*args)

    def getErrorExternalInhibitActive(self, *args):
        return self.__channel_object.getErrorExternalInhibitActive(*args)

    def getErrorTrip(self, *args):
        return self.__channel_object.getErrorTrip(*args)

    def getErrorVoltageBoundExceeded(self, *args):
        return self.__channel_object.getErrorVoltageBoundExceeded(*args)

    def getErrorVoltageLimitExceeded(self, *args):
        return self.__channel_object.getErrorVoltageLimitExceeded(*args)

    def getEventArc(self, *args):
        return self.__channel_object.getEventArc(*args)

    def getEventArcError(self, *args):
        return self.__channel_object.getEventArcError(*args)

    def getEventConstantCurrent(self, *args):
        return self.__channel_object.getEventConstantCurrent(*args)

    def getEventConstantPower(self, *args):
        return self.__channel_object.getEventConstantPower(*args)

    def getEventConstantVoltage(self, *args):
        return self.__channel_object.getEventConstantVoltage(*args)

    def getEventCurrentBoundExceeded(self, *args):
        return self.__channel_object.getEventCurrentBoundExceeded(*args)

    def getEventCurrentLimitExceeded(self, *args):
        return self.__channel_object.getEventCurrentLimitExceeded(*args)

    def getEventCurrentRampDown(self, *args):
        return self.__channel_object.getEventCurrentRampDown(*args)

    def getEventCurrentRampUp(self, *args):
        return self.__channel_object.getEventCurrentRampUp(*args)

    def getEventEmergency(self, *args):
        return self.__channel_object.getEventEmergency(*args)

    def getEventEndOfCurrentRamp(self, *args):
        return self.__channel_object.getEventEndOfCurrentRamp(*args)

    def getEventEndOfRamp(self, *args):
        return self.__channel_object.getEventEndOfRamp(*args)

    def getEventExternalInhibitActive(self, *args):
        return self.__channel_object.getEventExternalInhibitActive(*args)

    def getEventInputError(self, *args):
        return self.__channel_object.getEventInputError(*args)

    def getEventMaxPower(self, *args):
        return self.__channel_object.getEventMaxPower(*args)

    def getEventTrip(self, *args):
        return self.__channel_object.getEventTrip(*args)

    def getEventVoltageBottom(self, *args):
        return self.__channel_object.getEventVoltageBottom(*args)

    def getEventVoltageBoundExceeded(self, *args):
        return self.__channel_object.getEventVoltageBoundExceeded(*args)

    def getEventVoltageBoundLower(self, *args):
        return self.__channel_object.getEventVoltageBoundLower(*args)

    def getEventVoltageBoundUpper(self, *args):
        return self.__channel_object.getEventVoltageBoundUpper(*args)

    def getEventVoltageLimitExceeded(self, *args):
        return self.__channel_object.getEventVoltageLimitExceeded(*args)

    def getEventVoltageRampDown(self, *args):
        return self.__channel_object.getEventVoltageRampDown(*args)

    def getEventVoltageRampUp(self, *args):
        return self.__channel_object.getEventVoltageRampUp(*args)

    def getSetupDelayedTripAction(self, *args):
        return self.__channel_object.getSetupDelayedTripAction(*args)

    def getSetupDelayedTripTime(self, *args):
        return self.__channel_object.getSetupDelayedTripTime(*args)

    def getSetupExternalInhibitAction(self, *args):
        return self.__channel_object.getSetupExternalInhibitAction(*args)

    def getSetupOutputMode(self, *args):
        return self.__channel_object.getSetupOutputMode(*args)

    def getSetupOutputPolarity(self, *args):
        return self.__channel_object.getSetupOutputPolarity(*args)

    def getSetupResistanceExternal(self, *args):
        return self.__channel_object.getSetupResistanceExternal(*args)

    def getSetupVoltageBottom(self, *args):
        return self.__channel_object.getSetupVoltageBottom(*args)

    def getSetupVoltageRampPriority(self, *args):
        return self.__channel_object.getSetupVoltageRampPriority(*args)

    def getStatusArc(self, *args):
        return self.__channel_object.getStatusArc(*args)

    def getStatusConstantCurrent(self, *args):
        return self.__channel_object.getStatusConstantCurrent(*args)

    def getStatusConstantPower(self, *args):
        return self.__channel_object.getStatusConstantPower(*args)

    def getStatusConstantVoltage(self, *args):
        return self.__channel_object.getStatusConstantVoltage(*args)

    def getStatusCurrentBoundExceeded(self, *args):
        return self.__channel_object.getStatusCurrentBoundExceeded(*args)

    def getStatusCurrentLimit(self, *args):
        return self.__channel_object.getStatusCurrentLimit(*args)

    def getStatusCurrentLimitExceeded(self, *args):
        return self.__channel_object.getStatusCurrentLimitExceeded(*args)

    def getStatusCurrentMeasure(self, *args):
        return self.__channel_object.getStatusCurrentMeasure(*args)

    def getStatusCurrentMeasureWithTimestamp(self, *args):
        return self.__channel_object.getStatusCurrentMeasureWithTimestamp(*args)

    def getStatusCurrentMode(self, *args):
        return self.__channel_object.getStatusCurrentMode(*args)

    def getStatusCurrentModeList(self, *args):
        return self.__channel_object.getStatusCurrentModeList(*args)

    def getStatusCurrentNominal(self, *args):
        return self.__channel_object.getStatusCurrentNominal(*args)

    def getStatusCurrentRampDown(self, *args):
        return self.__channel_object.getStatusCurrentRampDown(*args)

    def getStatusCurrentRampUp(self, *args):
        return self.__channel_object.getStatusCurrentRampUp(*args)

    def getStatusCurrentRamping(self, *args):
        return self.__channel_object.getStatusCurrentRamping(*args)

    def getStatusCurrentRampspeedMax(self, *args):
        return self.__channel_object.getStatusCurrentRampspeedMax(*args)

    def getStatusCurrentRampspeedMin(self, *args):
        return self.__channel_object.getStatusCurrentRampspeedMin(*args)

    def getStatusEmergency(self, *args):
        return self.__channel_object.getStatusEmergency(*args)

    def getStatusErrorCounter(self, *args):
        return self.__channel_object.getStatusErrorCounter(*args)

    def getStatusEventCounter(self, *args):
        return self.__channel_object.getStatusEventCounter(*args)

    def getStatusExternalInhibitActive(self, *args):
        return self.__channel_object.getStatusExternalInhibitActive(*args)

    def getStatusLowCurrentRange(self, *args):
        return self.__channel_object.getStatusLowCurrentRange(*args)

    def getStatusMaxPower(self, *args):
        return self.__channel_object.getStatusMaxPower(*args)

    def getStatusOn(self, *args):
        return self.__channel_object.getStatusOn(*args)

    def getStatusRamping(self, *args):
        return self.__channel_object.getStatusRamping(*args)

    def getStatusRunningState(self, *args):
        return self.__channel_object.getStatusRunningState(*args)

    def getStatusTemperatureExternal(self, *args):
        return self.__channel_object.getStatusTemperatureExternal(*args)

    def getStatusTrip(self, *args):
        return self.__channel_object.getStatusTrip(*args)

    def getStatusVoltageBoundExceeded(self, *args):
        return self.__channel_object.getStatusVoltageBoundExceeded(*args)

    def getStatusVoltageBoundLower(self, *args):
        return self.__channel_object.getStatusVoltageBoundLower(*args)

    def getStatusVoltageBoundUpper(self, *args):
        return self.__channel_object.getStatusVoltageBoundUpper(*args)

    def getStatusVoltageLimit(self, *args):
        return self.__channel_object.getStatusVoltageLimit(*args)

    def getStatusVoltageLimitExceeded(self, *args):
        return self.__channel_object.getStatusVoltageLimitExceeded(*args)

    def getStatusVoltageMeasure(self, *args):
        return self.__channel_object.getStatusVoltageMeasure(*args)

    def getStatusVoltageMeasureWithTimestamp(self, *args):
        return self.__channel_object.getStatusVoltageMeasureWithTimestamp(*args)

    def getStatusVoltageMode(self, *args):
        return self.__channel_object.getStatusVoltageMode(*args)

    def getStatusVoltageModeList(self, *args):
        return self.__channel_object.getStatusVoltageModeList(*args)

    def getStatusVoltageNominal(self, *args):
        return self.__channel_object.getStatusVoltageNominal(*args)

    def getStatusVoltageRampDown(self, *args):
        return self.__channel_object.getStatusVoltageRampDown(*args)

    def getStatusVoltageRampUp(self, *args):
        return self.__channel_object.getStatusVoltageRampUp(*args)

    def getStatusVoltageRamping(self, *args):
        return self.__channel_object.getStatusVoltageRamping(*args)

    def getStatusVoltageRampspeedMax(self, *args):
        return self.__channel_object.getStatusVoltageRampspeedMax(*args)

    def getStatusVoltageRampspeedMin(self, *args):
        return self.__channel_object.getStatusVoltageRampspeedMin(*args)

    def setControlChannelEventMask(self, *args):
        return self.__channel_object.setControlChannelEventMask(*args)

    def setControlClearAll(self, *args):
        return self.__channel_object.setControlClearAll(*args)

    def setControlClearErrors(self, *args):
        return self.__channel_object.setControlClearErrors(*args)

    def setControlClearEvents(self, *args):
        return self.__channel_object.setControlClearEvents(*args)

    def setControlCurrentBounds(self, *args):
        return self.__channel_object.setControlCurrentBounds(*args)

    def setControlCurrentRampspeedDown(self, *args):
        return self.__channel_object.setControlCurrentRampspeedDown(*args)

    def setControlCurrentRampspeedUp(self, *args):
        return self.__channel_object.setControlCurrentRampspeedUp(*args)

    def setControlCurrentSet(self, trip_current_in_amp: float):
        return self.__channel_object.setControlCurrentSet(trip_current_in_amp)

    def setControlEmergency(self, *args):
        return self.__channel_object.setControlEmergency(*args)

    def setControlOn(self, on_off: bool):
        return self.__channel_object.setControlOn(on_off)

    def setControlVctCoefficient(self, *args):
        return self.__channel_object.setControlVctCoefficient(*args)

    def setControlVoltageBounds(self, *args):
        return self.__channel_object.setControlVoltageBounds(*args)

    def setControlVoltageRampspeedDown(self, *args):
        return self.__channel_object.setControlVoltageRampspeedDown(*args)

    def setControlVoltageRampspeedUp(self, ramp_speed_in_volts_per_sec):
        return self.__channel_object.setControlVoltageRampspeedUp(
            ramp_speed_in_volts_per_sec
        )

    def setControlVoltageSet(self, voltage_in_volt):
        return self.__channel_object.setControlVoltageSet(voltage_in_volt)

    def setSetupDelayedTripAction(self, *args):
        return self.__channel_object.setSetupDelayedTripAction(*args)

    def setSetupDelayedTripTime(self, *args):
        return self.__channel_object.setSetupDelayedTripTime(*args)

    def setSetupExternalInhibitAction(self, *args):
        return self.__channel_object.setSetupExternalInhibitAction(*args)

    def setSetupOutputMode(self, *args):
        return self.__channel_object.setSetupOutputMode(*args)

    def setSetupOutputPolarity(self, *args):
        return self.__channel_object.setSetupOutputPolarity(*args)

    def setSetupResistanceExternal(self, *args):
        return self.__channel_object.setSetupResistanceExternal(*args)

    def setSetupVoltageBottom(self, *args):
        return self.__channel_object.setSetupVoltageBottom(*args)

    def setSetupVoltageRampPriority(self, *args):
        return self.__channel_object.setSetupVoltageRampPriority(*args)

    def setStatusCurrentRampspeedMax(self, *args):
        return self.__channel_object.setStatusCurrentRampspeedMax(*args)

    def setStatusCurrentRampspeedMin(self, *args):
        return self.__channel_object.setStatusCurrentRampspeedMin(*args)

    def setStatusVoltageRampspeedMax(self, *args):
        return self.__channel_object.setStatusVoltageRampspeedMax(*args)

    def setStatusVoltageRampspeedMin(self, *args):
        return self.__channel_object.setStatusVoltageRampspeedMin(*args)
