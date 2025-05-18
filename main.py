# NOTE(wernerg): Constants
PROGRAM_MODE_DEV = "PROGRAM_MODE_DEV"
PROGRAM_MODE_CLI = "PROGRAM_MODE_CLI"
PROGRAM_MODE_STATS = "PROGRAM_MODE_STATS"
FILE_NOT_FOUND = "FILE_NOT_FOUND"
PERMISSION_DENIED = "PERMISSION_DENIED"
GENERIC_ERROR = "GENERIC_ERROR"

# NOTE(wernerg): Globals
program_modes = {
    "PROGRAM_MODE_DEV": 1,
    "PROGRAM_MODE_CLI": 2,
    "PROGRAM_MODE_STATS": 3,
}
error_codes = {
    "FILE_NOT_FOUND": 1,
    "PERMISSION_DENIED": 2,
    "GENERIC_ERROR": 3,
}


# NOTE(wernerg): Functions
def sort_pair(result, by_key=False, reverse=False):
    key_func = (lambda x: x[0]) if by_key else (lambda x: x[1])
    result.sort(key=key_func, reverse=reverse)
    return result


def count_per_char(text):
    result = []
    for char in text.lower():
        if char.isalpha():
            found = False
            for i, (c, cnt) in enumerate(result):
                if c == char:
                    result[i] = (c, cnt + 1)
                    found = True
                    break
            if not found:
                result.append((char, 1))
    return result


def format_error_message(error_code, msg):
    result = ""
    if PROGRAM_MODE_DEV in program_modes:
        result = "[ERR] " + msg
    if PROGRAM_MODE_CLI in program_modes:
        switch = {
            FILE_NOT_FOUND: lambda: "File not found.",
            PERMISSION_DENIED: lambda: "Read access denied.",
            GENERIC_ERROR: lambda: "Terribly sorry, bad programmers borked the codez.",
        }
        result = switch.get(error_code, lambda: "")()
    return result


def append_log(err_code, msg):
    result = []
    if err_code in error_codes:
        result.append(format_error_message(err_code, msg))
    return result


def read_file(filepath):
    result = None, ""
    try:
        with open(filepath, "r") as f:
            result = None, f.read()
    except FileNotFoundError:
        result = FILE_NOT_FOUND, f"File '{filepath}' not found"
    except PermissionError:
        result = PERMISSION_DENIED, f"File '{filepath}' read permission denied"
    except Exception as e:
        result = GENERIC_ERROR, f"{str(e)}"
    return result


def main():
    # NOTE(wernerg): Startup section
    result = []
    filepath = "books/frankenstein.txt"

    # NOTE(wernerg): Processing section
    err, file_content = read_file(filepath)
    if err:
        result = append_log(err, file_content)
    total_char_cnt = len(file_content)
    cnt_pair = count_per_char(file_content)
    sorted_pair = sort_pair(cnt_pair, reverse=True)
    total_word_cnt = len(file_content.split())

    # NOTE(wernerg): Output section
    if not err:
        if PROGRAM_MODE_CLI in program_modes:
            result.append(file_content)
        if PROGRAM_MODE_STATS in program_modes:
            result.append(f"--- Analysis report of {filepath} ---")
            result.append(f"Total word count: {total_word_cnt}")
            if sorted_pair is not None:
                result.append(f"Total char count: {total_char_cnt}")
                for char, cnt in sorted_pair:
                    result.append(f"'{char}': {cnt}")
            result.append("--- End of analysis report ---")
    if len(result) > 0:
        print("\n".join(filter(None, result)))


if __name__ == "__main__":
    program_modes = {
        PROGRAM_MODE_DEV,
        PROGRAM_MODE_CLI,
        PROGRAM_MODE_STATS,
    }
    main()
