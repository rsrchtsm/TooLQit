import sympy as sym
from typing import Dict, List, Union
from sympy.utilities.iterables import flatten

from utilities.data_classes import LeptoquarkParameters, SingleCouplingCrossSections, CrossTermsCrossSections, SingleCouplingEfficiency, SingleCouplingEfficiencyTauTau, CrossTermsEfficiency, CrossTermsEfficiencyTauTau
from utilities.constants import (
    lhc_data_HHbT,
    lhc_data_HHbV,
    lhc_data_LHbT,
    lhc_data_LHbV,
    lhc_data_ee,
    lhc_data_mumu,
    k_factor_U1_pair_production,
    k_factor_U1_pureqcd,
    k_factor_U1_single_production,
    k_factor_U1_t_channel,
    k_factor_U1_interference,
    quark_index,
    tag_names,
    pureqcd_contribution_mass_limit
)

def calculateCouplingContribution(leptoquark_parameters: LeptoquarkParameters, coupling: str, symbolic_coupling: sym.Symbol, branching_fraction: sym.Symbol, cross_section: SingleCouplingCrossSections, efficiencies: SingleCouplingEfficiency) -> sym.Symbol:
    """
    Compute the chi-square polynomial for each coupling
    """
    # number of bins is the total bins efficiency was divided into during data generation
    # we take t-channel here as it is also present is efficiency is of type CrossTermsEfficiency
    number_of_bins = len(efficiencies.efficiency_tchannel)

    # initialise bins 
    pureqcd_contribution = [0.0] * number_of_bins
    pair_production_contribution = [0.0] * number_of_bins
    interference_contribution = [0.0] * number_of_bins
    tchannel_contribution = [0.0] * number_of_bins
    single_production_contribution = [0.0] * number_of_bins

    # LHC data
    standard_model_contribution = []
    nd_contribution = []
    if coupling[quark_index] == '1':
        standard_model_contribution = lhc_data_ee["Standard Model"].to_numpy()
        nd_contribution = lhc_data_ee["ND"].to_numpy()
    elif coupling[quark_index] == '2':
        standard_model_contribution = lhc_data_mumu["Standard Model"].to_numpy()
        nd_contribution = lhc_data_mumu["ND"].to_numpy()

    # common denominator
    denominator = [nd_contribution[bin_number] + leptoquark_parameters.systematic_error * leptoquark_parameters.systematic_error * nd_contribution[bin_number] ** 2 for bin_number in range(number_of_bins)]

    # k-factors initialization with default values
    k_factor_pureqcd = 1
    k_factor_pair_production = 1
    k_factor_interference = 1
    k_factor_tchannel = 1
    k_factor_single_production = 1
    if leptoquark_parameters.leptoquark_model == "S1":
        k_factor_pureqcd = k_factor_U1_pureqcd
        k_factor_pair_production =  k_factor_U1_pair_production
        k_factor_interference = k_factor_U1_interference
        k_factor_tchannel = k_factor_U1_t_channel
        k_factor_single_production = k_factor_U1_single_production

    # process wise contributions
    for bin_number in range(number_of_bins):
        # pureqcd is to be included only under a mass limit as after that its contibution will be negligible
        if leptoquark_parameters.leptoquark_mass <= pureqcd_contribution_mass_limit:
            pureqcd_contribution[bin_number] += k_factor_pureqcd * cross_section.cross_section_pureqcd * efficiencies.efficiency_pureqcd[bin_number] * branching_fraction**2 * leptoquark_parameters.luminosity * 1000 
        # pair production
        pair_production_contribution[bin_number] += k_factor_pair_production * cross_section.cross_section_pair_production * efficiencies.efficiency_pair_production[bin_number] * symbolic_coupling**4 * branching_fraction**2 * leptoquark_parameters.luminosity * 1000
        interference_contribution[bin_number] += k_factor_interference * cross_section.cross_section_interference * efficiencies.efficiency_interference[bin_number] * symbolic_coupling**2 * leptoquark_parameters.luminosity * 1000
        tchannel_contribution[bin_number] += k_factor_tchannel * cross_section.cross_section_tchannel * efficiencies.efficiency_tchannel[bin_number] * symbolic_coupling**4 * leptoquark_parameters.luminosity * 1000
        single_production_contribution[bin_number] += k_factor_single_production * cross_section.cross_section_single_production * efficiencies.efficiency_single_production[bin_number] * symbolic_coupling**2 * branching_fraction * leptoquark_parameters.luminosity * 1000

    # calculate total contribution
    total_contribution = 0.0
    for bin_number in range(number_of_bins):
        if leptoquark_parameters.ignore_single_pair_processes:
            total_contribution += (
                pureqcd_contribution[bin_number] + pair_production_contribution[bin_number] + interference_contribution[bin_number] + tchannel_contribution[bin_number] + single_production_contribution[bin_number] + standard_model_contribution[bin_number] - nd_contribution[bin_number]
            )**2 / (denominator[bin_number])
        else:
            total_contribution += (
                pureqcd_contribution[bin_number] + pair_production_contribution[bin_number] + interference_contribution[bin_number] + tchannel_contribution[bin_number] + single_production_contribution[bin_number] + standard_model_contribution[bin_number] - nd_contribution[bin_number]
            )**2 / (denominator[bin_number])
    
    return sym.simplify(total_contribution)

