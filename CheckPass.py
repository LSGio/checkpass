import os

import Globals


def check_pass(password: str, mode: int = 1, verbose: bool = False) -> None:
    counter = 0
    found = False

    for (root, dirs, files) in os.walk(os.getcwd()):
        for name in files:
            full_name = os.path.join(root, name)
            if not str(full_name).endswith(".txt"):
                continue
            else:
                with open(full_name, encoding='utf-8') as current_file:
                    print(f"reading file {full_name}")
                    for line in current_file:
                        line = line.strip('\n')
                        if line == password:
                            counter += 1
                            found = True

    if not found:
        handle_error_or_exit_with_code(Globals.EXIT_CODE_PASSWORD_NOT_IN_LISTS)
    else:
        if mode == 2:
            print(f"We counted {counter} occurrences of your password")
        handle_error_or_exit_with_code(Globals.EXIT_CODE_PASSWORD_IN_LISTS)


def handle_error_or_exit_with_code(code: int) -> None:
    if not isinstance(code, int):
        raise TypeError(f"Expected exit code must be of type 'int' but got : {type(code)}")
    else:
        print(Globals.EXIT_MESSAGES[code])
        exit(code)
