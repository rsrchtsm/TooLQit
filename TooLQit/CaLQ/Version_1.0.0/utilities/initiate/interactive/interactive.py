from utilities.constants import (
    luminosity,
    default_ignore_single_pair_processes,
    default_significane,
    default_systematic_error,
    default_extra_width,
    InputMode,
)
from utilities.initiate.interactive.validate import (
    validateLeptoQuarkModel, 
    validateLeptoQuarkMass,
    validateLeptoQuarkCouplings,
    validateIgnoreSinglePairProduction,
    validateSignificance,
    validateSystematicError,
    validateExtraWidth
)
from utilities.parse import sortCouplingsAndValuesInteractive
from utilities.colour import prRed, prBlueNoNewLine, prBlue
from utilities.validate import validateInputData
from calculate import calculate


def initiateInteractive():
    """
    Initiate procedure for interactive mode
    """
    # initialize leptoquark model values
    leptoquark_model = "U1"
    leptoquark_mass = "1000"
    couplings = "X10LL[3,3]"
    ignore_single_pair_processes = default_ignore_single_pair_processes
    significance = default_significane
    systematic_error = default_systematic_error
    extra_width = default_extra_width

    printDefaultValues(ignore_single_pair_processes, significance, systematic_error, extra_width) 

    # loop to input values. we will have to add validations here only
    while True:
        prBlueNoNewLine("calq > ")
        inpt = input()
        s = inpt.split("=")
        if (":" in inpt):
            s = inpt.split(":")
        slen = len(s)
        if s[0].strip() == "import_model" and slen == 2:
            if validateLeptoQuarkModel(s[1].strip().upper()):
                leptoquark_model = s[1].strip().upper()
        elif s[0].strip() == "mass" and slen == 2:
            if validateLeptoQuarkMass(s[1].strip()):
                leptoquark_mass = s[1].strip()
        elif s[0].strip() == "couplings" and slen > 1:
            if validateLeptoQuarkCouplings(s[1].strip().upper(), leptoquark_model):
                couplings = s[1].strip().upper()
        elif s[0].strip() == "ignore_single_pair" and slen == 2:
            if validateIgnoreSinglePairProduction(s[1].strip()):
                ignore_single_pair_processes = "no"
                if s[1].strip().lower() in {"yes", "y", "true", "t", "1"}:
                    ignore_single_pair_processes = "yes"
        elif s[0].strip() == "significance" and slen == 2:
            if validateSignificance(s[1].strip()):
                significance = int(s[1].strip())
        elif s[0].strip() == "systematic_error" and slen == 2:
            if validateSystematicError(s[1].strip()):
                systematic_error = s[1].strip()
        elif s[0].strip() == "extra_width" and slen == 2:
            if validateExtraWidth(s[1].strip()):
                extra_width = float(s[1].strip())
        elif s[0].strip() == "status":
            print(f" Leptoquark model: {leptoquark_model}")
            print(f" Leptoquark mass = {leptoquark_mass}")
            print(f" Couplings: {couplings}")
            print(f" Extra width = {extra_width}")
            print(f" Ignore single & pair processes: {ignore_single_pair_processes}")
            print(f" Significance = {significance}")
            print(f" Systematic error = {systematic_error}")
        elif s[0].strip() == "help":
            printHelp()
        elif s[0].strip() == "initiate":
            leptoquark_parameters, _ = validateInputData(leptoquark_model, leptoquark_mass, couplings, ignore_single_pair_processes, significance, systematic_error, extra_width, luminosity)
            leptoquark_parameters.couplings_values = [" ".join(["0"] * len(couplings))]
            sortCouplingsAndValuesInteractive(leptoquark_parameters)
            calculate(leptoquark_parameters, InputMode.INTERACTIVE)
        elif s[0].strip().lower() in ["exit", "q", "quit", "exit()", ".exit"]:
            return
        elif s[0].strip() == "":
            continue
        else:
            prRed(f" Command {s[0]} not recognised. Please retry or enter 'q', 'quit' or 'exit' to exit.")


def printDefaultValues(ignore_single_pair_processes: str, significance: int, systematic_error: str, extra_width: int):
    # also print initial message here
    prBlue("========================================================")
    prBlue("Commands available:")
    print(" import_model:, mass=, couplings: , extra_width=,\n ignore_single_pair: (yes/no), significance=(1/2),\n systematic_error=, status, initiate, help")     

    prBlue("Couplings available:")
    print(" Examples for S1: Y10LL[1,1] Y10RR[3,1] [...]\n Examples for U1: X10LL[3,2] X10RR[1,1] [...]")

    prBlue("Default values:")
    print(f" import_model: U1")
    print(f" mass = 1000")
    print(f" couplings: X10LL[3,3]")
    print(f" extra_width = {extra_width}")
    print(f" ignore_single_pair: {ignore_single_pair_processes}")
    print(f" significance = {significance}")
    print(f" systematic_error = {systematic_error}")
    prBlue("========================================================")

def printHelp():
    """
    Content to be printed when help is inputted
    """
    prBlue("Commands with '=' expect a numerical value. Read README.md for more info on individual commands.")
    prBlue("Value input commands: ")
    print(" import_model: [Leptoquark model]")
    print(" mass= [Leptoquark mass] (should be between 1000 and 5000)")
    print(" couplings: [Couplings. For the format, refer to README.md]")
    print(" ignore_single_pair: [If true, the single & pair production contributions are ignored]")
    print(" significance= [Significance of the limit in standard deviations. Possible values=1,2]")
    print(" systematic_error= [Systematic error to be included in the calculations. Should be between 0 and 1]")
    print(" extra_width= [extra width to account for additional unaccounted decays]")
    prBlue("Other commands:")
    print(" status [To print current values]")
    print(" initiate [To start the calcualation]")
    print(" exit [To exit the calculator]")