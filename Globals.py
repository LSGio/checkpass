USAGE = "Usage : python3 Main.py <password-string> [MODE] [FLAGS]...\n" \
        "\n" \
        "The script will compare the given password and check if it exists\n" \
        "somewhere inside the directories of this scope\n" \
        "\n" \
        "MODE determines the format of the output\n" \
        "VERBOSE enables printing of additional info during the scan (may affect scan speeds)\n" \
        "Mandatory arguments to long options are mandatory for short options too\n" \
        "\n" \
        "Modes : \n" \
        "\n" \
        "1 (default) - print only binary answer after the scan finishes, \n" \
        "either the password exists or it doesn't exist\n" \
        "2 - print names of files during the scan\n" \
        "3 - print names of files and number of occurrences during the scan \n" \
        "\n" \
        "Flags : \n" \
        "\n" \
        "-v, --verbose\n" \
        "\t print additional information to the console\n" \
        "\n" \
        "Notes : \n" \
        "\n" \
        "* CRLF line endings are not supported yet\n" \
        "* Encodings other than UTF-8 are not supported yet\n"

VALID_MODES = ("1", "2", "3")
VALID_VERBOSE_FLAGS = ("-v", "--verbose")

# exit codes and error codes

EXIT_CODE_PASSWORD_NOT_IN_LISTS = 0
EXIT_CODE_PASSWORD_IN_LISTS = 1
ERROR_CODE_NOT_ENOUGH_ARGS = 2
ERROR_CODE_INVALID_MODE = 3

# corresponding exit and error messages

EXIT_MESSAGES = (
        "Your password is not in the lists",
        "Your password is in the lists",
        f"Missing required positional argument at position 1 \n\n{USAGE}",
        f"Invalid mode, must be one of : {ALLOWED_MODES}"
)
