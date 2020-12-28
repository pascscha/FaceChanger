#!/usr/bin/env python3
from facechanger.utils import parse_args
from facechanger.user_input import UserInputHandler
import cv2
from warnings import warn
import os

import dlib

if __name__ == "__main__":
    args = parse_args()
    
    # Download facial features detection model if necessary
    if not os.path.exists("shape_predictor_68_face_landmarks.dat"):
        warn("Could not find face prediction model, trying to download it from https://github.com/italojs/facial-landmarks-recognition/blob/master/shape_predictor_68_face_landmarks.dat?raw=true. This may take a while.")
        import requests
        data = requests.get("https://github.com/italojs/facial-landmarks-recognition/blob/master/shape_predictor_68_face_landmarks.dat?raw=true").content
        with open("shape_predictor_68_face_landmarks.dat", "wb") as f:
            f.write(data)

    face_detector = dlib.get_frontal_face_detector()
    feature_detector = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    ui_handler = UserInputHandler(args.filter)

    windowname = "FaceChanger"
    cv2.namedWindow(windowname, cv2.WINDOW_GUI_NORMAL)
    cv2.resizeWindow(windowname, 1000,1000)
    cv2.setMouseCallback(windowname, ui_handler.click)

    cap = cv2.VideoCapture(args.input)

    while True:
        success, img = cap.read()
        if not success:
            if args.loop:
                cap = cv2.VideoCapture(args.input)
                success, img = cap.read()
                if not success:
                    raise Exception("Error while reading stream")
            else:
                break # Input finished
        cv2.imshow("FaceChanger", img)
        key = cv2.waitKey(1)

