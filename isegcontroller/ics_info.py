import logging
import time
from isegcontroller.ics_client import IcsClient
from isegcontroller.ics_module_wrapper import ICSModuleAbstraction
from isegcontroller.ics_channel_wrapper import ICSChannelAbstraction
import inspect

# TODO CONVERT THIS INTO strings or dicts that can be used by interpreter


def get_all_channel_infos(ics_client: IcsClient) -> list[str]:
    channel_info_strings = []
    for ch_id, channel in ics_client.channels_dict.items():
        channel_info_strings.append(get_channel_info(ch_id, channel))
    return channel_info_strings


def get_complete_channel_info(channel: ICSChannelAbstraction) -> str:
    """
    prints the values of all the getter methods of a channel
    """
    # get all methods of channel (they are builtin bc it's a c wrapping)
    builtin_members = inspect.getmembers(channel, inspect.isbuiltin)

    getters = [(name, func) for name, func in builtin_members if name.startswith("get")]

    complete_string = ""
    for name, func in getters:
        value = func()
        complete_string += f"{name[2:]}: \t {value}"
    return complete_string


def get_channel_info(ch_id, channel: ICSChannelAbstraction) -> dict:
    status_v_nominal = channel.getStatusVoltageNominal()
    control_v_set = channel.getControlVoltageSet()
    status_v_measure = channel.getStatusVoltageMeasure()
    status_c_nominal = channel.getStatusCurrentNominal()
    control_c_set = channel.getControlCurrentSet()
    status_c_measure = channel.getStatusCurrentMeasure()
    status_v_limit_exceed = channel.getStatusVoltageLimitExceeded()
    status_c_limit_exceed = channel.getStatusCurrentLimitExceeded()
    status_current_trip = channel.getStatusTrip()
    status_on = channel.getStatusOn()
    status_emergency = channel.getStatusEmergency()
    time.sleep(0.1)  # wait for info to be filled
    return {
        "channel_id": ch_id,
        "status_on": status_on,
        "control_v_set": control_v_set,
        "status_v_measure": status_v_measure,
        "status_v_nominal": status_v_nominal,
        "control_c_set": control_c_set,
        "status_c_measure": status_c_measure,
        "status_c_nominal": status_c_nominal,
        "status_v_limit_exceed": status_v_limit_exceed,
        "status_c_limit_exceed": status_c_limit_exceed,
        "status_current_trip": status_current_trip,
        "status_emergency": status_emergency,
    }


def print_basic_info(ics_client: IcsClient) -> None:
    # Important to wait here so the crate gets booted up or whatever
    other_crate_cmd = ics_client.connection.crates
    print(f"Other crate cmd: {other_crate_cmd}")

    all_crates = ics_client.connection.getCrates()
    print(f"All crates {all_crates}.")

    # or_this = all_crates[0].crates
    # print(f"or this?: {or_this}")

    all_modules = ics_client.connection.getModules()
    logging.info(f"All modules {all_modules}.")

    all_channels = []
    for mod in all_modules:
        for i, channel in enumerate(mod.channels):
            all_channels.append(channel)
    logging.info(f"All channels {all_channels}.")

    # time to fill the cache from iCSservice
    time.sleep(0.2)

    for mod in all_modules:
        logging.info(f""" Module {mod.address}
                     Firmwarename: {mod.getStatusFirmwareName()}
                     Seriennummer: {mod.getStatusSerialNumber()}
                     Release: {mod.getStatusFirmwareRelease()}
                     Temperatur: {mod.getStatusTemperature()}
                     """)

    # for channel in all_channels:
    # get_channel_info(channel)
