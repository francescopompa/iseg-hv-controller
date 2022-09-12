"""
SEE README.md
"""
import ics_helper
import logging



def main():
    """
    ...
    """
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s::%(levelname)s::%(filename)s:%(funcName)s:%(lineno)d::\t%(message)s",
                        handlers=[logging.StreamHandler(), logging.FileHandler("hv_controller.log")])
    logging.info("Started")

    connectionName = "new_iCS_connection"
    # connectionParameters = "ws://localhost:1234"
    connectionLogin = "demo"
    connectionPassword = "demo"


if __name__ == '__main__':
    main()
