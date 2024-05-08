# Basic Cursor Detector (BCD)

[![bcd](https://img.shields.io/badge/bcd-v0.1-blue)](https://www.youtube.com/watch?v=dQw4w9WgXcQ)

Implements a basic multi-scale cursor detection using openCV.

## Features:

1. Works across multiple scales.
2. Works (at all!) (see below)

<img width="659" alt="image" src="https://github.com/Evanc123/mouse-detection/assets/4010547/e2eb6f01-9c43-4c80-934c-f2a019ef06aa">

To view the processed video, please check [this link](videos/processed_video.mp4).

## Limitations:

1. May not function effectively on non-white backgrounds, though conversion to grayscale could mitigate this issue (results may vary).
2. Performance is fucked

## Installation

Install using `uv` and run using `python`.

```shell

#If you haven't installed UV yet, run the following command:
curl -LsSf https://astral.sh/uv/install.sh | sh

# create a venv with uv

uv venv

# activate venv

source .venv/bin/activate

# install reqs (just opencv)

uv pip install -r requirements.txt

# run the thing

python main.py

# hit space or any key when you are done viewing the image
```

## To run on a video

```shell
python video.py

# Or, if you want to parallelize the processing, 

# this has a dependency on FFMPEG - if you don't have it installed on your machine, install it
python paralell_video.py
```
My m2 does a 7 second 2.5k video @ 30 fps in about 8 minutes using the parallelized script
