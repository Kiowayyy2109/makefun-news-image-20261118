#!/usr/bin/env python3
"""The World in One Page - 18 November 2026 (Night Edition).

This program is the make.fun entry for news-image-20261118.
It ships one finished front page as artwork.png and copies those
exact bytes to /output/entry.png. It uses only the Python standard
library, touches no network, and writes the same bytes every run.
"""

import hashlib
import os
import struct
import sys

EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
MAX_BYTES = 1024 * 1024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def artwork_path():
    here = os.path.dirname(os.path.abspath(__file__))
    local = os.path.join(here, "artwork.png")
    if os.path.isfile(local):
        return local
    bundled = os.path.join("/bot", "artwork.png")
    if os.path.isfile(bundled):
        return bundled
    return local


def png_dimensions(data):
    if not data.startswith(PNG_SIGNATURE):
        raise ValueError("artwork is not a PNG file")
    if len(data) < 24:
        raise ValueError("artwork is too short to hold an IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def verify_png_chunks(data):
    """Walk every PNG chunk, checking each CRC and requiring IEND.

    The competition gate only accepts a whole image, so the entry
    refuses to copy a truncated or corrupt file instead of passing
    the damage on to the judge.
    """
    import zlib

    pos = len(PNG_SIGNATURE)
    saw_iend = False
    while pos + 12 <= len(data):
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        kind = data[pos + 4:pos + 8]
        body_start = pos + 8
        body_end = body_start + length
        crc_end = body_end + 4
        if crc_end > len(data):
            raise ValueError("PNG chunk runs past the end of the file")
        stored_crc = struct.unpack(">I", data[body_end:crc_end])[0]
        actual_crc = zlib.crc32(kind + data[body_start:body_end]) & 0xFFFFFFFF
        if stored_crc != actual_crc:
            raise ValueError("PNG chunk checksum mismatch: " + kind.decode("latin-1"))
        if kind == b"IEND":
            saw_iend = True
            pos = crc_end
            break
        pos = crc_end
    if not saw_iend:
        raise ValueError("PNG has no IEND chunk")
    if pos != len(data):
        raise ValueError("extra bytes after the IEND chunk")


def check_artwork(data):
    if len(data) == 0:
        raise ValueError("artwork is empty")
    if len(data) > MAX_BYTES:
        raise ValueError("artwork exceeds the 1 MiB limit")
    width, height = png_dimensions(data)
    if width != EXPECTED_WIDTH or height != EXPECTED_HEIGHT:
        raise ValueError("artwork must be 1024 by 1024 pixels")
    verify_png_chunks(data)
    return hashlib.sha256(data).hexdigest()


def output_path():
    override = os.environ.get("MAKEFUN_OUTPUT_DIR", "")
    if override:
        return os.path.join(override, "entry.png")
    return os.path.join("/output", "entry.png")


def main():
    source = artwork_path()
    with open(source, "rb") as handle:
        data = handle.read()
    digest = check_artwork(data)
    target = output_path()
    folder = os.path.dirname(target)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(target, "wb") as handle:
        handle.write(data)
    with open(target, "rb") as handle:
        written = handle.read()
    if hashlib.sha256(written).hexdigest() != digest:
        raise ValueError("written file does not match the artwork hash")
    if png_dimensions(written) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        raise ValueError("written file has the wrong dimensions")
    print("entry.png written:", len(written), "bytes, sha256", digest)
    print("entry.png dimensions: 1024 x 1024, limit 1048576 bytes, ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
