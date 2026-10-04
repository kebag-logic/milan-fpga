#!/usr/bin/env python3
"""Tabulate the reviewer probes: per control, each suite's rc, tally and failing check names.

Usage: probe_table.py PROBES_DIR"""
import re
import sys
from pathlib import Path
P = Path(sys.argv[1])  # the probes scratch directory: r452-controls/, r453-controls/, r452-work/, r453-work/
rows = []
for who in ("r452", "r453"):
    for ctl in sorted(p.stem for p in (P / f"{who}-controls").glob("*.sv")):
        rc = (P / f"{who}-{ctl}.rc").read_text().split() if (P / f"{who}-{ctl}.rc").exists() else ["?", "?"]
        cells = []
        for suite in ("aecp_notify", "pp_top"):
            log = (P / "r452-work" / f"{ctl}-{suite}.log") if who == "r452" else (P / "r453-work" / ctl / f"{suite}.log")
            if not log.exists():
                cells.append("not run"); continue
            text = log.read_text(errors="replace")
            fails = [l[len("FAIL: "):].split(":")[0] for l in text.splitlines() if l.startswith("FAIL: ")]
            tally = re.findall(r"(\d+) checks: (\d+) PASS, (\d+) FAIL", text)
            builds = re.findall(r"\[build \w+\] (\d+) checks, (\d+) failures", text)
            if fails:
                names = sorted(set(fails), key=fails.index)
                cells.append(f"FAIL ({len(fails)}: {', '.join(names[:6])}{', ...' if len(names) > 6 else ''})")
            elif tally:
                cells.append(f"PASS {tally[-1][0]}/{tally[-1][1]}")
            else:
                cells.append("no tally, no FAIL line")
        rows.append((who, ctl, rc[0], rc[1], cells[0], cells[1]))
print("| Reviewer | Control | probe rc, s | `tb/aecp_notify` | `tb/pp_top` |")
print("|---|---|---|---|---|")
for who, ctl, rc, s, a, b in rows:
    print(f"| {who.upper()}-1 | `{ctl}` | {rc}, {s} | {a} | {b} |")
caught = sum(1 for r in rows if r[4].startswith("FAIL") or r[5].startswith("FAIL"))
print(f"\n{caught} of {len(rows)} controls fail a committed check")
