# FaceChanger
Simple script that can warp faces similar to some snapchat filters or face swaps. eyes, eyebrows, nose and mouth can all be moved and scaled interactively. The script can process the changes in real-time and works off images, videos or a live video stream from the webcam. 

## Demo
![Demo](examples/stock-example.gif)

This is a demo on a stock video from [pexels.com](https://www.pexels.com/video/man-in-white-long-sleeves-sitting-while-happily-looking-at-the-camera-5989765/).

## Usage
When running the script, the different facial features can be moved with the left mouse button and scaled with the right mouse button. You can use `./main.py -h` to get an overview of the available command line options. Here are some examples:
- `./main.py`
    - Run the program on the live feed from your webcam
- `./main.py -i examples/stock.mp4 -l -o out.mp4`
    - `-i`: Use the example stock video provided in this repository
    - `-l`: Loop the video
    - `-o`: Save the resulting video into the file out.mp4
- `./main.py -f filters/long-nose.json -s filters/my-custom-filter.json`
    - `-f`: Use the preset filter long-nose
    - `-s`: Save the interactive changes to the filter in a new file.