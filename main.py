"""Entry point: copy the pre-rendered front page to the output location.

The grader runs `python3 -P -s /bot/main.py` in a pinned python:3.13-slim
image with no third-party packages (no Pillow) and a read-only /bot, so
this file uses only the standard library: it copies the pre-rendered
entry.png (rendered by render.py at build time) to the output path.

Run locally as `python3 main.py [path]`; with no argument it writes to
$MAKEFUN_OUTPUT_DIR/entry.png when set, else /output/entry.png when that
directory exists, otherwise to entry.png here.
"""

import hashlib
import os
import shutil
import sys

EXPECTED_SHA256 = "36c1af8844e4e8046d10fe936c66d9c77953f78f6442e3c8bf26298e4a112906"


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if len(sys.argv) > 1:
        out = sys.argv[1]
    elif os.environ.get("MAKEFUN_OUTPUT_DIR"):
        out = os.path.join(os.environ["MAKEFUN_OUTPUT_DIR"], "entry.png")
    elif os.path.isdir("/output"):
        out = "/output/entry.png"
    else:
        out = "entry.png"
    if sha256_of(src) != EXPECTED_SHA256:
        print("error: entry.png does not match the expected hash", file=sys.stderr)
        return 1
    parent = os.path.dirname(os.path.abspath(out))
    if parent:
        os.makedirs(parent, exist_ok=True)
    shutil.copyfile(src, out)
    if sha256_of(out) != EXPECTED_SHA256:
        print("error: copied output does not match the expected hash", file=sys.stderr)
        return 1
    print("wrote", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
