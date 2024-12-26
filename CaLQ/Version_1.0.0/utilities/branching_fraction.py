import math
from typing import Dict, List
import sympy as sym

from utilities.data_classes import LeptoquarkParameters
from utilities.constants import chirality_index


def momentum(leptoquark_mass: float, quark_mass: float, lepton_mass: float):
    a = math.pow(leptoquark_mass + lepton_mass, 2) - math.pow(quark_mass, 2)
    b = math.pow(leptoquark_mass - lepton_mass, 2) - math.pow(quark_mass, 2)
    return math.sqrt(a * b) / (2 * leptoquark_mass)


def absoluteeEfficiencyCouplingMassFactor(leptoquark_mass: float, quark_mass: float, lepton_mass: float):
    return (
        math.pow(leptoquark_mass, 2)
        - (math.pow(lepton_mass, 2) + math.pow(quark_mass, 2))
        - math.pow((math.pow(lepton_mass, 2) - math.pow(quark_mass, 2)), 2) / math.pow(leptoquark_mass, 2)
        - (6 * lepton_mass * quark_mass)
    )


def U1DecayWidthMassFactor(leptoquark_mass: float, mass_dictionary: List[float]):
    return (
        momentum(leptoquark_mass, mass_dictionary[0], mass_dictionary[1])
        * absoluteeEfficiencyCouplingMassFactor(leptoquark_mass, mass_dictionary[0], mass_dictionary[1])
        / (8 * math.pow(math.pi, 2) * math.pow(leptoquark_mass, 2))
    )

def S1DecayWidthMassFactor(leptoquark_mass: float, mass_dictionary: List[float]):
    quark_mass = mass_dictionary[0]
    lepton_mass = mass_dictionary[1]
    return (math.pow(leptoquark_mass, 2) - math.pow(lepton_mass + quark_mass, 2)) * (math.sqrt((math.pow(leptoquark_mass, 2) - math.pow(lepton_mass + quark_mass, 2)) * (math.pow(leptoquark_mass, 2) - math.pow(lepton_mass - quark_mass, 2)))) / (8 * math.pi * math.pow(leptoquark_mass, 3))
    


# Calculate branching fraction using decay_width
def getBranchingFraction(leptoquark_parameters: LeptoquarkParameters, symbolic_couplings: List[sym.Symbol], mass_dictionary: Dict[str, List[List[str]]]) -> sym.Symbol:
    numerator: sym.Symbol = 0
    denominator: sym.Symbol = leptoquark_parameters.extra_width
    for coupling, symbolic_coupling in zip(leptoquark_parameters.sorted_couplings, symbolic_couplings):
        if leptoquark_parameters.leptoquark_model == "U1":
            denominator += symbolic_coupling ** 2 * U1DecayWidthMassFactor(leptoquark_parameters.leptoquark_mass, mass_dictionary[coupling][0])
            numerator += symbolic_coupling ** 2 * U1DecayWidthMassFactor(leptoquark_parameters.leptoquark_mass, mass_dictionary[coupling][0])
            if coupling[chirality_index] == 'L':
                denominator += symbolic_coupling ** 2 * U1DecayWidthMassFactor(leptoquark_parameters.leptoquark_mass, mass_dictionary[coupling][1])
        elif leptoquark_parameters.leptoquark_model == "S1":
            denominator += symbolic_coupling ** 2 * S1DecayWidthMassFactor(leptoquark_parameters.leptoquark_mass, mass_dictionary[coupling][0])
            numerator += symbolic_coupling ** 2 * S1DecayWidthMassFactor(leptoquark_parameters.leptoquark_mass, mass_dictionary[coupling][0])
            if coupling[chirality_index] == 'L':
                denominator += symbolic_coupling ** 2 * S1DecayWidthMassFactor(leptoquark_parameters.leptoquark_mass, mass_dictionary[coupling][1])
    
    return numerator/denominator