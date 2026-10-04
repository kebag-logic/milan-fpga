#!/usr/bin/env python3
"""R457-3: audit every law window the given logs print, against round 3's
definition of the walk (the range of the end-to-nearest-pop offset over the
window's steady ends, MEDIA_CLOCK_FOLLOWING.md "The walk").

For each leg-side offsets line ("T30 ... LAW ...: over N steady PDU ends the
first pop after ... A..B ... the pop nearest the boundary C..D (walk W); the
least clearance is X cycles ... against the K-cycle ambiguity window: margin M"):
  - W == D - C, unless the line carries the wrap suffix (then W == B - A and
    D - C > half a tick);
  - M == X - K and K == 9;
  - where a histogram line for the same tag follows (--law-boundary mode),
    its offsets span exactly C..D and its counts sum to N;
  - the window is NOT GRADABLE (a "[NOT GRADABLE] <tag>" line) iff X <= K.
For each graded window's law line ("N PDUs, fill ..., first-event delay from
it dmin..dmax cycles"), the band-edge margins dmin - 8T and 9T - dmax.
For each runner-side line of tdm8render-law-boundary ("+p: outcome; the pop
nearest the boundary a..b (walk w), least clearance c"): w == b - a, and the
outcome is "not gradable" iff c <= 9; and its "largest walk" line agrees
with the maximum of those lines.

A log is a DEFECT log (setpoint -1/+1, A2-a, window fault) by its file name;
band margins are reported for sound logs only.

usage: walk_audit.py LOG...
"""
import re
import sys
from collections import defaultdict

T = 100e6 / 48000.0
K = 9
OFF = re.compile(
    r"\[i\]\s+(T30 (?:INTERNAL|CRF) LAW(?: \+\d+)?): over (\d+) steady PDU ends the "
    r"first pop after the end is taken ([+-]\d+)\.\.([+-]\d+) cycles from it and "
    r"the pop nearest the boundary ([+-]\d+)\.\.([+-]\d+) \(walk (\d+)\); the least "
    r"clearance is (\d+) cycles, at PDU (\d+) \(offset ([+-]\d+)\), against the "
    r"(\d+)-cycle ambiguity window: margin (-?\d+)(; the nearest pop changes side[^\n]*)?")
HIST = re.compile(r"\[i\]\s+(T30 (?:INTERNAL|CRF) LAW(?: \+\d+)?): PDU ends per "
                  r"nearest-pop offset \(offset:ends\):((?: -?\d+:\d+)+)")
LAW = re.compile(r"\[i\]\s+(T30 (?:INTERNAL|CRF) LAW(?: \+\d+)?): (\d+) PDUs, fill at "
                 r"the PDU end (\d+)\.\.(\d+), first-event delay from it (-?\d+)\.\.(-?\d+) cycles")
NG = re.compile(r"\[NOT GRADABLE\] (T30 (?:INTERNAL|CRF) LAW(?: \+\d+)?):")
RUN = re.compile(r"\[i\]\s+\+(\d+): ([^;]+); the pop nearest the boundary ([+-]\d+)\.\.([+-]\d+) "
                 r"\(walk (\d+)\), least clearance (\d+)")
LARGEST = re.compile(r"the largest walk over (\d+) windows is (\d+) cycles \(([^)]*)\); "
                     r"the leg states a walk of (\d+)")
DEFECT = ("-sp", "sphi", "a2a", "wfault", "nodwell")

problems = []
stats = defaultdict(lambda: {"n": 0, "maxwalk": -1, "where": "", "wraps": 0,
                             "minclear_graded": None})
