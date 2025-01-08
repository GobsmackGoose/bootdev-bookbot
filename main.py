#NOTE(wernerg): Constants
PROGRAM_MODE_DEV    = "PROGRAM_MODE_DEV"
PROGRAM_MODE_CLI    = "PROGRAM_MODE_CLI"
PROGRAM_MODE_STATS  = "PROGRAM_MODE_STATS"
FILE_NOT_FOUND      = "FILE_NOT_FOUND"
PERMISSION_DENIED   = "PERMISSION_DENIED"
GENERIC_ERROR       = "GENERIC_ERROR"

#NOTE(wernerg): Globals
program_modes = {
  "PROGRAM_MODE_DEV":   1,
  "PROGRAM_MODE_CLI":   2,
  "PROGRAM_MODE_STATS": 3,
}
error_codes = {
  "FILE_NOT_FOUND":     1,
  "PERMISSION_DENIED":  2,
  "GENERIC_ERROR":      3,
}

#NOTE(wernerg): Functions
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
  #NOTE(wernerg): Startup section
  result = []
  filepath = "books/frankenstein.txt"

  #NOTE(wernerg): Processing section
  err, file_content = read_file(filepath)
  if err: result = append_log(err, file_content)
  words = file_content.split()
  count = len(words)

  #NOTE(wernerg): Output section
  if not err:
    if PROGRAM_MODE_CLI in program_modes:
      result.append(file_content)
    if PROGRAM_MODE_STATS  in program_modes:
      result.append(f"Total word count: {count}")

  if len(result) > 0: print("\n".join(filter(None, result)))

if __name__ == "__main__":
  program_modes = {
    PROGRAM_MODE_DEV,
    PROGRAM_MODE_CLI,
    PROGRAM_MODE_STATS,
  }
  main()
