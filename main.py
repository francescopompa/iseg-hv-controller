"""
SEE README.md
"""
import logging
import time
import json
import difflib
import ics_client


def main():
    """
    ...
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s::%(levelname)s::%(filename)s:%(funcName)s:%(lineno)d::\t%(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("hv_controller.log")],
    )
    logging.info("Started")

    server = ics_client.IcsClient(  # TODO bad name
        connection_name="ics_connection" + time.asctime(),
        connection_parameters="ws://192.168.0.10:8080",
        connection_login="admin",
        connection_password="password",
    )

    server.connect()

    # Power on CC24 crate with websocket command
    power_frame = {
        "i": "<session_id>",
        "t": "request",
        "c": [
            {
                "c": "getItem",
                "p": {
                    "p": {"l": "0", "a": "1000", "c": ""},
                    "i": "Control.power",
                    "v": "",
                    "u": "",
                },
            }
        ],
        "r": "websocket",
    }
    power_frame = json.dumps(power_frame)  # Convert to json string
    server.connection.rawCommand(power_frame)
    print(power_frame)

    # Check the result of the previous power on command
    result_cmd = {
        "i": "<session_id>",
        "t": "request",
        "c": [
            {
                "c": "setItem",
                "p": {
                    "p": {"l": "0", "a": "1000", "c": ""},
                    "i": "Control.power",
                    "v": "1",
                    "u": "",
                },
            }
        ],
        "r": "websocket",
    }
    result_cmd = json.dumps(result_cmd)
    result = server.connection.rawCommand(result_cmd)
    print(result)

    time.sleep(5)
    # Important to wait here so the crate gets booted up or whatever
    other_crate_cmd = server.connection.crates
    print(f"Other crate cmd: {other_crate_cmd}")

    all_crates = server.connection.getCrates()
    print(f"All crates {all_crates}.")

    # or_this = all_crates[0].crates
    # print(f"or this?: {or_this}")

    all_modules = server.connection.getModules()
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
    test_channel = all_channels[0]
    test_channel.setControlCurrentSet(1)
    test_channel.setControlVoltageSet(200)
    test_channel.setControlOn(1)


if __name__ == "__main__":
    # TODO make it so starting from shell without commands uses the values defined by config and with some commands sends those
    # TODO add argparse (see sphe_processor scripts project)
    main()
