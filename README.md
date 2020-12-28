# FaceChanger
Simple script that can warp faces similar to some snapchat filters or face swaps. eyes, eyebrows, nose and mouth can all be moved and scaled interactively. The script can process the changes in real-time and works off images, videos or a live video stream from the webcam. 

## Demo
![Demo](examples/stock-example.gif)

This is a demo on a stock video from [pexels.com](https://www.pexels.com/video/man-in-white-long-sleeves-sitting-while-happily-looking-at-the-camera-5989765/). The different facial features can be moved with the left mouse button and scaled with the right mouse button.

## Usage
```
usage: main.py [-h] [-f FILTER] [-s SAVE] [-i INPUT] [-l] [-o OUTPUT]

Face Changer. Let's you change your appearance in real-time.

optional arguments:
  -h, --help            show this help message and exit
  -f FILTER, --filter FILTER
                        The path to the filter that should be used. Uses default filter, that does not change the face, if none is provided.
  -s SAVE, --save SAVE  The path (JSON) where the resulting filter of the interactive session should be saved.
  -i INPUT, --input INPUT
                        The path input file for the face change. Uses webcam if none is provided.
  -l, --loop            Loop the input video. If the input is an image, this flag should be set, otherwise the image will only be shown for one frame.
  -o OUTPUT, --output OUTPUT
                        The path (MP4) where the resulting video should be saved.
```