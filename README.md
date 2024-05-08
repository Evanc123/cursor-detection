Implements very rudimentary multi-scale cursor detection using openCV

features:

1. works for multiple scales

limitations:

1. probably doesn't work for non white backgrounds (although it goes grayscale so maybe its fine, YMMV)
2. slow as shit (like really slow)

To Run:

# install uv if you haven't (if you haven't wut r u doing)

`curl -LsSf https://astral.sh/uv/install.sh | sh`

# activate venv

`source .venv/bin/activate`

# install reqs (just opencv)

`uv pip install -r requirements.txt`

# run the thing

`uv python main.py`
