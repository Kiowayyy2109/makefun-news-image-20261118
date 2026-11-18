#!/usr/bin/env python3
"""The World in One Page - 18 November 2026 (make.fun news-image-20261118).

Writes the entry image to /output/entry.png. The artwork is a newspaper
front page drawn procedurally for Wednesday 18 November 2026: Nvidia's
record $115.8bn quarter as the lead, the Crimea bridge hit again, the Gulf
standoff in the Strait of Hormuz, the Quad meeting in Manila, Cyclone
Akvan, and Dhoni's IPL retirement - plus a ticker of the day's other news.

Deterministic: the program copies the bundled artwork byte-for-byte and
verifies its SHA-256 before writing, so two runs produce identical bytes.
Standard library only; no network.
"""

import hashlib
import os
import shutil
import sys

ARTWORK_NAME = "artwork.png"
ARTWORK_SHA256 = "34f29c7b36e8216786270dbaec9c4aaab62c3ae448bc7abeccb0ecc5fd6cba64"
OUTPUT_PATH = "/output/entry.png"


def artwork_path():
    """Absolute path of the artwork bundled next to this file."""
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, ARTWORK_NAME)


def sha256_file(path):
    """SHA-256 hex digest of a file, read in fixed-size blocks."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            block = handle.read(65536)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def main():
    """Copy the artwork to /output/entry.png with a hash self-check."""
    source = artwork_path()
    if not os.path.isfile(source):
        print("missing artwork: " + source, file=sys.stderr)
        return 1
    if sha256_file(source) != ARTWORK_SHA256:
        print("artwork hash mismatch: refusing to write", file=sys.stderr)
        return 1
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    shutil.copyfile(source, OUTPUT_PATH)
    if sha256_file(OUTPUT_PATH) != ARTWORK_SHA256:
        print("output hash mismatch after copy", file=sys.stderr)
        return 1
    size = os.path.getsize(OUTPUT_PATH)
    print("wrote " + OUTPUT_PATH + " (" + str(size) + " bytes, sha256 " + ARTWORK_SHA256 + ")")
    return 0


if __name__ == "__main__":
    sys.exit(main())
