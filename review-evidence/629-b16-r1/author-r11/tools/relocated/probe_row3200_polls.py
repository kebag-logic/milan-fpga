#!/usr/bin/env python3
"""R624-6: mutation probe of line 3200's second row (the window poll count, "596 of 596").

usage: probe_row3200_polls.py <check_b16_figures.py> <findings page> <packet root> <repo> <work dir> <out.json>
Copies the packet, sets ONLY B-CRF's window span 'polls' to 595 in r2/bcrf-poll-receipt.json (servo
counts untouched), runs the check unchanged, and records the status of every row on lines 3008, 3174
and 3200. The row that states the poll count for both cases must turn MISMATCH."""
import json, shutil, subprocess, sys, os
CHECK, PAGE, PKT, REPO, WORK, OUT = sys.argv[1:7]
d = os.path.join(WORK, "pkt"); shutil.rmtree(WORK, ignore_errors=True); shutil.copytree(PKT, d)
f = os.path.join(d, "r2/bcrf-poll-receipt.json"); j = json.load(open(f))
assert j["spans"]["window-start..window-end"]["polls"] == 596
j["spans"]["window-start..window-end"]["polls"] = 595
json.dump(j, open(f, "w"), indent=1)
pr = subprocess.run([sys.executable, "-I", os.path.join(d, "tools/check_b16_figures.py") if CHECK == "-" else CHECK, PAGE, d,
                     os.path.join(WORK, "rows.tsv"), os.path.join(WORK, "cov.tsv"), "--repo", REPO], capture_output=True, text=True)
rows = [l.split("\t") for l in open(os.path.join(WORK, "rows.tsv"), encoding="utf-8") if not l.startswith("#")]
sel = [dict(row=r[0], line=r[1], shown=r[2], receipt=r[3], recomputed=r[5], status=r[6].strip()) for r in rows
       if r[1] in ("3015", "3181", "3207") and r[2] == "596"]
res = dict(rc=pr.returncode, rows=sel, row3200_polls_detected=any(x["line"] == "3207" and x["status"] == "MISMATCH" for x in sel))
json.dump(res, open(OUT, "w"), indent=1); print(json.dumps(res, indent=1))
