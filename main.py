#!/usr/bin/env python3
"""Entry point for the 18 November 2026 one-image news summary.

The artwork is a finished 1024x1024 PNG that sits next to this file as
artwork.png. Running this program publishes that exact file to
/output/entry.png. No network, no randomness, no clock reads: the
output bytes are the artwork bytes, every single run.
"""

import hashlib
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "artwork.png")
DEST_DIR = "/output"
DEST = os.path.join(DEST_DIR, "entry.png")
MAX_BYTES = 1024 * 1024
EXPECTED_W = 1024
EXPECTED_H = 1024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def read_source():
    with open(SOURCE, "rb") as handle:
        return handle.read()


def check_png_header(data):
    if not data.startswith(PNG_SIGNATURE):
        raise ValueError("artwork is not a PNG file")
    # IHDR is the first chunk: length (4), type (4), then width/height.
    if data[12:16] != b"IHDR":
        raise ValueError("PNG is missing its IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def check_png_chunks(data):
    """Walk every chunk so a truncated or padded file is rejected.

    A PNG is a signature followed by length/type/payload/CRC records.
    The walk must land exactly on the end of the data, and the final
    chunk seen must be IEND, otherwise the image is not complete.
    """
    offset = len(PNG_SIGNATURE)
    seen_types = []
    while offset < len(data):
        if offset + 8 > len(data):
            raise ValueError("truncated PNG chunk header at %d" % offset)
        (length,) = struct.unpack(">I", data[offset : offset + 4])
        chunk_type = data[offset + 4 : offset + 8]
        end = offset + 8 + length + 4
        if end > len(data):
            raise ValueError("truncated PNG chunk %r" % chunk_type)
        seen_types.append(chunk_type)
        offset = end
    if offset != len(data):
        raise ValueError("PNG has trailing bytes after the last chunk")
    if not seen_types or seen_types[-1] != b"IEND":
        raise ValueError("PNG does not end with an IEND chunk")
    if b"IDAT" not in seen_types:
        raise ValueError("PNG carries no image data (IDAT) chunk")
    return seen_types


def validate(data):
    if len(data) == 0:
        raise ValueError("artwork is empty")
    if len(data) > MAX_BYTES:
        raise ValueError("artwork exceeds the 1 MiB limit: %d bytes" % len(data))
    width, height = check_png_header(data)
    if (width, height) != (EXPECTED_W, EXPECTED_H):
        raise ValueError(
            "artwork must be %dx%d, got %dx%d"
            % (EXPECTED_W, EXPECTED_H, width, height)
        )
    check_png_chunks(data)
    return width, height


def publish(data):
    """Write via a sibling temp file, then rename over the destination.

    The rename keeps a reader from ever seeing a half-written entry,
    and the bytes that land are exactly the bytes that were validated.
    """
    tmp_path = DEST + ".tmp"
    with open(tmp_path, "wb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(tmp_path, DEST)


def main():
    data = read_source()
    width, height = validate(data)
    digest_before = hashlib.sha256(data).hexdigest()
    os.makedirs(DEST_DIR, exist_ok=True)
    publish(data)
    with open(DEST, "rb") as handle:
        written = handle.read()
    if hashlib.sha256(written).hexdigest() != digest_before:
        raise RuntimeError("written file does not match the artwork hash")
    if written != data:
        raise RuntimeError("written file is not a byte-for-byte copy")
    print(
        "entry.png written: %dx%d, %d bytes, sha256=%s"
        % (width, height, len(written), digest_before)
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