def calculateCouplingContributionCrossTerms(leptoquark_parameters: LeptoquarkParameters, coupling1: str, coupling2: str, symbolic_coupling1: sym.Symbol, symbolic_coupling2: sym.Symbol, cross_section: CrossTermsCrossSections, efficiencies: CrossTermsEfficiency) -> sym.Symbol:
    """
    Compute the chi-square polynomial for each coupling
    """
    # number of bins is the total bins efficiency was divided into during data generation
    # we take t-channel here as it is also present is efficiency is of type CrossTermsEfficiency
    number_of_bins = len(efficiencies.efficiency_tchannel)

    # initialise bins 
    cross_terms_tchannel_contribution = [0.0] * number_of_bins

    # LHC data
    standard_model_contribution = []
    nd_contribution = []
    if coupling1[quark_index] == '1':
        standard_model_contribution = lhc_data_ee["Standard Model"].to_numpy()
        nd_contribution = lhc_data_ee["ND"].to_numpy()
    elif coupling1[quark_index] == '2':
        standard_model_contribution = lhc_data_mumu["Standard Model"].to_numpy()
        nd_contribution = lhc_data_mumu["ND"].to_numpy()

    # common denominator
    denominator = [nd_contribution[bin_number] + leptoquark_parameters.systematic_error * leptoquark_parameters.systematic_error * nd_contribution[bin_number] ** 2 for bin_number in range(number_of_bins)]

    # k-factors initialization with default values
    k_factor_tchannel = 1
    if leptoquark_parameters.leptoquark_model == "U1":
        k_factor_tchannel = k_factor_U1_t_channel

    # process wise contributions
    for bin_number in range(number_of_bins):
        cross_terms_tchannel_contribution[bin_number] += k_factor_tchannel * cross_section.cross_terms_cross_section_tchannel * efficiencies.efficiency_tchannel[bin_number] * symbolic_coupling1**2 * symbolic_coupling2**2 * leptoquark_parameters.luminosity * 1000

    # calculate total contribution
    total_contribution = 0.0
    for bin_number in range(number_of_bins):
        total_contribution += (
            cross_terms_tchannel_contribution[bin_number] + standard_model_contribution[bin_number] - nd_contribution[bin_number]
        )**2 / (denominator[bin_number])
    
    return sym.simplify(total_contribution)


