#!/usr/bin/env python3
from facechanger import utils
from facechanger import constants
from facechanger.transform import transform

import json
import cv2
from warnings import warn
import os
import numpy as np

import dlib

def detect_features(img, face_detector, feature_detector):
    """Detects facial features from a given image
    """
    gray = cv2.cvtColor(src=img, code=cv2.COLOR_BGR2GRAY)
    faces = face_detector(gray)
    if len(faces) > 0:
        face = faces[0]
    
        landmarks = feature_detector(image=gray, box=face)
        landmark_list = []
        for n in range(0, 68):
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            landmark_list.append((x,y))

        # Mirror lower head around x-axis, in order to also include hairline, as landmarks only include chin otherwise
        highest_y = np.array(landmark_list)[constants.LOWER_HEAD].min(axis=0)[1]
        for i in constants.LOWER_HEAD:
            landmark_list.append((landmark_list[i][0], max(1,2*highest_y-landmark_list[i][1])))

        return np.array(landmark_list)
    else:
        return None

def zoom(points, factor):
    """Zoom the points by the given factor, with the anchor at the center.
    """
    center = np.mean(points, axis=0)
    return (points-center)*factor + center

def get_new_features(features, filter):
    """Apply filter to features
    """
    new_features = features.copy()

    for k, v in filter.items():
        indices = constants.INDICES[k]
        new_features[indices] = zoom(new_features[indices], v["zoom"]) + v["trans"]
    
    return np.array(new_features)

if __name__ == "__main__":
    args = utils.parse_args()
    
    # Download facial features detection model if necessary
    if not os.path.exists("shape_predictor_68_face_landmarks.dat"):
        warn("Could not find face prediction model, trying to download it from https://github.com/italojs/facial-landmarks-recognition/blob/master/shape_predictor_68_face_landmarks.dat?raw=true. This may take a while.")
        import requests
        data = requests.get("https://github.com/italojs/facial-landmarks-recognition/blob/master/shape_predictor_68_face_landmarks.dat?raw=true").content
        with open("shape_predictor_68_face_landmarks.dat", "wb") as f:
            f.write(data)

    # Set up face detector
    face_detector = dlib.get_frontal_face_detector()
    feature_detector = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    # Set up user input handler
    ui_handler = utils.UserInputHandler(args.filter)

    # Set up opencv window
    windowname = "FaceChanger"
    cv2.namedWindow(windowname, cv2.WINDOW_GUI_NORMAL)
    cv2.resizeWindow(windowname, 1000,1000)
    cv2.setMouseCallback(windowname, ui_handler.click)

    # Set video output if required
    if args.output is not None:
        fourcc = cv2.VideoWriter_fourcc(*'MP4V')

    out = None

    # Start video capturing
    cap = cv2.VideoCapture(args.input)

    try:
        while True:
            # Read input
            success, img = cap.read()
            if not success:
                if args.loop:
                    cap = cv2.VideoCapture(args.input)
                    success, img = cap.read()
                    if not success:
                        raise Exception("Error while reading stream")
                else:
                    break # Input finished
            
            features = detect_features(img, face_detector, feature_detector)
            if features is not None:
                new_features = get_new_features(features, ui_handler.get_filter())
                ui_handler.features = new_features
                new_img = transform(img, features, new_features)

                # Start video output
                if args.output is not None:   
                    if out is None:
                        height, width, channels = new_img.shape
                        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                        out = cv2.VideoWriter(args.output, fourcc, 20, (width, height))
                    out.write(new_img)
            else:
                new_img = img  
            cv2.imshow("FaceChanger", new_img)
            key = cv2.waitKey(1)
    except KeyboardInterrupt:
        print("Thanks, bye")
    finally:
        cap.release()
        if out is not None:
            out.release()
        if args.save is not None:
            with open(args.save, "w+") as f:
                json.dump(ui_handler.get_filter(), f, indent=1)
