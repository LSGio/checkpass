import sys

from Checker import Checker


def main():

    if len(sys.argv) < 2:
        # Password not provided by user
        C = Checker()
        C.check()
    elif len(sys.argv) == 2:
        # Flags not provided by user
        C = Checker(sys.argv[1])
        C.check()
    elif len(sys.argv) >= 3:
        # Flags were provided
        C = Checker(sys.argv[1], tuple(sys.argv[2::]))
        C.check()


if __name__ == "__main__":
    main()
