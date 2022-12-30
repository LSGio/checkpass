import sys

from Checker import Checker


def main():

    if len(sys.argv) < 2:
        # Password not provided by user, checking empty string
        C = Checker()
        C.check()
    elif len(sys.argv) == 2:
        # Output format not provided by user
        C = Checker(sys.argv[1])
        C.check()
    elif len(sys.argv) == 3:
        # Output format was provided
        C = Checker(sys.argv[1], sys.argv[2])
        C.check()
    elif len(sys.argv) >= 4:
        # Flags were provided
        C = Checker(sys.argv[1], sys.argv[2], tuple(sys.argv[3::]))
        C.check()


if __name__ == "__main__":
    main()
