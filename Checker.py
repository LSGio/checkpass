import codecs
import glob
import os
import sys


class Checker:

    USAGE = "Usage : python3 Main.py <password-string> [FLAGS]...\n" \
            "\n" \
            "The script will compare the given password and check if it exists\n" \
            "somewhere inside the lists of previously used \\ leaked \\ common credentials\n" \
            "\n" \
            "Valid Flags : \n" \
            "\n" \
            "-v, --verbose\n" \
            "\t print additional information to the console\n" \
            "\n" \
            "-p, --progress\n" \
            "\t show progress bar during the scan" \
            "\n" \
            "-c, --count\n" \
            "\t print the number of occurrences for the given password" \
            "Notes : \n" \
            "\n" \
            "* Flags should be separated by space, no support for grouped flags yet\n" \
            "* Line endings other than LF are not supported yet\n" \
            "* Encodings other than UTF-8 are not supported yet\n"

    VALID_COUNT_FLAGS = ("-c", "--count")
    VALID_VERBOSE_FLAGS = ("-v", "--verbose")
    VALID_PROGRESS_FLAGS = ("-p", "--progress")

    # Error codes

    ERROR_CODE_NOT_ENOUGH_ARGS = 1

    # Corresponding error messages

    ERROR_MESSAGES = (
        f"Missing required positional argument at position 1 \n\n{USAGE}"
    )

    def __init__(self, credential: str | None = None, flags: tuple | None = None):

        # Mandatory attributes
        if credential is None:
            self.__handle_error_or_exit_with_code(Checker.ERROR_CODE_NOT_ENOUGH_ARGS)
        else:
            self.__credential = credential

        # Flag attributes
        self.__flags = flags if flags is not None else ()
        self.__print_count = False
        self.__show_progress = False
        self.__verbose = False

        for flag in Checker.VALID_COUNT_FLAGS:
            if flag in self.__flags:
                self.__print_count = True
        for flag in Checker.VALID_PROGRESS_FLAGS:
            if flag in self.__flags:
                self.__show_progress = True
        for flag in Checker.VALID_VERBOSE_FLAGS:
            if flag in self.__flags:
                self.__verbose = True

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

    def __handle_error_or_exit_with_code(self, code: int) -> None:

        if not isinstance(code, int):
            raise TypeError(f"Expected an exit code of type 'int' but got : {type(code)} instead")
        else:
            # Codes are enumerated from 1, so we subtract 1 to access the list of messages
            print(f"\033[1K\r{Checker.ERROR_MESSAGES[code - 1]}")
            self.__print_progress()
            exit(-1 * code)

    def __print_verbose(self, message: str):

        if self.__verbose:
            print(f"\033[1K\r{message}")
            self.__print_progress()

    def __update_progress(self, current: int, total: int):

        self.__progress = int(100 * (current / float(total)))

    def __print_progress(self):

        if self.__show_progress:
            percent = '█' * self.__progress + '_' * (100 - self.__progress)
            print(f"\033[1K\r[{percent}] {self.__progress} %", end="")

    def __print_result(self):
        pass

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
