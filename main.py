"""
SEE README.md
"""
import ics_helper


def main():
    """
    ...
    """
    print(ics_helper.check_is_linux_platform())
    print(ics_helper.check_is_win_platform())
    ics_client = ics_helper.import_from_path("", "")


if __name__ == '__main__':
    main()
