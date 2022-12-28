import sys

import CheckPass
import Globals


def main():
    if len(sys.argv) < 2:
        # Password not provided by user
        CheckPass.handle_error_or_exit_with_code(Globals.ERROR_CODE_NOT_ENOUGH_ARGS)
    elif len(sys.argv) == 2:
        # Mode not provided by user
        CheckPass.check_pass(sys.argv[1], 1)
    elif len(sys.argv) == 3:
        # Mode was provided
        if sys.argv[2] not in Globals.ALLOWED_MODES:
            # Unknown mode
            CheckPass.handle_error_or_exit_with_code(Globals.ERROR_CODE_INVALID_MODE)
        else:
            CheckPass.check_pass(sys.argv[1], int(sys.argv[2]))
    elif len(sys.argv) == 4:
        # Verbose flag was provided
        if sys.argv[3].lower() not in Globals.ALLOWED_VERBOSE_FLAGS:
            CheckPass.handle_error_or_exit_with_code(Globals.ERROR_CODE_INVALID_VERBOSE_FLAG)
        else:
            CheckPass.check_pass(sys.argv[1], int(sys.argv[2]), )


if __name__ == "__main__":
    main()