def calculateCouplingContributionTauTau(leptoquark_parameters: LeptoquarkParameters, coupling: str, symbolic_coupling: sym.Symbol, branching_fraction: sym.Symbol, cross_section: Union[SingleCouplingCrossSections, CrossTermsCrossSections], efficiencies: Union[SingleCouplingEfficiencyTauTau, CrossTermsEfficiencyTauTau]) -> sym.Symbol:
    """
    Compute the chi-square polynomial for each coupling
    """
    # number of bins is the total bins efficiency was divided into during data generation
    # we take t-channel here as it is also present is efficiency is of type CrossTermsEfficiency
    total_contribution = 0.0
    for tag_name in tag_names:
        number_of_bins = 0
        if tag_name == "HHbT.csv":
            number_of_bins = len(efficiencies.efficiency_tchannel.hhbt)
        elif tag_name == "HHbV.csv":
            number_of_bins = len(efficiencies.efficiency_tchannel.hhbv)
        elif tag_name == "LHbT.csv":
            number_of_bins = len(efficiencies.efficiency_tchannel.lhbt)
        elif tag_name == "LHbV.csv":
            number_of_bins = len(efficiencies.efficiency_tchannel.lhbv)

        # initialise bins 
        pureqcd_contribution = [0.0] * number_of_bins
        pair_production_contribution = [0.0] * number_of_bins
        interference_contribution = [0.0] * number_of_bins
        tchannel_contribution = [0.0] * number_of_bins
        single_production_contribution = [0.0] * number_of_bins

        # LHC data
        standard_model_contribution = []
        nd_contribution = []
        if tag_name == "HHbT.csv":
            standard_model_contribution = lhc_data_HHbT["Standard Model"].to_numpy()
            nd_contribution = lhc_data_HHbT["ND"].to_numpy()
        elif tag_name == "HHbV.csv":
            standard_model_contribution = lhc_data_HHbV["Standard Model"].to_numpy()
            nd_contribution = lhc_data_HHbV["ND"].to_numpy()
        elif tag_name == "LHbT.csv":
            standard_model_contribution = lhc_data_LHbT["Standard Model"].to_numpy()
            nd_contribution = lhc_data_LHbT["ND"].to_numpy()
        elif tag_name == "LHbV.csv":
            standard_model_contribution = lhc_data_LHbV["Standard Model"].to_numpy()
            nd_contribution = lhc_data_LHbV["ND"].to_numpy()

        # common denominator
        denominator = [nd_contribution[bin_number] + leptoquark_parameters.systematic_error * leptoquark_parameters.systematic_error * nd_contribution[bin_number] ** 2 for bin_number in range(number_of_bins)]

        # k-factors initialization with default values
        k_factor_pureqcd = 1
        k_factor_pair_production = 1
        k_factor_interference = 1
        k_factor_tchannel = 1
        k_factor_single_production = 1
        if leptoquark_parameters.leptoquark_model == "U1":
            k_factor_pureqcd = k_factor_U1_pureqcd
            k_factor_pair_production =  k_factor_U1_pair_production
            k_factor_interference = k_factor_U1_interference
            k_factor_tchannel = k_factor_U1_t_channel
            k_factor_single_production = k_factor_U1_single_production

        # process wise contributions
        for bin_number in range(number_of_bins):
            if tag_name == "HHbT.csv":
                # pureqcd is to be included only under a mass limit as after that its contibution will be negligible
                if leptoquark_parameters.leptoquark_mass <= pureqcd_contribution_mass_limit:
                    pureqcd_contribution[bin_number] += k_factor_pureqcd * cross_section.cross_section_pureqcd * efficiencies.efficiency_pureqcd.hhbt[bin_number] * branching_fraction**2 * leptoquark_parameters.luminosity * 1000
                pair_production_contribution[bin_number] += k_factor_pair_production * cross_section.cross_section_pair_production * efficiencies.efficiency_pair_production.hhbt[bin_number] * symbolic_coupling**4 * branching_fraction**2 * leptoquark_parameters.luminosity * 1000
                interference_contribution[bin_number] += k_factor_interference * cross_section.cross_section_interference * efficiencies.efficiency_interference.hhbt[bin_number] * symbolic_coupling**2 * leptoquark_parameters.luminosity * 1000
                tchannel_contribution[bin_number] += k_factor_tchannel * cross_section.cross_section_tchannel * efficiencies.efficiency_tchannel.hhbt[bin_number] * symbolic_coupling**4 * leptoquark_parameters.luminosity * 1000
                single_production_contribution[bin_number] += k_factor_single_production * cross_section.cross_section_single_production * efficiencies.efficiency_single_production.hhbt[bin_number] * symbolic_coupling**2 * branching_fraction * leptoquark_parameters.luminosity * 1000
            elif tag_name == "HHbV.csv":
                # pureqcd is to be included only under a mass limit as after that its contibution will be negligible
                if leptoquark_parameters.leptoquark_mass <= pureqcd_contribution_mass_limit:
                    pureqcd_contribution[bin_number] += k_factor_pureqcd * cross_section.cross_section_pureqcd * efficiencies.efficiency_pureqcd.hhbv[bin_number] * branching_fraction**2 * leptoquark_parameters.luminosity * 1000
                pair_production_contribution[bin_number] += k_factor_pair_production * cross_section.cross_section_pair_production * efficiencies.efficiency_pair_production.hhbv[bin_number] * symbolic_coupling**4 * branching_fraction**2 * leptoquark_parameters.luminosity * 1000
                interference_contribution[bin_number] += k_factor_interference * cross_section.cross_section_interference * efficiencies.efficiency_interference.hhbv[bin_number] * symbolic_coupling**2 * leptoquark_parameters.luminosity * 1000
                tchannel_contribution[bin_number] += k_factor_tchannel * cross_section.cross_section_tchannel * efficiencies.efficiency_tchannel.hhbv[bin_number] * symbolic_coupling**4 * leptoquark_parameters.luminosity * 1000
                single_production_contribution[bin_number] += k_factor_single_production * cross_section.cross_section_single_production * efficiencies.efficiency_single_production.hhbv[bin_number] * symbolic_coupling**2 * branching_fraction * leptoquark_parameters.luminosity * 1000
            elif tag_name == "LHbT.csv":
                # pureqcd is to be included only under a mass limit as after that its contibution will be negligible
                if leptoquark_parameters.leptoquark_mass <= pureqcd_contribution_mass_limit:
                    pureqcd_contribution[bin_number] += k_factor_pureqcd * cross_section.cross_section_pureqcd * efficiencies.efficiency_pureqcd.lhbt[bin_number] * branching_fraction**2 * leptoquark_parameters.luminosity * 1000
                pair_production_contribution[bin_number] += k_factor_pair_production * cross_section.cross_section_pair_production * efficiencies.efficiency_pair_production.lhbt[bin_number] * symbolic_coupling**4 * branching_fraction**2 * leptoquark_parameters.luminosity * 1000
                interference_contribution[bin_number] += k_factor_interference * cross_section.cross_section_interference * efficiencies.efficiency_interference.lhbt[bin_number] * symbolic_coupling**2 * leptoquark_parameters.luminosity * 1000
                tchannel_contribution[bin_number] += k_factor_tchannel * cross_section.cross_section_tchannel * efficiencies.efficiency_tchannel.lhbt[bin_number] * symbolic_coupling**4 * leptoquark_parameters.luminosity * 1000
                single_production_contribution[bin_number] += k_factor_single_production * cross_section.cross_section_single_production * efficiencies.efficiency_single_production.lhbt[bin_number] * symbolic_coupling**2 * branching_fraction * leptoquark_parameters.luminosity * 1000
            elif tag_name == "LHbV.csv":
                # pureqcd is to be included only under a mass limit as after that its contibution will be negligible
                if leptoquark_parameters.leptoquark_mass <= pureqcd_contribution_mass_limit:
                    pureqcd_contribution[bin_number] += k_factor_pureqcd * cross_section.cross_section_pureqcd * efficiencies.efficiency_pureqcd.lhbv[bin_number] * branching_fraction**2 * leptoquark_parameters.luminosity * 1000
                pair_production_contribution[bin_number] += k_factor_pair_production * cross_section.cross_section_pair_production * efficiencies.efficiency_pair_production.lhbv[bin_number] * symbolic_coupling**4 * branching_fraction**2 * leptoquark_parameters.luminosity * 1000
                interference_contribution[bin_number] += k_factor_interference * cross_section.cross_section_interference * efficiencies.efficiency_interference.lhbv[bin_number] * symbolic_coupling**2 * leptoquark_parameters.luminosity * 1000
                tchannel_contribution[bin_number] += k_factor_tchannel * cross_section.cross_section_tchannel * efficiencies.efficiency_tchannel.lhbv[bin_number] * symbolic_coupling**4 * leptoquark_parameters.luminosity * 1000
                single_production_contribution[bin_number] += k_factor_single_production * cross_section.cross_section_single_production * efficiencies.efficiency_single_production.lhbv[bin_number] * symbolic_coupling**2 * branching_fraction * leptoquark_parameters.luminosity * 1000

        # calculate total contribution
        for bin_number in range(number_of_bins):
            if leptoquark_parameters.ignore_single_pair_processes:
                total_contribution += (
                    pureqcd_contribution[bin_number] + pair_production_contribution[bin_number] + interference_contribution[bin_number] + tchannel_contribution[bin_number] + single_production_contribution[bin_number] + standard_model_contribution[bin_number] - nd_contribution[bin_number]
                )**2 / (denominator[bin_number])
            else:
                total_contribution += (
                    pureqcd_contribution[bin_number] + pair_production_contribution[bin_number] + interference_contribution[bin_number] + tchannel_contribution[bin_number] + single_production_contribution[bin_number] + standard_model_contribution[bin_number] - nd_contribution[bin_number]
                )**2 / (denominator[bin_number])
        total_contribution = sym.simplify(total_contribution)
    
    return sym.simplify(total_contribution)

