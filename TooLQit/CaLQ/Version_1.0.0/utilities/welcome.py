def printBanner():
    try:
        with open("banner", encoding="utf8") as f:
            contents = f.read()
            print(f"{contents}")
    except OSError:
        print("CaLQ: Calculator for LHC limits on leptoquarks")
        print("Version 1.0.0")
