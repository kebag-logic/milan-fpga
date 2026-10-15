#!/usr/bin/env python3
"""Summarise a follow_ring bind campaign directory: per run and per B17 cycle.

usage: summ_bind.py <sweep_dir> <label>
Prints a Markdown table and totals; reads only the runs' own logs and rc files.
"""
import re
import sys
from pathlib import Path

d, label = Path(sys.argv[1]), sys.argv[2]
pat = re.compile(
    r"RESULT-645-BIND: B17 cycle (?P<c>\d+) phase (?P<ph>[0-9.]+) (?P<mode>at INTERNAL|under CRF following): "
    r"first PDU \+(?P<fp>[0-9.]+) ms after the bind, primed margin (?P<plo>[-0-9.e+]+)\.\.(?P<phi>[-0-9.e+]+) us "
    r"\((?P<win>inside|OUTSIDE) B17's window\), arms (?P<a>\d+) .*?settle recentres (?P<p>\d+) \((?P<t>[-0-9.]+) "
    r"ticks after the arm\), render recentres (?P<r>\d+), SLIP_LB \+(?P<du>\d+) dups \+(?P<sk>\d+) skips, "
    r"slipped frames (?P<pre>\d+) before the ring acts and (?P<post>\d+) after.*?margin after a recentre "
    r"(?P<alo>[-+0-9.e]+)\.\.(?P<ahi>[-+0-9.e]+) ticks, full side (?P<flo>[-+0-9.e]+)")
slip = re.compile(r"info: B17 cycle (\d+): slip \((dup|skip)\) ([-+0-9.]+) s after the bind, "
                  r"([-+0-9.]+) s from the first burst")
tot = dict(runs=0, rc0=0, binds=0, inside=0, slipped_binds=0, dups=0, skips=0, pre=0, post=0,
           arms=0, pulses=0, renders=0, one_each=0, slips_at_burst=0, slips_before_burst=0,
           slips_after_burst=0, inside_slipped=0, outside_pre_binds=0)
ext = dict(after_lo=1e9, after_hi=-1e9, full_lo=1e9, primed_lo=1e9, primed_hi=-1e9, ticks_lo=1e9, ticks_hi=-1e9)
rows = []
for log in sorted(d.glob("bind_*.log")):
    rcf = d / f"{log.stem}.rc"
    if not rcf.exists():
        continue
    rc = int(rcf.read_text().strip())
    text = log.read_text()
    tot["runs"] += 1
    tot["rc0"] += rc == 0
    per = []
    for m in pat.finditer(text):
        g = m.groupdict()
        a, p, r, du, sk = (int(g[k]) for k in ("a", "p", "r", "du", "sk"))
        pre, post = int(g["pre"]), int(g["post"])
        inside = g["win"] == "inside"
        tot["binds"] += 1
        tot["inside"] += inside
        tot["slipped_binds"] += (du + sk) > 0
        tot["inside_slipped"] += inside and (du + sk) > 0
        tot["outside_pre_binds"] += (not inside) and pre > 0
        tot["dups"] += du
        tot["skips"] += sk
        tot["pre"] += pre
        tot["post"] += post
        tot["arms"] += a
        tot["pulses"] += p
        tot["renders"] += r
        tot["one_each"] += (a == 1 and p == 1 and r == 1)
        if p == 1 and a == 1:
            t = float(g["t"])
            ext["ticks_lo"] = min(ext["ticks_lo"], t)
            ext["ticks_hi"] = max(ext["ticks_hi"], t)
        ext["primed_lo"] = min(ext["primed_lo"], float(g["plo"]))
        ext["primed_hi"] = max(ext["primed_hi"], float(g["phi"]))
        alo, ahi, flo = float(g["alo"]), float(g["ahi"]), float(g["flo"])
        if alo < 1e8:
            ext["after_lo"] = min(ext["after_lo"], alo)
            ext["after_hi"] = max(ext["after_hi"], ahi)
        if flo < 1e8:
            ext["full_lo"] = min(ext["full_lo"], flo)
        per.append((int(g["c"]), float(g["ph"]), float(g["plo"]), float(g["phi"]), inside, a, p, r, du, sk,
                    pre, post))
    for m in slip.finditer(text):
        dt = float(m.group(4))
        if 0.0 <= dt < 0.01:
            tot["slips_at_burst"] += 1
        elif dt < 0.0:
            tot["slips_before_burst"] += 1
        else:
            tot["slips_after_burst"] += 1
    rows.append((log.stem, rc, per))
print(f"## {label}")
print()
print("| Run | rc | First-PDU phase, tick | Primed margin, us | B17 window | Binds | SLIP_LB dups / skips | "
      "Slipped frames before / after the ring acts | Arms / settle / render recentres |")
print("|---|---|---|---|---|---|---|---|---|")
for name, rc, per in rows:
    if not per:
        print(f"| {name} | {rc} | - | no RESULT | - | 0 | - | - | - |")
        continue
    ph = per[0][1]
    plo = min(v[2] for v in per)
    phi = max(v[3] for v in per)
    win = "inside" if all(v[4] for v in per) else ("OUTSIDE" if not any(v[4] for v in per) else "mixed")
    s = [sum(v[i] for v in per) for i in range(5, 12)]
    print(f"| {name} | {rc} | {ph:.4f} | {plo:.3f} to {phi:.3f} | {win} | {len(per)} | {s[3]} / {s[4]} | "
          f"{s[5]} / {s[6]} | {s[0]} / {s[1]} / {s[2]} |")
print()
print("totals:", tot)
print("extrema:", ext)
