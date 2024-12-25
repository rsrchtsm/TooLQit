import sys
from typing import Any
from functools import cmp_to_key

from utilities.constants import lepton_index, quark_index, chirality_index
from utilities.data_classes import LeptoquarkParameters


def compareCouplings(item1: Any, item2: Any) -> int:
    """
    Use this function as the comparator function while sorting lambdas
    """
    a1 = list(item1[0])
    a2 = list(item2[0])
    if a1[quark_index] != a2[quark_index]:
        return ord(a1[quark_index]) - ord(a2[quark_index])
    if a1[chirality_index] == a2[chirality_index]:
        return ord(a1[lepton_index]) - ord(a2[lepton_index])
    return -1 if a1[chirality_index] == "L" else 1


def sortCouplingsAndValues(
    leptoquark_parameters: LeptoquarkParameters
):
    """
    Sort coupling and values so that the correct efficiency files can be read
    """
    for line_number, coupling_value in enumerate(leptoquark_parameters.couplings_values):
        if len(coupling_value) != len(leptoquark_parameters.couplings):
            sys.exit(f"[Query error]: Coupling values length in line {line_number+1} is {coupling_value} which does not match the length of input couplings {leptoquark_parameters.couplings}")
        combined_couplings_and_values = zip(leptoquark_parameters.couplings, coupling_value)
        sorted_combined_couplings_and_values = sorted(combined_couplings_and_values, key=cmp_to_key(compareCouplings))
        sorted_combined_couplings_and_values = list(zip(*sorted_combined_couplings_and_values))
        leptoquark_parameters.sorted_couplings = list(sorted_combined_couplings_and_values[0])
        leptoquark_parameters.sorted_couplings_values.append(list(sorted_combined_couplings_and_values[1]))

def sortCouplingsAndValuesInteractive(
    leptoquark_parameters: LeptoquarkParameters
):
    """
    Sort coupling and values so that the correct efficiency files can be read for interactive mode
    """
    for _, coupling_value in enumerate(leptoquark_parameters.couplings_values):
        combined_couplings_and_values = zip(leptoquark_parameters.couplings, coupling_value)
        sorted_combined_couplings_and_values = sorted(combined_couplings_and_values, key=cmp_to_key(compareCouplings))
        sorted_combined_couplings_and_values = list(zip(*sorted_combined_couplings_and_values))
        leptoquark_parameters.sorted_couplings = list(sorted_combined_couplings_and_values[0])
        leptoquark_parameters.sorted_couplings_values.append(list(sorted_combined_couplings_and_values[1]))