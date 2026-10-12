#!/usr/bin/env python3
"""Check each published RAM ledger row and independently recompute the measured-lane correction."""
from pathlib import Path
import re
paths=[Path("docs/design/AREA_BUDGET.md"),Path("docs/design/MARK_II_AREA_PLAN.md")]
ledgers=[]
for path in paths:
 text=path.read_text();block=text.split("| Item | RAMB36 delta | RAMB18 delta | Tile delta | Image tiles after |",1)[1].split("\n\n",1)[0]
 rows=[];total=0.0
 for line in block.splitlines():
  if not line.startswith("| ") or line.startswith("|---"):continue
  name,r36,r18,delta,after=[v.strip() for v in line.strip("|").split("|")]
  r36,r18,delta,after=map(float,[r36,r18,delta,after])
  assert r36+r18/2 == delta,(name,delta)
  total+=delta;assert total==after,(name,total,after)
  rows.append((name,delta,total));print(path,name,delta,total)
 assert total==113
 ledgers.append(rows)
assert ledgers[0]==ledgers[1]
assert 121.5-113 == 8.5
assert 113+(56-53)==116 and 121.5-116==5.5
assert 124+6==130 and 130-121.5==8.5
assert 124+(54.5-53)-11==114.5
text=paths[1].read_text()
assert all(token in text for token in ["M2 (34)","M5 (121)","M6 (418)","38,784, 744 over 38,040"])
partial_planned=37957
partial_measured=partial_planned+(200-34)+(600-121)+(600-418)
assert partial_measured==38784 and partial_measured-38040==744
print("PASS measured M2/M5/M6 replacement: 37957 + 166 + 479 + 182 = 38784; 744 over target")
print("PASS historical mapped memory ledger arithmetic; this does not remeasure current firmware mapping")
