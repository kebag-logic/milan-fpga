#!/usr/bin/env python3
"""Reduce dump_rows.py output to fixed-width digests (R317-1). compact_rows.py IN OUT"""
import hashlib, json, sys
data = json.loads(open(sys.argv[1]).read())
short = lambda v: v if len(v) <= 64 else "repr-sha256:" + hashlib.sha256(v.encode("utf-8", "surrogatepass")).hexdigest()[:16]
for kind in ("accepted", "mutations"):
    data[kind] = [[row[0]] + [short(v) for v in row[1:]] for row in data[kind]]
open(sys.argv[2], "w").write(json.dumps(data, indent=1) + "\n")
