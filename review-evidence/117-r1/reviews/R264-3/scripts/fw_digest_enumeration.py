#!/usr/bin/env python3
"""Does the page's 64-octet firmware-field digest fall to a small enumeration?

Usage: fw_digest_enumeration.py DIGEST
Enumerates zero-padded 64-octet fields holding version-shaped strings
(d.dd.dd, d.d.d, dd.dd.dd, d.dd.ddd) and reports only whether a unique match
exists and how many candidates were tried. The matching value is never printed.
"""
import hashlib, itertools, sys

target = sys.argv[1]
shapes = [(1, 2, 2), (1, 1, 1), (2, 2, 2), (1, 2, 3), (1, 1, 2), (1, 2, 1)]
tried = found = 0
for a, b, c in shapes:
    for x in itertools.product(range(10 ** a), range(10 ** b), range(10 ** c)):
        s = f"{x[0]:0{a}d}.{x[1]:0{b}d}.{x[2]:0{c}d}".encode()
        tried += 1
        if hashlib.sha256(s + b"\0" * (64 - len(s))).hexdigest() == target:
            found += 1
print(f"candidates_tried={tried} matches={found} value=<withheld>")
