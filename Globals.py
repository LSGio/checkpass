USAGE = "Usage : python3 Main.py <password-string> [MODE] [VERBOSE]\n" \
        "\n" \
        "The script will compare the given password and check if it exists\n" \
        "somewhere inside the directories of this scope\n" \
        "\n" \
        "MODE determines the format of the output\n" \
        "VERBOSE enables printing of additional info during the scan (may affect scan speeds)\n" \
        "\n" \
        "Modes : \n" \
        "\n" \
        "1 (default) - print only binary answer after the scan finishes, \n" \
        "either the password exists or it doesn't exist\n" \
        "2 - print names of files during the scan\n" \
        "3 - print names of files and number of occurrences in each file during the scan \n" \
        "\n" \
        "Verbose : \n" \
        "\n" \
        "false | no | 0 (default) - output depends on provided mode only\n" \
        "true | yes | 1 - haven't decided what is does yet\n"

ALLOWED_MODES = ("1", "2", "3")
ALLOWED_VERBOSE_FLAGS = ("0", "1", "true", "false", "yes", "no")

# exit codes and error codes

EXIT_CODE_PASSWORD_NOT_IN_LISTS = 0
EXIT_CODE_PASSWORD_IN_LISTS = 1
ERROR_CODE_NOT_ENOUGH_ARGS = 2
ERROR_CODE_INVALID_MODE = 3
ERROR_CODE_INVALID_VERBOSE_FLAG = 4

# corresponding exit and error messages

EXIT_MESSAGES = (
        "Your password is not in the lists",
        "Your password is in the lists",
        f"Missing required positional argument at position 1 \n\n{USAGE}",
        f"Invalid mode, must be one of : {ALLOWED_MODES}"
        f"Invalid verbose flag, must be one of : {ALLOWED_VERBOSE_FLAGS}"
)
