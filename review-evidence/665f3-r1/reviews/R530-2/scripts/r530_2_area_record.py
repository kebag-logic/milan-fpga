#!/usr/bin/env python3
"""Re-derive the round-3 area record's arithmetic from docs/design/MAILBOX_SPLIT.md
at the exact head (the table 'LUT before | round 2 | round 3 | FF ...').
Usage: r530_2_area_record.py <clone>"""
import re, sys
from pathlib import Path
t = Path(sys.argv[1], "docs/design/MAILBOX_SPLIT.md").read_text()
rows = {}
for line in t.splitlines():
    m = re.match(r"\| (`KL_mbx[^|]*|\*\*Total\*\*) \|" + r" ([\d,*]+) \|" * 6, line)
    if m:
        name = m.group(1).strip()
        vals = [int(v.replace(",", "").replace("*", "")) for v in m.groups()[1:]]
        rows[name] = vals
for k, v in rows.items():
    print(f"{k:42s} {v}")
tot = rows.pop("**Total**")
s = [sum(v[i] for v in rows.values()) for i in range(6)]
print("sum of listed blocks:", s)
print("total minus listed (blocks not in the table): LUT", [tot[i] - s[i] for i in range(3)], "FF", [tot[i] - s[i] for i in range(3, 6)])
print("round-3 delta over FC r2: LUT", tot[2] - tot[0], "FF", tot[5] - tot[3])
print("round-2 delta over FC r2: LUT", tot[1] - tot[0], "FF", tot[4] - tot[3])
per = {k: v[2] - v[0] for k, v in rows.items()}
print("per-block round-3 LUT deltas:", per, "unlisted:", (tot[2] - s[2]) - (tot[0] - s[0]))
print("breakdown 64 + 22 + 271 =", 64 + 22 + 271, "; SRL16E 128 / 2 =", 128 // 2, "; (34 RAMD32 + 10 RAMS32) / 2 =", (34 + 10) // 2)
print("target check: LUT", tot[2] - tot[0], "<= 300 ?", tot[2] - tot[0] <= 300, "; FF", tot[5] - tot[3], "<= 120 ?", tot[5] - tot[3] <= 120)
