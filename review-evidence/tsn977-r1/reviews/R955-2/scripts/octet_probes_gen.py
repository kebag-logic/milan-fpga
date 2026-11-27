#!/usr/bin/env python3
"""Generate one probe per term of record_moved's 20-octet compare (term -> 0u).
Usage: octet_probes_gen.py TREE OUT_JSON"""
import json, re, sys
from pathlib import Path
src = (Path(sys.argv[1]) / "src/acmp.c").read_text()
body = src[src.index("static bool record_moved"):]
body = body[:body.index("return diff != 0u;")]
expr = body[body.index("uint32_t diff = ") + len("uint32_t diff = "):]
terms = [t.strip() for t in re.split(r"\s\|\s|\s\|\n", expr.rstrip().rstrip(";")) if t.strip()]
probes = []
for i, t in enumerate(terms):
    m = re.search(r"p\[(\d+)\]", t)
    octet = int(m.group(1))
    assert src.count(t) == 1, t
    probes.append({"name": f"r2-record-omit-p{octet}", "old": t, "new": "0u"})
assert len(probes) == 20, len(probes)
Path(sys.argv[2]).write_text(json.dumps(probes, indent=1) + "\n")
print(len(probes), "probes")
