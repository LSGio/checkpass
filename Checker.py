import glob
import os
import getpass


class Checker:

    USAGE = "Usage : python3 Main.py [FLAGS]...\n" \
            "\n" \
            "The script compares a user-given password and checks if it exists\n" \
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
            "\t print scanned filenames, add an asterisk if credential is found there\n" \
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

    PASSWORD_PROMPT = "Please provide a credential: "

    RESULT_PASSWORD_FOUND = "Your credential is in the files!"
    RESULT_PASSWORD_NOT_FOUND = "Your credential is not in the files!"
    RESULT_OCCURRENCE_FORMAT = "We counted {0} occurrences of your password"

    EXIT_CODE_OK = 0

    ERROR_TYPE_MISMATCH = "Expected an exit code of type {0} but got : {1} instead"

    def __init__(self, flags: tuple | None = None):

        # Default flag attributes
        self.__flags = flags if flags is not None else ()
        self.__is_insecure = False
        self.__print_count = False
        self.__verbose = False
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
        for flag in Checker.VALID_VERBOSE_FLAGS:
            if flag in self.__flags:
                self.__verbose = True

        if self.__is_insecure:
            self.__credential = input(Checker.PASSWORD_PROMPT)
        else:
            self.__credential = getpass.getpass(Checker.PASSWORD_PROMPT)

        # Internal variables
        self.__credential_occurrences = 0
        self.__credential_found = False

    def __print_error_and_exit_with_code(self, code: int = EXIT_CODE_OK, message: str | None = None) -> None:

        if not isinstance(code, int):
            raise TypeError(Checker.ERROR_TYPE_MISMATCH.format(str(int), str(type(code))))
        if not isinstance(message, str):
            raise TypeError(Checker.ERROR_TYPE_MISMATCH.format(str(str), str(type(message))))
        if message is not None:
            print(message)
        exit(-1 * code)

    def __print_verbose(self, message: str):

        if self.__verbose:
            print(message)

    def __print_result(self):

        result = Checker.RESULT_PASSWORD_FOUND if self.__credential_found else Checker.RESULT_PASSWORD_NOT_FOUND
        print(result)
        if self.__print_count and self.__credential_found:
            print(Checker.RESULT_OCCURRENCE_FORMAT.format(self.__credential_occurrences))

    def check(self) -> None:

        glob_pattern_passwords = "Passwords/**/*.txt"
        glob_pattern_hashes = "Hashes/**/*.txt"
        glob_pattern_login_pairs = "LoginPairs/**/*.txt"

        current_directory = os.getcwd()
        filenames = glob.glob(glob_pattern_passwords, root_dir=current_directory, recursive=True)
        self.__files_dict = dict.fromkeys(filenames, 0)

        for index, filename in enumerate(filenames):

            full_name = os.path.join(current_directory, filename)
            with open(full_name, encoding='utf-8') as current_file:
                for line in current_file:
                    line = line.strip()
                    if line == self.__credential:
                        self.__files_dict[filename] += 1
                        self.__credential_found = True

                if self.__files_dict[filename] != 0:
                    self.__print_verbose(f"File : {full_name} *")
                else:
                    self.__print_verbose(f"File : {full_name}")

        self.__credential_occurrences = sum(self.__files_dict.values())
        self.__print_result()
