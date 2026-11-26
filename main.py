#!/usr/bin/env python3
"""Entry for news-image-20261126: copy the bundled front page to the output dir.

Standard library only. No network, no randomness.
Reads entry.png sitting next to this file and writes it to
$MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png),
then verifies the copy byte for byte.
"""

import hashlib
import os
import shutil
import sys

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
SOURCE_NAME = "entry.png"


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, SOURCE_NAME)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    dest = os.path.join(out_dir, SOURCE_NAME)

    if not os.path.isfile(source):
        print("error: bundled %s not found next to main.py" % SOURCE_NAME,
              file=sys.stderr)
        return 1

    with open(source, "rb") as handle:
        magic = handle.read(len(PNG_MAGIC))
    if magic != PNG_MAGIC:
        print("error: bundled %s is not a PNG file" % SOURCE_NAME,
              file=sys.stderr)
        return 1

    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(source, dest)

    src_size = os.path.getsize(source)
    dst_size = os.path.getsize(dest)
    if src_size != dst_size:
        print("error: size mismatch after copy (%d != %d)"
              % (src_size, dst_size), file=sys.stderr)
        return 1
    with open(dest, "rb") as handle:
        dest_magic = handle.read(len(PNG_MAGIC))
    if dest_magic != PNG_MAGIC:
        print("error: copied file lost its PNG header", file=sys.stderr)
        return 1
    if sha256_of(source) != sha256_of(dest):
        print("error: checksum mismatch after copy", file=sys.stderr)
        return 1

    print("wrote %s (%d bytes, sha256 %s)"
          % (dest, dst_size, sha256_of(dest)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
