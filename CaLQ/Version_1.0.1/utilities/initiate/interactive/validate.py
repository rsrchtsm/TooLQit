from utilities.constants import scalar_leptoquark_models, vector_leptoquark_models, minimum_leptoquark_mass, maximum_leptoquark_mass
from utilities.colour import prRed
from utilities.colour import prBlue


def validateLeptoQuarkModel(leptoquark_model: str,) -> bool:
    if leptoquark_model not in scalar_leptoquark_models and leptoquark_model not in vector_leptoquark_models:
        prRed(f"[input_model error -- {leptoquark_model}]: Not a valid lepqtoquark model. Allowed models: {scalar_leptoquark_models + vector_leptoquark_models}")
        return False
    
    prBlue("Leptoquark model updated!")
    prBlue("Please update the couplings if necessary.") 
    prBlue("(Scalar LQ couplings -> Y****[i,j] ---  Vector LQ couplings -> X****[i,j] )")
    return True


def validateLeptoQuarkMass(
    leptoquark_mass: str, 
) -> bool:
    try:
        leptoquark_mass = float(leptoquark_mass)
        if leptoquark_mass < minimum_leptoquark_mass or leptoquark_mass > maximum_leptoquark_mass:
            prRed(f"[mass error]: Leptoquark mass should be between {minimum_leptoquark_mass} GeV and {maximum_leptoquark_mass} GeV")
            return False
    except:
        prRed("[mass error]: Leptoquark mass should be a valid number")
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
            prRed(f"[ couplings error -- {item} ]: Multiple occurances of the input coupling was found! \nEach coupling can only be provided once.")
            return False
        else:
            frequency[item] = 1

    if not len(couplings_list):
        prRed("[couplings error]: Couplings cannot be empty!")
        return False
    
    for i in range(len(couplings_list)):
        if len(couplings_list[i]) != 10:
            prRed(f"[ couplings error -- {couplings_list[i]} ]: The input coupling is formatted incorrectly (not 10 characters)! \nor the correct formatting, refer to README.md file.")
            return False
        
        if not (
            (couplings_list[i][0] == 'Y' and leptoquark_model in scalar_leptoquark_models)
            or (couplings_list[i][0] == 'X' and leptoquark_model in vector_leptoquark_models)
        ):
            prRed(f"[ couplings error -- {couplings_list[i]} ]: Invalid input coupling for the LQ model! \n\nFor scalar leptoquarks, the first letter should be Y. \nFor vector leptoquarks, it should be X. \n\nRefer to README.md for the valid format.")
            return False
        
        if couplings_list[i][1:3] != "10":
            prRed(f"[ couplings error -- {couplings_list[i]} ]: Invalid coupling format for weak representation and type of LQ ---  current model coverage dictates first letter (X/Y) should be followed by '10'. \nFor the correct formatting, refer to README.md file.")
            return False

        if couplings_list[i][3] not in ["L", "R"] or couplings_list[i][4] not in ["L", "R"]:
            prRed(f"[ couplings error -- {couplings_list[i]} ]: The 4th, 5th characters of input couplings should be either L (indicating left-handed) & or R (right-handed) denoting chirality. \n For the correct formatting, please refer to README.md file.")
            return False
        
        # [v1 specific] error message
        if (couplings_list[i][3] == "L" and couplings_list[i][4] == "R") or (couplings_list[i][3] == "R" and couplings_list[i][4] == "L"):
            prRed(f"[ couplings error -- {couplings_list[i]} ]: Invalid coupling entered for U1/S1 model! (Mixed chiralities) \nFor the allowed set of couplings, please refer to the TooLQit manual [arXiv:2412.19729].")
            return False
        
        if couplings_list[i][5] != '[':
            prRed(f"[ couplings error -- {couplings_list[i]} ]: Fermion generation information should be enclosed in square brackets! \nPlease refer to README.md for valid format")
            return False
        
        if couplings_list[i][6] not in ["1", "2", "3"]:
            prRed(f"[ couplings error -- {couplings_list[i]}]: Invalid quark generation input for the coupling! (Valid values are 1, 2, and 3.)")
            return False
        
        if couplings_list[i][8] not in ["1", "2", "3"]:
            prRed(f"[ couplings error -- {couplings_list[i]}]: Invalid lepton generation input for the coupling! (Valid values are 1, 2, and 3.)")
            return False
        
        # [v1 specific] error message
        if (leptoquark_model in scalar_leptoquark_models and couplings_list[i][6] == "3"):
            prRed(f"[ couplings error -- {couplings_list[i]} ]: For scalar LQ S1, third-generation-quark couplings are not covered in the current version. \nPlease choose another coupling. \n(For more information, please refer to the TooLQit manual [arXiv:2412.19729].)")
            return False

        if couplings_list[i][7] != ',':
            prRed(f"[ couplings error -- {couplings_list[i]} ]: Lepton and quark generations need to comma-separated!")
            return False
        
        if couplings_list[i][9] != ']':
            prRed(f"[ couplings error -- {couplings_list[i]} ]: Generation information should be enclosed in square brackets. For valid format, refer to README.md file.")
            return False

    return True


def validateIgnoreSinglePairProduction(
    ignore_single_pair_processes: str, 
) -> bool:
    if ignore_single_pair_processes.lower() in {"yes", "y", "no", "n"}:
        return True
    prRed("[ignore_single_pair error]: ignore_single_pair takes input 'yes'/'y' or 'no'/'n'")
    return False

def validateSignificance(
    significance: str, 
) -> bool:
    try:
        significance = int(significance)
        if significance != 1 and significance != 2:
            prRed("[significance error]: Significance should be a valid number, 1 or 2")
            return False
    except:
        prRed("[significance error]: Significance should be a valid number, 1 or 2")
        return False
    return True

def validateSystematicError(
    systematic_error: str,
) -> bool:
    try:
        systematic_error = float(systematic_error)
        if systematic_error < 0 or systematic_error > 1:
            prRed("[systematic_error error]: Systematic error should be a valid number between 0 and 1.")
            return False
    except:
        prRed("[systematic_error error]: Systematic error should be a valid number between 0 and 1.")
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