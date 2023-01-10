import sys

from Checker import Checker


def main():

    if len(sys.argv) < 2:
        checker = Checker()
        checker.check()
    else:
        checker = Checker(tuple(sys.argv[1::]))
        checker.check()


if __name__ == "__main__":
    main()
