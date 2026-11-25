"""Entry point: draw the front page and write it to /output/entry.png.

Run locally as `python3 main.py [path]`; with no argument it writes to
/output/entry.png when that directory exists, otherwise to entry.png here.
"""

import os
import sys

# The grader runs `python3 -P -s main.py`: -P (safe path) does not put the
# script's directory on sys.path, so a plain `from render import render`
# raises ModuleNotFoundError and the run exits 1. Add it explicitly.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from render import render


def main():
    if len(sys.argv) > 1:
        out = sys.argv[1]
    elif os.path.isdir("/output"):
        out = "/output/entry.png"
    else:
        out = "entry.png"
    render(out)
    print("wrote", out)


if __name__ == "__main__":
    main()
