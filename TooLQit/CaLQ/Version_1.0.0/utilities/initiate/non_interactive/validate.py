from utilities.data_classes import NonInteractiveInputParameters
from utilities.validate import checkIfFilesExist

def validateNonInteractiveInput(non_interactive_input_parameters: NonInteractiveInputParameters):
    """
    to valide non-interactive mode input
    """
    checkIfFilesExist([non_interactive_input_parameters.input_card_path, non_interactive_input_parameters.input_values_path])
