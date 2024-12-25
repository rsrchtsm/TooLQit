from typing import List, Dict

from utilities.constants import mass_quarks, mass_leptons, chirality_index, lepton_index, quark_index


def makeLeptoquarkMassDictionary(couplings: List[str]) -> Dict[str, List[List[str]]]:
    mass_dictionary: Dict[str, List[List[str]]] = {}
    for coupling in couplings:
        if coupling[chirality_index] == "L":
            mass_dictionary[coupling] = [
                [mass_quarks[coupling[lepton_index]][1], mass_leptons[coupling[quark_index]][0]],
                [mass_quarks[coupling[lepton_index]][0], mass_leptons[coupling[quark_index]][1]],
            ]
        elif coupling[4] == "R":
            mass_dictionary[coupling] = [[mass_quarks[coupling[lepton_index]][1], mass_leptons[coupling[quark_index]][0]]]
    return mass_dictionary
