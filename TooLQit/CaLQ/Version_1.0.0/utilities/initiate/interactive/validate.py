from utilities.constants import scalar_leptoquark_models, vector_leptoquark_models, minimum_leptoquark_mass, maximum_leptoquark_mass
from utilities.colour import prRed


def validateLeptoQuarkModel(
    leptoquark_model: str,
) -> bool:
    if leptoquark_model not in scalar_leptoquark_models and leptoquark_model not in vector_leptoquark_models:
        prRed(f"[Model error]: Not a valid lepqtoquark model. Allowed models: {scalar_leptoquark_models + vector_leptoquark_models}")
        return False
    return True


def validateLeptoQuarkMass(
    leptoquark_mass: str, 
) -> bool:
    try:
        leptoquark_mass = float(leptoquark_mass)
        if leptoquark_mass < minimum_leptoquark_mass or leptoquark_mass > maximum_leptoquark_mass:
            prRed(f"[Mass error]: Leptoquark mass should be between {minimum_leptoquark_mass} GeV and {maximum_leptoquark_mass} GeV")
            return False
    except:
        prRed("[Mass error]: Leptoquark mass should be a valid number")
        return False
    return True

def validateLeptoQuarkCouplings(
    couplings: str, 
    leptoquark_model: str,
) -> bool:
    couplings_list = couplings.strip().split(' ')

    # Count frequency of each element
    frequency = {}
    for item in couplings_list:
        if item in frequency:
            prRed(f"[Couplings error]: Coupling {item} is repeated. A coupling can only be inputted once")
            return False
        else:
            frequency[item] = 1

    if not len(couplings_list):
        prRed("[Couplings error]: Couplings cannot be empty. Refer to README.md for valid format")
        return False
    for i in range(len(couplings_list)):
        if len(couplings_list[i]) != 10:
            prRed(f"[Couplings error]: The couplings input {couplings_list[i]} is not 10 characters. Refer to README.md for valid format")
            return False
        if not (
            (couplings_list[i][0] == 'Y' and leptoquark_model in scalar_leptoquark_models)
            or (couplings_list[i][0] == 'X' and leptoquark_model in vector_leptoquark_models)
        ):
            prRed("[Couplings error]: For scalar leptoquarks, the first letter should be Y & for vector leptoquarks, it should be X. Refer to README.md for valid format")
            return False
        if couplings_list[i][1:3] != "10":
            prRed(f"[Couplings error]: The second and third characters of {couplings_list[i]} should be '10'. Refer to README.md for valid format")
            return False
        if couplings_list[i][3] not in ["L", "R"]:
            prRed(f"[Couplings error]: The 4th character of {couplings_list[i]} should be either L or R for left-handed & right-handed couplings respectively. Refer to README.md for valid format")
            return False
        if couplings_list[i][4] not in ["L", "R"]:
            prRed(f"[Couplings error]: The 5th character of {couplings_list[i]} should be either L or R for left-handed & right-handed couplings respectively. Refer to README.md for valid format")
            return False
        if couplings_list[i][5] != '[':
            prRed(f"[Couplings error]: The 6th character of {couplings_list[i]} should be '['. Refer to README.md for valid format")
            return False
        if (leptoquark_model in scalar_leptoquark_models and couplings_list[i][6] not in ["1", "2"]) or (leptoquark_model in vector_leptoquark_models and couplings_list[i][6] not in ["1", "2", "3"]):
            prRed(f"[Couplings error]: The 7th character of {couplings_list[i]} should be a valid quark generation. Refer to README.md for valid format")
            return False
        if couplings_list[i][7] != ',':
            prRed(f"[Couplings error]: The 8th character of {couplings_list[i]} should be ','. Refer to README.md for valid format")
            return False
        if couplings_list[i][8] not in ["1", "2", "3"]:
            prRed(f"[Couplings error]: The 9th character of {couplings_list[i]} should be a valid lepton generation. Refer to README.md for valid format")
            return False
        if couplings_list[i][9] != ']':
            prRed(f"[Couplings error]: The 10th character of {couplings_list[i]} should be ']'. Refer to README.md for valid format")
            return False
    return True


def validateIgnoreSinglePairProduction(
    ignore_single_pair_processes: str, 
) -> bool:
    if ignore_single_pair_processes.lower() in {"yes", "y", "true", "t", "1", "no", "n", "false", "f", "0"}:
        return True
    prRed("[Ignore single pair production error]: ignore_single_pair takes input 'yes'/'y' or 'no'/'n'")
    return False

def validateSignificance(
    significance: str, 
) -> bool:
    try:
        significance = int(significance)
        if significance != 1 and significance != 2:
            prRed("[Significance error]: Significance should be a valid number, 1 or 2")
            return False
    except:
        prRed("[Significance error]: Significance should be a valid number, 1 or 2")
        return False
    return True

def validateSystematicError(
    systematic_error: str,
) -> bool:
    try:
        systematic_error = float(systematic_error)
        if systematic_error < 0 or systematic_error > 1:
            prRed("[Systematic error]: Systematic error should be a valid number between 0 and 1.")
            return False
    except:
        prRed("[Systematic error]: Systematic error should be a valid number between 0 and 1.")
        return False
    return True

def validateExtraWidth(
    extra_width: str,
):
    # validate extra width
    try:
        extra_width = float(extra_width)
    except:
        prRed("[Extra width error]: Extra width should be a valid number in GeV")
        return False
    return True