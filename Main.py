import sys

from Checker import Checker


def main():

    if len(sys.argv) < 2:
        # Password wasn't provided by user
        checker = Checker()
        checker.check()
    elif len(sys.argv) == 2:
        # Flags weren't provided by user
        checker = Checker(sys.argv[1])
        checker.check()
    elif len(sys.argv) >= 3:
        # Flags were provided
        checker = Checker(sys.argv[1], tuple(sys.argv[2::]))
        checker.check()


if __name__ == "__main__":
    main()
