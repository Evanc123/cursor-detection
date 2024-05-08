# Basic Cursor Detector (BCD)

Implements a basic multi-scale cursor detection using openCV.


## Features:

1. Works across multiple scales.
2. Works! (see below)

<img width="659" alt="image" src="https://github.com/Evanc123/mouse-detection/assets/4010547/e2eb6f01-9c43-4c80-934c-f2a019ef06aa">


## Limitations:

1. May not function effectively on non-white backgrounds, though conversion to grayscale could mitigate this issue (results may vary).
2. Performance is significantly slow.
   To Run:

## Installation

Install using `uv` and run using `python`.

```shell

#If you haven't installed UV yet, run the following command:
curl -LsSf https://astral.sh/uv/install.sh | sh

# activate venv

source .venv/bin/activate

# install reqs (just opencv)

uv pip install -r requirements.txt

# run the thing

uv python main.py

# hit space or any key when you are done viewing the image
```
