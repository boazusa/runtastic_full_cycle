# args_parser.py
import argparse


def get_args():
    """Parse command-line arguments and return them."""
    parser = argparse.ArgumentParser(description="A script with flags")

    # Define flags
    parser.add_argument("-e", "--email", type=str, help="Account email", required=True)
    parser.add_argument("-p", "--password", type=str, help="Account password", required=True)
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode")

    return parser.parse_args()


# Only run this if the script is executed directly
if __name__ == "__main__":
    args = get_args()
    print(args)  # For testing purposes