import glob
import os



class Checker:

    USAGE = "Usage : python3 Main.py <password-string> [FORMAT] [FLAGS]...\n" \
            "\n" \
            "The script will compare the given password and check if it exists\n" \
            "somewhere inside the lists of previously used \\ leaked \\ common credentials\n" \
            "\n" \
            "FORMAT determines the format of the output\n" \
            "\n" \
            "Valid Formats : \n" \
            "\n" \
            "1 (default) - print only binary answer after the scan finishes, \n" \
            "either the password exists or it doesn't exist\n" \
            "2 - print names of files during the scan\n" \
            "3 - print names of files and number of occurrences during the scan \n" \
            "FLAGS affect the behaviour of the script, more info below (may affect scan speeds)\n" \
            "\n" \
            "Valid Flags : \n" \
            "\n" \
            "-v, --verbose\n" \
            "\t print additional information to the console\n" \
            "\n" \
            "-p, --progress\n" \
            "\t show progress bar during the scan" \
            "\n" \
            "Notes : \n" \
            "\n" \
            "* Line endings other than LF are not supported yet\n" \
            "* Encodings other than UTF-8 are not supported yet\n"

    VALID_FORMATS = ("1", "2", "3")
    VALID_VERBOSE_FLAGS = ("-v", "--verbose")
    VALID_PROGRESS_FLAGS = ("-p", "--progress")

    # Exit codes and error codes

    EXIT_CODE_PASSWORD_NOT_IN_LISTS = 0
    EXIT_CODE_PASSWORD_IN_LISTS = 1
    ERROR_CODE_NOT_ENOUGH_ARGS = 2
    ERROR_CODE_INVALID_FORMAT = 3

    # Corresponding exit and error messages

    EXIT_MESSAGES = (
        "Your password is not in the lists",
        "Your password is in the lists",
        f"Missing required positional argument at position 1 \n\n{USAGE}",
        f"Invalid format, must be one of : {VALID_FORMATS}"
    )

    def __init__(self, credential: str = None, output_format: str = "1", flags: tuple = None):

        # Mandatory attributes
        self.__credential = self.__get_valid_credential(credential)
        self.__output_format = self.__get_valid_output_format(output_format)

        # Optional attributes
        self.__credential_occurrences = 0
        self.__progress = 0
        self.__credential_found = False
        self.__flags = () if flags is None else flags
        self.__verbose = self.__is_verbose()
        self.__show_progress = self.__should_show_progress()

    def __get_valid_credential(self, credential: str) -> str:

        if credential is None:
            self.__handle_error_or_exit_with_code(Checker.ERROR_CODE_NOT_ENOUGH_ARGS)
        else:
            return credential

    def __get_valid_output_format(self, output_format: str) -> int:

        if output_format not in Checker.VALID_FORMATS:
            self.__handle_error_or_exit_with_code(Checker.ERROR_CODE_INVALID_FORMAT)
        else:
            return int(output_format)

    def __is_verbose(self) -> bool:

        for flag in Checker.VALID_VERBOSE_FLAGS:
            if flag in self.__flags:
                return True
        return False

    def __should_show_progress(self) -> bool:

        for flag in Checker.VALID_PROGRESS_FLAGS:
            if flag in self.__flags:
                return True
        return False

    def __handle_error_or_exit_with_code(self, code: int) -> None:

        if not isinstance(code, int):
            raise TypeError(f"Expected exit code must be of type 'int' but got : {type(code)}")
        else:
            print(f"\r\n{Checker.EXIT_MESSAGES[code]}")
            exit(code)

    def __print_verbose(self, message: str):

        if self.__verbose:
            print(f"\033[1K\r{message}")
            self.__print_progress()

    def __update_progress(self, current, total):

        self.__progress = int(100 * (current / float(total)))

    def __print_progress(self):

        if self.__show_progress:
            percent = '█' * self.__progress + '_' * (100 - self.__progress)
            print(f"\033[1K\r[{percent}] {self.__progress}%", end="")

    def check(self) -> None:

        cwd = os.getcwd()
        filenames = glob.glob("**/*.txt", root_dir=os.getcwd(), recursive=True)
        number_of_files = len(filenames)

        for index, filename in enumerate(filenames):

            # Update progress
            self.__update_progress(index + 1, number_of_files)
            self.__print_progress()

            full_name = os.path.join(cwd, filename)
            self.__print_verbose(f"Checking file : {full_name}")
            with open(full_name, encoding='utf-8') as current_file:
                for line in current_file:
                    line = line.strip('\n')
                    if line == self.__credential:
                        self.__credential_occurrences += 1
                        self.__credential_found = True

        if not self.__credential_found:
            self.__handle_error_or_exit_with_code(Checker.EXIT_CODE_PASSWORD_NOT_IN_LISTS)
        else:
            if self.__output_format == 2:
                print(f"We counted {self.__credential_occurrences} occurrences of your password")
            self.__handle_error_or_exit_with_code(Checker.EXIT_CODE_PASSWORD_IN_LISTS)