def calculateCouplingContributionTauTauCrossTerms(leptoquark_parameters: LeptoquarkParameters, coupling1: str, coupling2: str, symbolic_coupling1: sym.Symbol, symbolic_coupling2: sym.Symbol, cross_section: CrossTermsCrossSections, efficiencies: CrossTermsEfficiencyTauTau) -> sym.Symbol:
    """
    Compute the chi-square polynomial for each coupling
    """
    # number of bins is the total bins efficiency was divided into during data generation
    # we take t-channel here as it is also present is efficiency is of type CrossTermsEfficiency
    total_contribution = 0.0
    for tag_name in tag_names:
        number_of_bins = 0
        if tag_name == "HHbT.csv":
            number_of_bins = len(efficiencies.efficiency_tchannel.hhbt)
        elif tag_name == "HHbV.csv":
            number_of_bins = len(efficiencies.efficiency_tchannel.hhbv)
        elif tag_name == "LHbT.csv":
            number_of_bins = len(efficiencies.efficiency_tchannel.lhbt)
        elif tag_name == "LHbV.csv":
            number_of_bins = len(efficiencies.efficiency_tchannel.lhbv)

        # initialise bins 
        cross_terms_tchannel_contribution = [0.0] * number_of_bins

        # LHC data
        standard_model_contribution = []
        nd_contribution = []
        if tag_name == "HHbT.csv":
            standard_model_contribution = lhc_data_HHbT["Standard Model"].to_numpy()
            nd_contribution = lhc_data_HHbT["ND"].to_numpy()
        elif tag_name == "HHbV.csv":
            standard_model_contribution = lhc_data_HHbV["Standard Model"].to_numpy()
            nd_contribution = lhc_data_HHbV["ND"].to_numpy()
        elif tag_name == "LHbT.csv":
            standard_model_contribution = lhc_data_LHbT["Standard Model"].to_numpy()
            nd_contribution = lhc_data_LHbT["ND"].to_numpy()
        elif tag_name == "LHbV.csv":
            standard_model_contribution = lhc_data_LHbV["Standard Model"].to_numpy()
            nd_contribution = lhc_data_LHbV["ND"].to_numpy()

        # common denominator
        denominator = [nd_contribution[bin_number] + leptoquark_parameters.systematic_error * leptoquark_parameters.systematic_error * nd_contribution[bin_number] ** 2 for bin_number in range(number_of_bins)]

        # k-factors initialization with default values
        k_factor_tchannel = 1
        if leptoquark_parameters.leptoquark_model == "U1":
            k_factor_tchannel = k_factor_U1_t_channel

        # process wise contributions
        for bin_number in range(number_of_bins):
            if tag_name == "HHbT.csv":
                cross_terms_tchannel_contribution[bin_number] += k_factor_tchannel * cross_section.cross_terms_cross_section_tchannel * efficiencies.efficiency_tchannel.hhbt[bin_number] * symbolic_coupling1**2 * symbolic_coupling2**2 * leptoquark_parameters.luminosity * 1000
            elif tag_name == "HHbV.csv":
                cross_terms_tchannel_contribution[bin_number] += k_factor_tchannel * cross_section.cross_terms_cross_section_tchannel * efficiencies.efficiency_tchannel.hhbv[bin_number] * symbolic_coupling1**2 * symbolic_coupling2**2 * leptoquark_parameters.luminosity * 1000
            elif tag_name == "LHbT.csv":
                cross_terms_tchannel_contribution[bin_number] += k_factor_tchannel * cross_section.cross_terms_cross_section_tchannel * efficiencies.efficiency_tchannel.lhbt[bin_number] * symbolic_coupling1**2 * symbolic_coupling2**2 * leptoquark_parameters.luminosity * 1000
            elif tag_name == "LHbV.csv":
                cross_terms_tchannel_contribution[bin_number] += k_factor_tchannel * cross_section.cross_terms_cross_section_tchannel * efficiencies.efficiency_tchannel.lhbv[bin_number] * symbolic_coupling1**2 * symbolic_coupling2**2 * leptoquark_parameters.luminosity * 1000

        # calculate total contribution
        for bin_number in range(number_of_bins):
            total_contribution += (
                cross_terms_tchannel_contribution[bin_number] + standard_model_contribution[bin_number] - nd_contribution[bin_number]
            )**2 / (denominator[bin_number])
        total_contribution = sym.simplify(total_contribution)
    
    return sym.simplify(total_contribution)

