import codecs
import glob
import os
import sys
import getpass


class Checker:

    USAGE = "Usage : python3 Main.py [FLAGS]...\n" \
            "\n" \
            "The script will compare the given password and check if it exists\n" \
            "somewhere inside the lists of previously used \\ leaked \\ common credentials\n" \
            "\n" \
            "Valid Flags : \n" \
            "\n" \
            "-h, --help\n" \
            "\t print this help text\n" \
            "\n" \
            "-i, --insecure\n" \
            "\t echo the password to the console\n" \
            "-v, --verbose\n" \
            "\t print additional information to the console\n" \
            "\n" \
            "-p, --progress\n" \
            "\t show progress bar during the scan\n" \
            "\n" \
            "-c, --count\n" \
            "\t print the number of occurrences for the given password\n" \
            "\n" \
            "Notes : \n" \
            "\n" \
            "* Passwords are invisible by default when you type them\n" \
            "* Flags should be separated by space, no support for grouped flags yet\n" \
            "* Line endings other than LF are not supported yet\n" \
            "* Encodings other than UTF-8 are not supported yet\n"

    VALID_HELP_FLAGS = ("-h", "--help")
    VALID_INSECURE_FLAGS = ("-i", "--insecure")
    VALID_COUNT_FLAGS = ("-c", "--count")
    VALID_VERBOSE_FLAGS = ("-v", "--verbose")
    VALID_PROGRESS_FLAGS = ("-p", "--progress")

    PASSWORD_PROMPT = "Please provide a credential: "

    EXIT_CODE_OK = 0

    def __init__(self, flags: tuple | None = None):

        # Default flag attributes
        self.__flags = flags if flags is not None else ()
        self.__is_insecure = False
        self.__print_count = False
        self.__verbose = False
        self.__show_progress = False
        self.__files_dict = dict()

        for flag in Checker.VALID_HELP_FLAGS:
            if flag in self.__flags:
                self.__print_error_and_exit_with_code(Checker.EXIT_CODE_OK, Checker.USAGE)
        for flag in Checker.VALID_INSECURE_FLAGS:
            if flag in self.__flags:
                self.__is_insecure = True
        for flag in Checker.VALID_COUNT_FLAGS:
            if flag in self.__flags:
                self.__print_count = True
        for flag in Checker.VALID_PROGRESS_FLAGS:
            if flag in self.__flags:
                self.__show_progress = True
        for flag in Checker.VALID_VERBOSE_FLAGS:
            if flag in self.__flags:
                self.__verbose = True

        if self.__is_insecure:
            self.__credential = input(Checker.PASSWORD_PROMPT)
        else:
            self.__credential = getpass.getpass(Checker.PASSWORD_PROMPT)

        # Internal variables
        self.__credential_occurrences = 0
        self.__progress = 0
        self.__credential_found = False

    def __should_show_progress(self) -> bool:

        for flag in Checker.VALID_PROGRESS_FLAGS:
            if flag in self.__flags:
                if sys.stdout.encoding != "utf-8":
                    # Try to get the utf-8 writer
                    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, 'strict')
                    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.buffer, 'strict')
                return True
        return False

    def __print_error_and_exit_with_code(self, code: int, message: str) -> None:

        if not isinstance(code, int):
            raise TypeError(f"Expected an exit code of type 'int' but got : {type(code)} instead")
        if not isinstance(message, str):
            raise TypeError(f"Expected an error message of type 'str' but got : {type(message)} instead")

        print(f"\033[1K\r{message}")
        if self.__show_progress:
            self.__print_progress()
        exit(-1 * code)

    def __print_verbose(self, message: str):

        if self.__verbose:
            print(f"\033[1K\r{message}")
            self.__print_progress()

    def __update_progress(self, current: int, total: int):

        self.__progress = int(100 * (current / total))

    def __print_progress(self):

        if self.__show_progress:
            percent = '█' * self.__progress + '_' * (100 - self.__progress)
            print(f"\033[1K\r[{percent}] {self.__progress} %", end="")

    def __print_result(self):

        print()
        print()
        print(f"Password found : {self.__credential_found}")
        if self.__print_count:
            print(f"We counted {self.__credential_occurrences} occurrences of your password")

    def check(self) -> None:

        current_directory = os.getcwd()
        filenames = glob.glob("**/*.txt", root_dir=current_directory, recursive=True)
        number_of_files = len(filenames)

        for index, filename in enumerate(filenames):

            # Update progress
            self.__update_progress(index + 1, number_of_files)
            self.__print_progress()

            full_name = os.path.join(current_directory, filename)
            self.__print_verbose(f"Checking file : {full_name}")
            with open(full_name, encoding='utf-8') as current_file:
                for line in current_file:
                    line = line.strip()
                    if line == self.__credential:
                        self.__credential_occurrences += 1
                        self.__credential_found = True

        self.__print_result()
