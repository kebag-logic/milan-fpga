#!/usr/bin/env python3
"""Match each 'rv32 at ... text=' line of a ctrl_nvm suite log to the README
"Static sizes" row with the same bss, and compare every shared column.
usage: match_sizes.py <suite log> <sw/firmware/ctrl_nvm/README.md>"""
import re, sys
log, readme = open(sys.argv[1]).read(), open(sys.argv[2]).read()
meas = [dict(re.findall(r"(\w+)=(\d+)", m.group(0)), hz=m.group(1))
        for m in re.finditer(r"rv32 at (\d+) Hz: (.*)", log)]
sec = readme.split("## Static sizes", 1)[1].split("\n## ", 1)[0]
rows = [[c.strip().strip("`").replace(",", "") for c in l.strip("|").split("|")]
        for l in sec.splitlines() if l.startswith("| `")]
cols = ["shape", "hz", "records", "container", "stage", "payload", "chunk", "store", "clock", "bss", "text"]
rows = [dict(zip(cols, r)) for r in rows]
bad = 0
if len(meas) != 5 or len(rows) != 5: print(f"count mismatch: {len(meas)} measured, {len(rows)} rows"); bad = 1
for m in meas:
    hit = [r for r in rows if r["bss"] == m["bss"]]
    if len(hit) != 1: print("no unique row for bss", m["bss"]); bad = 1; continue
    r = hit[0]
    for k in ("hz", "stage", "payload", "chunk", "store", "clock", "bss", "text"):
        ok = r[k] == m[k]; bad |= not ok
        print(f"{r['shape']:28s} {k:8s} table={r[k]:>10s} measured={m[k]:>10s} {'OK' if ok else 'MISMATCH'}")
print("RESULT:", "MISMATCH" if bad else "ALL MATCH"); sys.exit(bad)
