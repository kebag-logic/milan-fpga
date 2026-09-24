#!/usr/bin/env python3
"""Search every publishable packet file for the private identity tokens, in every census encoding.

Usage: leak_check_publishables.py <packet-dir> <private-benign-file> <private-token-file>...
Generic words and the adjudicated benign tokens (the DUT's own serial from
configs/, a short host role name, a numeric that matches inside timestamps)
are read from a private file and excluded; nothing about any token is printed.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from identity_census import encodings  # noqa: E402

pkt, benignfile, *tokfiles = sys.argv[1:]
toks = set()
for tf in tokfiles:
    for t in open(tf, "rb").read().split(b"\n"):
        if t and not re.fullmatch(rb"[0-9a-f]{64}", t) and len(t) < 200:
            toks.add(t)
benign = {t for t in open(benignfile, "rb").read().split(b"\n") if t}
toks -= benign
files = [os.path.join(d, f) for top in ("receipts", "scripts") for d, _, fs in os.walk(os.path.join(pkt, top)) for f in fs]
files.append(os.path.join(pkt, "REPORT.md"))
leaks = 0
for f in files:
    data = open(f, "rb").read()
    n = sum(len(rx.findall(data)) for t in toks for rx in encodings(t).values())
    leaks += n
    if n:
        print(f"LEAK {os.path.relpath(f, pkt)} occurrences {n}")
print(f"publishable files checked: {len(files)}; identity tokens searched: {len(toks)}; leak occurrences: {leaks}")
sys.exit(1 if leaks else 0)
