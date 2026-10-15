#!/usr/bin/env python3
"""Summarise a follow_ring bind sweep directory by bind: B17 window, SLIP_LB, slip times.

usage: grid_summary.py <sweep_dir> <label>

Reads only the runs' own logs and rc files. Per bind (one RESULT-645-BIND line and
the slip info lines that follow it): the window class, SLIP_LB dups/skips, slipped
frames before and after the ring acts, and each slip's time after the bind's first
PDU and against B17's first burst. Totals: binds inside and outside B17's window,
binds with any SLIP_LB change on each side (with phase, size and timing), and any
slip after the ring acts.
"""
import re
import sys
from pathlib import Path

d, label = Path(sys.argv[1]), sys.argv[2]
res = re.compile(
    r"RESULT-645-BIND: B17 cycle (?P<c>\d+) phase (?P<ph>[0-9.]+) at INTERNAL: first PDU \+(?P<fp>[0-9.]+) ms "
    r"after the bind, primed margin (?P<plo>[-0-9.e+]+)\.\.(?P<phi>[-0-9.e+]+) us \((?P<win>inside|OUTSIDE) "
    r"B17's window\), arms (?P<a>\d+) .*?settle recentres (?P<p>\d+) .*?render recentres (?P<r>\d+), SLIP_LB "
    r"\+(?P<du>\d+) dups \+(?P<sk>\d+) skips, slipped frames (?P<pre>\d+) before the ring acts and (?P<post>\d+) after")
slip = re.compile(r"info: B17 cycle (\d+): slip \((dup|skip)\) ([-+0-9.]+) s after the bind, ([-+0-9.]+) s from "
                  r"the first burst")
runs = rc0 = 0
binds = []
for log in sorted(d.glob("bind_*.log")):
    rcf = d / f"{log.stem}.rc"
    if not rcf.exists():
        continue
    runs += 1
    rc0 += int(rcf.read_text().strip()) == 0
    cur = None
    for line in log.read_text().splitlines():
        m = res.search(line)
        if m:
            g = m.groupdict()
            cur = dict(run=log.stem, cycle=int(g["c"]), phase=float(g["ph"]), fp_ms=float(g["fp"]),
                       plo=float(g["plo"]), phi=float(g["phi"]), inside=g["win"] == "inside",
                       one_each=(g["a"], g["p"], g["r"]) == ("1", "1", "1"), dups=int(g["du"]),
                       skips=int(g["sk"]), pre=int(g["pre"]), post=int(g["post"]), slips=[])
            binds.append(cur)
            continue
        m = slip.search(line)
        if m and cur is not None and int(m.group(1)) == cur["cycle"]:
            t_bind = float(m.group(3))
            cur["slips"].append((m.group(2), (t_bind - cur["fp_ms"] * 1e-3) * 1e3, float(m.group(4))))
inside = [b for b in binds if b["inside"]]
outside = [b for b in binds if not b["inside"]]


def moved(bs):
    return [b for b in bs if b["dups"] + b["skips"] > 0]


def show(b):
    ts = ", ".join(f"{k} {ms:+.3f} ms after the first PDU ({fb:+.4f} s from the burst)" for k, ms, fb in b["slips"])
    return (f"  {b['run']} cycle {b['cycle']} phase {b['phase']:.5f} primed {b['plo']:.3f}..{b['phi']:.3f} us: "
            f"SLIP_LB +{b['dups']} dups +{b['skips']} skips, frames {b['pre']} before / {b['post']} after the ring "
            f"acts; {ts}")


print(f"## {label}")
print(f"runs {runs}, rc 0: {rc0}; binds {len(binds)}; one arm / settle / render recentre each: "
      f"{sum(b['one_each'] for b in binds)}")
print(f"inside B17's window: {len(inside)}, with a SLIP_LB change: {len(moved(inside))}")
for b in moved(inside):
    print(show(b))
mo = moved(outside)
print(f"outside: {len(outside)}, with a SLIP_LB change: {len(mo)}, at phases "
      f"{sorted({round(b['phase'], 5) for b in mo})}")
if mo:
    last = max(ms for b in mo for _, ms, fb in b["slips"] if fb < 0.0) if any(
        fb < 0.0 for b in mo for _, _, fb in b["slips"]) else float("nan")
    print(f"  latest slip before the first burst: {last:.3f} ms after the first PDU")
for b in mo:
    print(show(b))
print(f"slips after the ring acts, all binds: {sum(b['post'] for b in binds)}")
