#!/usr/bin/env python3
"""Compare the coverage rows and campaign tallies of two hosted firmware-unit logs (dev vs head)."""
import re, sys
from pathlib import Path
MOVE = {"sw/firmware/ctrl/adp/adp.c": "third_party/tsn-c-stack/src/adp.c",
        "sw/firmware/ctrl/acmp/acmp.c": "third_party/tsn-c-stack/src/acmp.c",
        "sw/firmware/ctrl/maap/maap.c": "third_party/tsn-c-stack/src/maap.c",
        "sw/firmware/ctrl/wire/wire.h": "third_party/tsn-c-stack/include/wire.h"}
ROW = re.compile(r"Z ((?:sw|third_party)/\S+)\s+(\d+/\d+)\s+(\d+/\d+)\s+lines")
TALLY = re.compile(r"Z (.*(?:\d+ of \d+ caught|\d+/\d+ caught|caught \d+ of \d+).*)$")
def read(p):
    rows, tallies = {}, []
    for line in Path(p).read_text(errors="replace").splitlines():
        if (m := ROW.search(line)):
            rows[MOVE.get(m[1], m[1])] = (m[2], m[3])
        elif (m := TALLY.search(line)):
            tallies.append(re.sub(r"^\s+", "", m[1]))
    return rows, tallies
dev, head = read(sys.argv[1]), read(sys.argv[2])
bad = 0
for f in sorted(set(dev[0]) | set(head[0])):
    d, h = dev[0].get(f), head[0].get(f)
    flag = "same" if d == h else "DIFF"
    bad += d != h
    print(f"{flag} {f} dev={d} head={h}")
print("coverage rows:", len(dev[0]), "dev,", len(head[0]), "head,", bad, "differ")
print("dev tallies:"); [print("  ", t) for t in dev[1]]
print("head tallies:"); [print("  ", t) for t in head[1]]