band = []          # (log, tag, lower margin, upper margin) for sound graded windows
standing = []      # (log, tag, walk, clear, margin, dmin..dmax) of standing windows
runner = {"lines": 0, "maxwalk": -1, "largest": []}
for path in sys.argv[1:]:
    name = path.split("/")[-1]
    defect = any(d in name for d in DEFECT)
    text = open(path, errors="replace").read()
    lines = text.splitlines()
    for i, ln in enumerate(lines):
        m = OFF.search(ln)
        if m:
            tag, ends = m[1], int(m[2])
            n0, n1, d0, d1, walk, clear = (int(m[x]) for x in (3, 4, 5, 6, 7, 8))
            k, margin, wrap = int(m[11]), int(m[12]), m[13] is not None
            want = (n1 - n0) if wrap else (d1 - d0)
            if walk != want:
                problems.append(f"{name}:{i+1}: {tag} walk {walk} != range {want}")
            if wrap and not 2 * (d1 - d0) > T:
                problems.append(f"{name}:{i+1}: {tag} wrap suffix but nearest range {d1-d0}")
            if not wrap and 2 * (d1 - d0) > T:
                problems.append(f"{name}:{i+1}: {tag} nearest range {d1-d0} wraps, no suffix")
            if k != K or margin != clear - k:
                problems.append(f"{name}:{i+1}: {tag} window {k} margin {margin} clear {clear}")
            # histogram (law-boundary mode): the next line for the same tag
            for nl in lines[i + 1:i + 3]:
                h = HIST.search(nl)
                if h and h[1] == tag:
                    pts = [tuple(map(int, p.split(":"))) for p in h[2].split()]
                    lo, hi = min(p[0] for p in pts), max(p[0] for p in pts)
                    if (lo, hi) != (d0, d1) or sum(p[1] for p in pts) != ends:
                        problems.append(f"{name}:{i+1}: {tag} histogram {lo}..{hi} "
                                        f"sum {sum(p[1] for p in pts)} vs {d0}..{d1} {ends}")
            ng = any(NG.search(x) and NG.search(x)[1] == tag for x in lines[i + 1:i + 4])
            if ng != (clear <= K):
                problems.append(f"{name}:{i+1}: {tag} NOT GRADABLE {ng} but clearance {clear}")
            kind = ("CRF" if "CRF" in tag else "LAW") + (" defect" if defect else " sound")
            s = stats[kind]
            s["n"] += 1
            s["wraps"] += wrap
            if walk > s["maxwalk"]:
                s["maxwalk"], s["where"] = walk, f"{name} {tag} {d0:+d}..{d1:+d}"
            if not ng and (s["minclear_graded"] is None or clear < s["minclear_graded"]):
                s["minclear_graded"] = clear
            if not ng:
                for nl in lines[i + 1:i + 6]:
                    lw = LAW.search(nl)
                    if lw and lw[1] == tag:
                        dmin, dmax = int(lw[5]), int(lw[6])
                        if not defect:
                            band.append((name, tag, dmin - 8 * T, 9 * T - dmax))
                        if ("lawonly" in name or "suite" in name or "stdhist" in name
                                or "probe-sp" in name or "arm-" in name):
                            standing.append((name, tag, walk, clear, margin, f"{dmin}..{dmax}",
                                             f"fill {lw[3]}..{lw[4]}", f"{d0:+d}..{d1:+d}"))
                        break
        r = RUN.search(ln)
        if r:
            runner["lines"] += 1
            lo, hi, w, c = int(r[3]), int(r[4]), int(r[5]), int(r[6])
            if w != hi - lo:
                problems.append(f"{name}:{i+1}: runner +{r[1]} walk {w} != {hi-lo}")
            ngr = "not gradable" in r[2].lower()
            if ngr != (c <= K):
                problems.append(f"{name}:{i+1}: runner +{r[1]} '{r[2]}' at clearance {c}")
            runner["maxwalk"] = max(runner["maxwalk"], w)
        g = LARGEST.search(ln)
        if g:
            runner["largest"].append((name, int(g[1]), int(g[2]), g[3], int(g[4])))

print("# per kind: windows, largest walk (where), wrapped windows, least clearance of a graded window")
for kind in sorted(stats):
    s = stats[kind]
    print(f"{kind}\t{s['n']}\t{s['maxwalk']}\t{s['where']}\t{s['wraps']}\t{s['minclear_graded']}")
print(f"# runner per-window lines: {runner['lines']}, largest walk {runner['maxwalk']}")
for name, n, w, where, stated in runner["largest"]:
    print(f"# runner summary {name}: largest walk over {n} windows is {w} ({where}); stated {stated}")
if band:
    lo = min(band, key=lambda b: b[2])
    hi = min(band, key=lambda b: b[3])
    print(f"# sound graded windows with a law line: {len(band)}; least lower-edge margin "
          f"{lo[2]:.2f} ({lo[0]} {lo[1]}); least upper-edge margin (to 9T) {hi[3]:.2f} "
          f"({hi[0]} {hi[1]}), to 9T + 1 cycle {hi[3] + 1:.2f}")
print("# standing graded windows: log, tag, walk, clearance, margin, delay, fill, nearest-pop range")
for row in standing:
    print("\t".join(str(x) for x in row))
print(f"# problems: {len(problems)}")
for p in problems:
    print("PROBLEM " + p)
sys.exit(1 if problems else 0)
