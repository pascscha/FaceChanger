import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Face Changer. Let's you change your appearance in real-time.")
    parser.add_argument(
        "-f", "--filter",
        type=str,
        required=False,
        help="The path to the filter that should be used. Uses default filter, that does not change the face, if none is provided."
    )
    parser.add_argument(
        "-s", "--save",
        type=str,
        required=False,
        help="The path (JSON) where the resulting filter of the interactive session should be saved."
    )
    parser.add_argument(
        "-i", "--input",
        type=str,
        required=False,
        help="The path input file for the face change. Uses webcam if none is provided."
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        required=False,
        help="The path (MP4) where the resulting video should be saved."
    )
    args = parser.parse_args()
    print(args)