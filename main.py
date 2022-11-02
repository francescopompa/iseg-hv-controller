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
        handlers=[logging.StreamHandler(), logging.FileHandler("hv_controller.log")],
    )
    logging.info("Started")

    server = ics_client.IcsClient(  # bad name
        connection_name="ics_connection" + time.asctime(),
        connection_parameters="ws://192.168.0.101:8080",
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

    other_crate_cmd = server.connection.crates
    print(f"Other crate cmd: {other_crate_cmd}")

    all_crates = server.connection.getCrates()
    print(f"All crates {all_crates}.")

    # or_this = all_crates[0].crates
    # print(f"or this?: {or_this}")

    all_modules = server.connection.getModules()
    logging.info(f"All modules {all_modules}.")

    all_channels = []
    for i, mod in enumerate(all_modules):
        all_channels.append(mod.channels)
    logging.info(f"All channels {all_channels}.")

    # time to fill the cache from iCSservice
    time.sleep(10)

    for mod in all_modules:
        logging.info(
            f""" Module {mod.address}
                     Firmwarename: {mod.getStatusFirmwareName()}
                     Seriennummer: {mod.getStatusSerialNumber()}
                     Release: {mod.getStatusFirmwareRelease()}
                     Temperatur: {mod.getStatusTemperature()}
                     """
        )

    for i_mod, mod_channels in enumerate(all_channels):
        print(f"Module: {i_mod}")
        for channel in mod_channels:
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


if __name__ == "__main__":
    main()
