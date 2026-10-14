#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Remove transient build products and normalize generated runtime metadata."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
import shutil
import struct
import sys


def java_store(path: Path, epoch: int) -> None:
    """Normalize certificate-entry dates in the distribution's JKS trust store."""
    if not path.exists():
        return
    data = bytearray(path.read_bytes())
    magic, version, count = struct.unpack_from(">III", data)
    if (magic, version) != (0xFEEDFEED, 2):
        raise ValueError("unexpected Java trust-store format")
    offset = 12
    for _ in range(count):
        kind = struct.unpack_from(">I", data, offset)[0]
        offset += 4
        if kind != 2:
            raise ValueError("trust store contains a non-certificate entry")
        length = struct.unpack_from(">H", data, offset)[0]
        offset += 2 + length
        struct.pack_into(">Q", data, offset, epoch * 1000)
        offset += 8
        length = struct.unpack_from(">H", data, offset)[0]
        offset += 2 + length
        length = struct.unpack_from(">I", data, offset)[0]
        offset += 4 + length
    if offset != len(data) - 20:
        raise ValueError("unexpected trust-store trailer")
    data[-20:] = hashlib.sha1("changeit".encode("utf-16-be") + b"Mighty Aphrodite" + data[:-20]).digest()
    path.write_bytes(data)


def normalize(root: Path, epoch: int) -> None:
    """Discard bytecode and make file ownership and mtimes independent of builds."""
    for path in sorted(root.rglob("*"), reverse=True):
        if path.is_symlink():
            continue
        if path.name == "__pycache__" and path.is_dir():
            shutil.rmtree(path)
        elif path.suffix == ".pyc" and path.is_file():
            path.unlink()
    for path in [root, *root.rglob("*")]:
        if path.is_mount():
            continue
        os.chown(path, 0, 0, follow_symlinks=False)
        os.utime(path, (epoch, epoch), follow_symlinks=False)


def main() -> int:
    """Normalize a tool prefix or the package installer's transient files."""
    epoch = int(os.environ["SOURCE_DATE_EPOCH"])
    if sys.argv[1] == "system":
        for name in ("/var/log", "/var/cache/fontconfig", "/var/cache/ldconfig",
                     "/var/cache/apt", "/var/lib/apt/lists"):
            path = Path(name)
            shutil.rmtree(path, ignore_errors=True)
            path.mkdir(parents=True, exist_ok=True)
        java_store(Path("/etc/ssl/certs/java/cacerts"), epoch)
        for name in ("/usr", "/var", "/etc"):
            normalize(Path(name), epoch)
    else:
        normalize(Path(sys.argv[1]), epoch)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
