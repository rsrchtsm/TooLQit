def prBlue(text):
    print(f"\033[94m{text}\033[00m")

def prBlueNoNewLine(text):
    print(f"\033[94m{text}\033[00m", end='')

def prRed(text):
    print(f"\033[91m{text}\033[00m")

def prRedNoNewLine(text):
    print(f"\033[91m{text}\033[00m", end='')