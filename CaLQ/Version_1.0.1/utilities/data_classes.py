from typing import List


class LeptoquarkParameters:
    """
    class for all parameters required for calculation. This class will have all the values that are user-inputted
    """
    def __init__(
        self,
        leptoquark_model: str = '',
        leptoquark_mass: float = 0.0,
        ignore_single_pair_processes: bool = False,
        significance: int = 0,
        systematic_error: float = 0.0,
        extra_width: float = 0.0,
        luminosity: float = 0.0,
        couplings: List[str] = [],
        couplings_values: List[List[float]] = [],
        sorted_couplings: List[str] = [],
        sorted_couplings_values: List[List[float]] = [],
    ):
        self.leptoquark_model = leptoquark_model
        self.leptoquark_mass = leptoquark_mass
        self.couplings = couplings
        self.ignore_single_pair_processes = ignore_single_pair_processes
        self.significance = significance
        self.systematic_error = systematic_error
        self.extra_width = extra_width
        self.luminosity = luminosity
        self.couplings_values = couplings_values
        self.sorted_couplings = sorted_couplings
        self.sorted_couplings_values = sorted_couplings_values

    def __str__(self):
        return (
            f"Leptoquark Model: {self.leptoquark_model}\n"
            f"Leptoquark Mass: {self.leptoquark_mass} GeV\n"
            f"Ignore Single/Pair Processes: {self.ignore_single_pair_processes}\n"
            f"Significance: {self.significance}\n"
            f"Systematic error: {self.systematic_error * 100:.2f}%\n"
            f"Extra Width: {self.extra_width} GeV\n"
            f"Luminosity: {self.luminosity} fb^-1\n"
            f"Couplings: {self.couplings}\n"
            f"Couplings Values: {self.couplings_values}\n"
            f"Sorted Couplings: {self.sorted_couplings}\n"
            f"Sorted Couplings Values: {self.sorted_couplings_values}"
        )


class NonInteractiveInputParameters:
    """
    class for non-interactive mode input parameters to be taken from the user

    :param input_card_path: File path to the .card file for non-interactive input
    :param input_values_path: File path to the .vals file(values file) for non-interactive input
    :param output_yes_path: File path of the output file (allowed values)
    :param output_no_path: File path of the output file (disallowed values)
    """
    def __init__(
        self,
        input_card_path: str = "",
        input_values_path: str = "",
        output_yes_path: str = "",
        output_no_path: str = "",
        output_common_path: str = "",
    ):
        self.input_card_path = input_card_path
        self.input_values_path = input_values_path
        self.output_yes_path = output_yes_path
        self.output_no_path = output_no_path
        self.output_common_path = output_common_path


class SingleCouplingCrossSections:
    def __init__(
        self,
        cross_section_pureqcd: float,
        cross_section_pair_production: float,
        cross_section_single_production: float,
        cross_section_interference: float,
        cross_section_tchannel: float,
    ):
        self.cross_section_pureqcd = cross_section_pureqcd
        self.cross_section_pair_production = cross_section_pair_production
        self.cross_section_single_production = cross_section_single_production
        self.cross_section_interference = cross_section_interference
        self.cross_section_tchannel = cross_section_tchannel

    def __str__(self):
        return (
            f"Cross Section Pure QCD: {self.cross_section_pureqcd}\n"
            f"Cross Section Pair Production: {self.cross_section_pair_production}\n"
            f"Cross Section Single Production: {self.cross_section_single_production}\n"
            f"Cross Section Interference: {self.cross_section_interference}\n"
            f"Cross Section T-Channel: {self.cross_section_tchannel}"
        )

class CrossTermsCrossSections:
    def __init__(
        self,
        cross_terms_cross_section_tchannel: float, # the cross-section to be used for cross-terms
        actual_cross_section_tchannel: float, # the cross-section when 2 couplings are switched on
    ):
        self.cross_terms_cross_section_tchannel = cross_terms_cross_section_tchannel
        self.actual_cross_section_tchannel = actual_cross_section_tchannel

    def __str__(self):
        return (
            f"Cross-Terms Cross Section T-Channel: {self.cross_terms_cross_section_tchannel}\n"
            f"Actual Cross Section T-Channel: {self.actual_cross_section_tchannel}"
        )


class SingleCouplingEfficiency:
    def __init__(
        self,
        efficiency_pureqcd: List[float],
        efficiency_pair_production: List[float],
        efficiency_single_production: List[float],
        efficiency_interference: List[float],
        efficiency_tchannel: List[float],
    ):
        self.efficiency_pureqcd = efficiency_pureqcd
        self.efficiency_pair_production = efficiency_pair_production
        self.efficiency_single_production = efficiency_single_production
        self.efficiency_interference = efficiency_interference
        self.efficiency_tchannel = efficiency_tchannel

    def __str__(self):
        return (
            f"Efficiency Pure QCD: {self.efficiency_pureqcd}\n"
            f"Efficiency Pair Production: {self.efficiency_pair_production}\n"
            f"Efficiency Single Production: {self.efficiency_single_production}\n"
            f"Efficiency Interference: {self.efficiency_interference}\n"
            f"Efficiency T-Channel: {self.efficiency_tchannel}"
        )

class CrossTermsEfficiency:
    # This will only have t channel for now
    def __init__(
        self,
        efficiency_tchannel: List[float],
    ):
        self.efficiency_tchannel = efficiency_tchannel
        
class TagsTauTau:
    def __init__(
        self,
        hhbt: List[float],
        hhbv: List[float],
        lhbt: List[float],
        lhbv: List[float],
    ):
        self.hhbt = hhbt
        self.hhbv = hhbv
        self.lhbt = lhbt
        self.lhbv = lhbv

class SingleCouplingEfficiencyTauTau:
    def __init__(
        self,
        efficiency_pureqcd: TagsTauTau,
        efficiency_pair_production: TagsTauTau,
        efficiency_single_production: TagsTauTau,
        efficiency_interference: TagsTauTau,
        efficiency_tchannel: TagsTauTau,
    ):
        self.efficiency_pureqcd = efficiency_pureqcd
        self.efficiency_pair_production = efficiency_pair_production
        self.efficiency_single_production = efficiency_single_production
        self.efficiency_interference = efficiency_interference
        self.efficiency_tchannel = efficiency_tchannel

class CrossTermsEfficiencyTauTau:
    # This will only have t channel for now
    def __init__(
        self,
        efficiency_tchannel: TagsTauTau,
    ):
        self.efficiency_tchannel = efficiency_tchannel