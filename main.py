"""
SEE README.md
"""
import logging
import ics_client



def main():
    """
    ...
    """
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s::%(levelname)s::%(filename)s:%(funcName)s:%(lineno)d::\t%(message)s",
                        handlers=[logging.StreamHandler(), logging.FileHandler("hv_controller.log")])
    logging.info("Started")

    connection_name = "new_iCS_connection"
    # connection_parameters = "ws://localhost:1234"
    connection_login = "demo"
    connection_password = "demo"




if __name__ == '__main__':
    main()

