# Calculator Imports
import sys
import argparse

from utilities.data_classes import NonInteractiveInputParameters
from utilities.welcome import printBanner
from utilities.initiate.non_interactive.non_interactive import initiateNonInteractive
from utilities.initiate.interactive.interactive import  initiateInteractive
from utilities.constants import default_input_file_path

# calq execution starts here
def main():
    """
    Calq starting function that parses command line argument 
    """
    # argparser for CLI arguments
    parser = argparse.ArgumentParser(description="CaLQ Usage:")
    # for choosing interactive/non-interactive modes
    parser.add_argument(
        "--non-interactive",
        "-ni",
        action="store_true",
        help="Run in non-interactive mode. This requires input-card and input-values to be specified.",
    )
    # wheter to display banner from banner.txt
    parser.add_argument(
        "--no-banner", "-nb", action="store_true", help="CaLQ banner is not printed."
    )
    # non-interactive mode parameters
    parser.add_argument(
        "--input-card",
        type=str,
        default="",
        help="[filename]: Input card file. Format is explained in README.txt",
    )
    parser.add_argument(
        "--input-values",
        type=str,
        default="",
        help="[filename]: Input values to check from the given file. Format is explained in README.txt",
    )
    parser.add_argument(
        "--output-yes",
        type=str,
        default="calq_yes.csv",
        help="[filename]: Specify the name of output file (allowed values) (overwrites the existing file). Default: calq_yes.csv",
    )
    parser.add_argument(
        "--output-no",
        type=str,
        default="calq_no.csv",
        help="[filename]: Specify the name of output file (disallowed values) (overwrites the existing file). Default: calq_no.csv",
    )
    parser.add_argument(
        "--output-common",
        type=str,
        default="calq_common.csv",
        help="[filename]: Specify the name of output file (overwrites the existing file). Default: calq_common.csv",
    )

    # parse args
    args = parser.parse_args()

    if not args.no_banner:
        printBanner()

    if args.non_interactive:
        non_interactive_input_parameters = NonInteractiveInputParameters(
            input_card_path = args.input_card, 
            input_values_path = args.input_values, 
            output_yes_path = args.output_yes, 
            output_no_path = args.output_no, 
            output_common_path=args.output_common,
        )
        nonInteractiveMessage(
            non_interactive_input_parameters
        )
        initiateNonInteractive(
            non_interactive_input_parameters
        )
    else:
        initiateInteractive()


def nonInteractiveMessage(
    non_interactive_input_parameters: NonInteractiveInputParameters,
):
    """
    Print an initial message for non-interactive mode
    """
    if not non_interactive_input_parameters.input_card_path:
        sys.exit(
            "[Card error]: Input Card file not specified in the expected format (mandatory for non-interactive mode). Exiting.\n"
        )
    if not non_interactive_input_parameters.input_values_path:
        non_interactive_input_parameters.input_values_path = default_input_file_path
        with open(non_interactive_input_parameters.input_card_path, encoding="utf8") as c:
            input_card_lines = c.readlines()
            random_points = input_card_lines[7].split("#")[0].strip()
            if random_points == '0':
                sys.exit(
                    "[Values error]: Input Values file not specified & random points is set to zero. Exiting.\n"
                )
    print(f"Input Card file: {non_interactive_input_parameters.input_card_path}")
    print(f"Input Values file: {non_interactive_input_parameters.input_values_path}")
    print(f"Output Yes file: {non_interactive_input_parameters.output_yes_path}")
    print(f"Output No file: {non_interactive_input_parameters.output_no_path}")
    print(f"Output Common file: {non_interactive_input_parameters.output_common_path}")


try:
    main()
except KeyboardInterrupt:
    sys.exit("\n\nKeyboardInterrupt recieved. Exiting.")
