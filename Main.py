import sys

from Checker import Checker


def main():
    if len(sys.argv) < 2:
        # Password not provided by user, checking empty string
        C = Checker()
        C.check()
    elif len(sys.argv) == 2:
        # Mode not provided by user
        C = Checker(sys.argv[1])
        C.check()
    elif len(sys.argv) == 3:
        # Mode was provided
        C = Checker(sys.argv[1], sys.argv[2])
        C.check()
    elif len(sys.argv) > 4:
        # Flags were provided
        # TODO : slice the sys.argv list and send flags as tuple to constructor
        pass


if __name__ == "__main__":
    main()
