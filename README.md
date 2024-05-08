# Basic Cursor Detector (BCD)

[![bcd](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/Evanc123/mouse-detection)

Implements a basic multi-scale cursor detection using openCV.

## Features:

1. Works across multiple scales.
2. Works!

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
