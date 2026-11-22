#!/usr/bin/env python3
"""Rebuild a GNU-gzip (level 6, FNAME, Unix) file from decompressed content for each mtime in a window and report
the mtime whose bytes hash to the target sha256. Usage: gz_header_search.py <file.gz> <name> <target-sha256> <lo> <hi>
A target of 'self' validates the method on <file.gz> itself, using its own header mtime."""
import gzip, hashlib, struct, subprocess, sys
src, name, target, lo, hi = sys.argv[1], sys.argv[2].encode(), sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
raw = open(src, "rb").read()
content = gzip.decompress(raw)
body = subprocess.run(["gzip", "-6", "-n", "-c"], input=content, capture_output=True, check=True).stdout[10:]
if target == "self":
    target = hashlib.sha256(raw).hexdigest(); lo = hi = struct.unpack("<I", raw[4:8])[0]
for mt in range(lo, hi + 1):
    head = b"\x1f\x8b\x08\x08" + struct.pack("<I", mt) + b"\x00\x03" + name + b"\x00"
    if hashlib.sha256(head + body).hexdigest() == target:
        print(f"{src}: reproduced with GNU gzip -6, name {name.decode()!r}, mtime {mt}; {len(head)+len(body)} B -> {target}")
        sys.exit(0)
print(f"{src}: no mtime in [{lo}, {hi}] reproduces {target}")
sys.exit(1)