def getChiSquareSymbolic(leptoquark_parameters: LeptoquarkParameters, branching_fraction: sym.Symbol, coupling_to_process_cross_section_map: Dict[str, Union[SingleCouplingCrossSections, CrossTermsCrossSections]], coupling_to_process_efficiencies_map: Dict[str, Union[SingleCouplingEfficiency, SingleCouplingEfficiencyTauTau, CrossTermsEfficiency, CrossTermsEfficiencyTauTau]], symbolic_couplings: List[sym.Symbol], print_output: bool) -> sym.Symbol:
    """
    Compute the chi-square polynomial
    """
    chi_square: sym.Symbol = 0

    # calculate single coupling contribution
    for coupling, symbolic_coupling, in zip(leptoquark_parameters.sorted_couplings, symbolic_couplings):
        if coupling[quark_index] == '3':
            chi_square = chi_square + calculateCouplingContributionTauTau(
                leptoquark_parameters, coupling, symbolic_coupling, branching_fraction, coupling_to_process_cross_section_map[coupling], coupling_to_process_efficiencies_map[coupling]
            )
        else:
            chi_square = chi_square + calculateCouplingContribution(
                leptoquark_parameters, coupling, symbolic_coupling, branching_fraction, coupling_to_process_cross_section_map[coupling], coupling_to_process_efficiencies_map[coupling]
            )
        if print_output:
            print(f"{coupling} contributions calculated!!")
    
    # calculate cross-terms contribution
    for i in range(len(leptoquark_parameters.sorted_couplings)):
        for j in range(i+1, len(leptoquark_parameters.sorted_couplings)):
            # if couplings belong to the same category
            if leptoquark_parameters.sorted_couplings[i][quark_index] == leptoquark_parameters.sorted_couplings[j][quark_index]:
                cross_terms_coupling = f"{leptoquark_parameters.sorted_couplings[i]}_{leptoquark_parameters.sorted_couplings[j]}"
                if coupling[quark_index] == '3':
                    chi_square = chi_square + calculateCouplingContributionTauTauCrossTerms(
                        leptoquark_parameters, leptoquark_parameters.sorted_couplings[i], leptoquark_parameters.sorted_couplings[j], symbolic_couplings[i], symbolic_couplings[j], coupling_to_process_cross_section_map[cross_terms_coupling], coupling_to_process_efficiencies_map[cross_terms_coupling]
                    )
                else:
                    chi_square = chi_square + calculateCouplingContributionCrossTerms(
                        leptoquark_parameters, leptoquark_parameters.sorted_couplings[i], leptoquark_parameters.sorted_couplings[j], symbolic_couplings[i], symbolic_couplings[j], coupling_to_process_cross_section_map[cross_terms_coupling], coupling_to_process_efficiencies_map[cross_terms_coupling]
                    )
                if print_output:
                    print(f"{cross_terms_coupling} contributions calculated!!")

    return sym.simplify(chi_square)

