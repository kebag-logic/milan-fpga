#!/usr/bin/env python3
"""Check an author packet's INDEX.md against the files present. usage: check_packet_index.py PACKET_DIR"""
import hashlib, os, re, sys
os.chdir(sys.argv[1])
rows = re.findall(r"\| `([^`]+)` \| ([\d,]+) \| `([0-9a-f]{64})` \|", open("INDEX.md").read())
listed = {p for p, _, _ in rows}
for p, size, digest in rows:
    if not os.path.exists(p):
        print("MISSING", p)
        continue
    data = open(p, "rb").read()
    if hashlib.sha256(data).hexdigest() != digest or len(data) != int(size.replace(",", "")):
        print(f"DIFFERS {p}: listed {size} B, present {len(data)} B")
files = sorted(os.path.relpath(os.path.join(r, f)) for r, _, fs in os.walk(".") for f in fs)
print(f"rows {len(rows)}; files present {len(files)}; present but unlisted: {[f for f in files if f not in listed]}")
