#!/usr/bin/env python3
from facechanger.utils import parse_args
from facechanger.user_input import UserInputHandler
import dlib

if __name__ == "__main__":
    args = parse_args()

    input_handler = UserInputHandler(args.filter)
    face_detector = dlib.get_frontal_face_detector()
    feature_detector = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

