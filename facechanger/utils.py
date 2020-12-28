import argparse
import os
import json
from types import SimpleNamespace
from warnings import warn

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
        "-l", "--loop",
        action="store_true",
        help="Loop the input video. If the input is an image, this option should be set, otherwise the image will only be shown for one frame."
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        required=False,
        help="The path (MP4) where the resulting video should be saved."
    )
    args = parser.parse_args()

    processed = SimpleNamespace()

    if args.filter is not None:
        if not os.path.exists(args.filter):
            parser.error("The provided filter path does not exist.")
        else:
            with open(args.filter) as f:
                try:
                    processed.filter = json.load(f)
                except json.decoder.JSONDecodeError:
                    parser.error("The provided filter is not a valid JSON file.")            
    else:
        with open(os.path.join("facechanger","filters","default.json")) as f:
            processed.filter = json.load(f)

    if args.save is not None:
        if not args.save.lower().endswith(".json"):
            warn("The save path for the filter does not end in .json, the resulting file will be a JSON file nevertheless.")
    processed.save = args.save

    if args.input is not None:
        if not os.path.exists(args.input):
            parser.error("The provided input path does not exist.")
        processed.input = args.input
    else:
        processed.input = 0 # Use webcam
    
    processed.loop = args.loop

    if args.output is not None:
        if not args.save.lower().endswith(".mp4"):
            warn("The save path for the video file does not end in .mp4, the resulting file will be a MP4 file nevertheless.")
    processed.output = args.output

    return processed

