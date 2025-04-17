import pandas as pd
from enum import Enum

# INFRA
# coupling input params
lepton_index = 6
quark_index = 8
chirality_index = 4

# input modes
class InputMode(Enum):
    INTERACTIVE = "interactive"
    NONINTERACTIVE = "noninteractive"

# non-interactive card params
input_card_number_of_lines = 8

# interactive mode default values
default_ignore_single_pair_processes = "yes"
default_significane = 2
default_systematic_error = "0.1"
default_extra_width = 0

# FILES
DATA_PREFIX = "data"

# cross-section
def get_cross_sections_df_pair_production(model: str):
    return pd.read_csv(f"{DATA_PREFIX}/model/{model}/cross_section/pair.csv", header=[0])
def get_cross_sections_df_single_production(model: str):
    return pd.read_csv(f"{DATA_PREFIX}/model/{model}/cross_section/single.csv", header=[0])
def get_cross_sections_df_interference(model: str):
    return pd.read_csv(f"{DATA_PREFIX}/model/{model}/cross_section/interference.csv", header=[0])
def get_cross_sections_df_tchannel(model: str):
    return pd.read_csv(f"{DATA_PREFIX}/model/{model}/cross_section/tchannel.csv", header=[0])
def get_cross_sections_df_pureqcd(model: str):
    return pd.read_csv(f"{DATA_PREFIX}/model/{model}/cross_section/pureqcd.csv", header=[0])
def get_cross_sections_df_cross_terms_tchannel(model: str):
    return pd.read_csv(f"{DATA_PREFIX}/model/{model}/cross_section/tchannel_doublecoupling.csv",header=[0])

# efficiency
def get_efficiency_prefix(model: str):
    return f"{DATA_PREFIX}/model/{model}/efficiency"
def get_t_ct_prefix(model: str):
    return f"{DATA_PREFIX}/model/{model}/efficiency/t"

# LHC data
LHC_DATA_PREFIX = f"{DATA_PREFIX}/HEPdata"
lhc_data_HHbT = pd.read_csv(f"{LHC_DATA_PREFIX}/HHbT.csv", header=[0])
lhc_data_HHbV = pd.read_csv(f"{LHC_DATA_PREFIX}/HHbV.csv", header=[0])
lhc_data_LHbT = pd.read_csv(f"{LHC_DATA_PREFIX}/LHbT.csv", header=[0])
lhc_data_LHbV = pd.read_csv(f"{LHC_DATA_PREFIX}/LHbV.csv", header=[0])
lhc_data_ee = pd.read_csv(f"{LHC_DATA_PREFIX}/dielectron.csv", header=[0])
lhc_data_mumu = pd.read_csv(f"{LHC_DATA_PREFIX}/dimuon.csv", header=[0])

# tau-tau tag_names
tag_names = ["HHbT.csv", "HHbV.csv", "LHbT.csv", "LHbV.csv"]

# CALCUATION
# coupling value limits
# Currently being used for generating random coupling values
min_coupling_value_limit = -3.5
max_coupling_value_limit = 3.5

# lepton & quark masses
mass_quarks = {'1': [0.0023, 0.0048], '2': [1.275, 0.095], '3': [173.07, 4.18]}
mass_leptons = {'1': [0.000511, 2.2e-06], '2': [0.1057, 0.00017], '3': [1.777, 0.0155]}

# pureqcd contribution mass limit
pureqcd_contribution_mass_limit = 6000

# 1 sigma chi-square limits
chi_sq_limits_1 = [
    1.00,
    2.295748928898636,
    3.5267403802617303,
    4.719474460025883,
    5.887595445915204,
    7.038400923736641,
    8.176236497856527,
    9.30391276903717,
    10.423363154355838,
    11.535981713319316,
    12.64281133339149,
    13.744655587189282,
    14.842148802786893,
    15.935801892195538,
    17.026033423371082,
    18.11319133873574,
    19.197568537049687,
]

# 2 sigma chi-square limits
chi_sq_limits_2 = [
    4.00,
    6.180074306244173,
    8.024881760266252,
    9.715627154871333,
    11.313855908361862,
    12.848834791793395,
    14.337110231671799,
    15.789092974617745,
    17.21182898078949,
    18.610346565823498,
    19.988381717650192,
    21.348799569984315,
    22.693854280452445,
    24.025357063756637,
    25.344789151124267,
    26.653380234523553,
    27.952164463248984,
]

# leptoquark models
scalar_leptoquark_models = ["S1"]
vector_leptoquark_models = ["U1"]


# default luminosity values
luminosity = 139

# k-factor on the basis of proccess
k_factor_U1_pair_production = 1.5
k_factor_U1_pureqcd = 1.5
k_factor_U1_single_production = 1.0
k_factor_U1_t_channel = 1.0
k_factor_U1_interference = 1.0

# default value of input file path
default_input_file_path = "sample/sample_1.vals"

# minimum & maximum leptoquark mass allowed
minimum_leptoquark_mass = 1000.0
maximum_leptoquark_mass = 5000.0

# global data decimal precision for efficiencies & cross-sections
global_data_precision = 6
# do not keep this value below 3
number_of_minima_starting_points = 5