import logging
import time


def print_channel_info(ics_client, channel):
    # TODO move alle these infos into other method
    print(channel.module)
    print(channel)
    status_v_nominal = channel.getStatusVoltageNominal()
    control_v_set = channel.getControlVoltageSet
    status_v_measure = channel.getStatusVoltageMeasure()
    status_c_nominal = channel.getStatusCurrentNominal()
    control_c_set = channel.getControlCurrentSet()
    status_c_measure = channel.getStatusCurrentMeasure()
    status_v_limit_exceed = channel.getStatusVoltageLimitExceeded()
    status_c_limit_exceed = channel.getStatusCurrentLimitExceeded()
    status_current_trip = channel.getStatusTrip()
    status_on = channel.getStatusOn()
    status_emergency = channel.getStatusEmergency()
    setup_delayed_trip_action = channel.getSetupDelayedTripAction()
    setup_delayed_trip_time = channel.getSetupDelayedTripTime()
    print(
        f"""
        status_v_nominal {status_v_nominal}
        control_v_set {control_v_set}
        status_v_measure {status_v_measure}
        status_c_nominal {status_c_nominal}
        control_c_set {control_c_set}
        status_c_measure {status_c_measure}
        status_v_limit_exceed {status_v_limit_exceed}
        status_c_limit_exceed {status_c_limit_exceed}
        status_current_trip  {status_current_trip}
        status_on  {status_on}
        status_emergency  {status_emergency}
        setup_delayed_trip_action  {setup_delayed_trip_action}
        setup_delayed_trip_time  {setup_delayed_trip_time}
        """
    )


def print_some_info(ics_bridge):
    # Important to wait here so the crate gets booted up or whatever
    other_crate_cmd = ics_bridge.connection.crates
    print(f"Other crate cmd: {other_crate_cmd}")

    all_crates = ics_bridge.connection.getCrates()
    print(f"All crates {all_crates}.")

    # or_this = all_crates[0].crates
    # print(f"or this?: {or_this}")

    all_modules = ics_bridge.connection.getModules()
    logging.info(f"All modules {all_modules}.")

    all_channels = []
    for mod in all_modules:
        for i, channel in enumerate(mod.channels):
            all_channels.append(channel)
    logging.info(f"All channels {all_channels}.")

    # time to fill the cache from iCSservice
    time.sleep(5)

    for mod in all_modules:
        logging.info(
            f""" Module {mod.address}
                     Firmwarename: {mod.getStatusFirmwareName()}
                     Seriennummer: {mod.getStatusSerialNumber()}
                     Release: {mod.getStatusFirmwareRelease()}
                     Temperatur: {mod.getStatusTemperature()}
                     """
        )

    for channel in all_channels:
        print_channel_info(channel)
