#!/usr/bin/env python3
from facechanger.utils import parse_args
from facechanger.input_handler import InputHandler

if __name__ == "__main__":
    args = parse_args()
    input_handler = InputHandler(args.filter)