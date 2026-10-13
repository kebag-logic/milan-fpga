#!/usr/bin/env python3
"""R624-5: is the line-3200 row of check_b16_figures.py sensitive to B-CRF's own window LOCKED count?

usage: probe_row3200.py <repo> <author packet> <scratch dir> <out.json>

Copies the packet, changes only r2/bcrf-poll-receipt.json's window LOCKED count (596 -> 595), runs the
packet's check on the unchanged page, and reports each row's status on lines 3008, 3174 and 3200.
A row that recomputes B-CRF's count must turn MISMATCH; the 3200 row's key reads only B-AAF's receipt.
"""
import json, shutil, subprocess, sys
from pathlib import Path

repo, packet, scratch, out = (Path(a).resolve() for a in sys.argv[1:5])
cp = scratch / "pkt-row3200"
if cp.exists():
    shutil.rmtree(cp)
shutil.copytree(packet, cp)
f = cp / "r2/bcrf-poll-receipt.json"
d = json.loads(f.read_text())
w = d["spans"]["window-start..window-end"]
assert w["servo"] == {"LOCKED": 596}, w["servo"]
w["servo"] = {"LOCKED": 595, "ACQUIRE": 1}
f.write_text(json.dumps(d, indent=1))
page = repo / "docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md"
p = subprocess.run([sys.executable, "-I", str(cp / "tools/check_b16_figures.py"), str(page), str(cp),
                    str(scratch / "row3200-rows.tsv"), str(scratch / "row3200-cov.tsv")],
                   capture_output=True, text=True, timeout=600)
rows = [l.split("\t") for l in (scratch / "row3200-rows.tsv").read_text().splitlines() if not l.startswith("#")]
sel = [r for r in rows if r[1] in ("3015", "3181", "3207") and r[2] == "596" or (r[1] in ("3015",) and r[2] == "three")]
res = {"rc": p.returncode, "summary": json.loads(p.stdout.splitlines()[0]),
       "rows": [{"row": r[0], "line": r[1], "shown": r[2], "receipt": r[3], "recomputed": r[5], "status": r[6]} for r in sel]}
res["row3200_insensitive"] = all(x["status"] == "OK" for x in res["rows"] if x["line"] == "3207")
Path(out).write_text(json.dumps(res, indent=1) + "\n")
print(json.dumps(res, indent=1))
