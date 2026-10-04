#!/usr/bin/env python3
"""R457-3: compare the executor's published round3-boundary-walks.md (the
unmutated design's per-window table, one per processor) with the per-window
lines this review's own tdm8render-law-boundary run printed.

usage: compare_walks_table.py round3-boundary-walks.md lb-head.log lb-c4.log

For every (processor, history, phase) cell of the published table: the
nearest-pop range, the walk, the least clearance and the outcome (P graded
pass, N not gradable) must equal the review run's line for the unmutated
gateware. Also: the two setpoint defects' lines must carry the same range,
walk and clearance as the unmutated design's, in every history.
"""
import re
import sys

VERDICT = re.compile(r"^\[(?:PASS|FAIL)\] law boundary, (the unmutated gateware|the render "
                     r"setpoint one event (?:low|high)), (the leg's own scan|descending|\+\d+ alone)")
WIN = re.compile(r"^\s+\[i\]\s+\+(\d+): ([^;]+); the pop nearest the boundary ([+-]\d+)\.\.([+-]\d+) "
                 r"\(walk (\d+)\), least clearance (\d+)")


def runs(path):
    got = {}
    cur = None
    for ln in open(path, errors="replace"):
        v = VERDICT.search(ln)
        if v:
            h = v[2]
            hist = "asc" if h.startswith("the leg") else "desc" if h == "descending" else "alone"
            cur = (v[1], hist)
            continue
        w = WIN.search(ln)
        if w and cur:
            outcome = "N" if "not gradable" in w[2].lower() else "P" if "pass" in w[2].lower() \
                else "F" if "fail" in w[2].lower() else w[2]
            got[cur + (int(w[1]),)] = (int(w[3]), int(w[4]), int(w[5]), int(w[6]), outcome)
    return got


def table(path):
    out = {}
    proc = None
    for ln in open(path):
        if ln.startswith("## dev's pin"):
            proc = "head"
        elif ln.startswith("## processor `c4cb84ff`"):
            proc = "c4"
        m = re.match(r"^\| \+(\d+) \|(.*)$", ln)
        if not (m and proc):
            continue
        cells = [c.strip() for c in m[2].split("|")]
        for k, hist in enumerate(("asc", "desc", "alone")):
            rng, walk, clear, oc = cells[4 * k:4 * k + 4]
            if not rng:
                continue
            a, b = (int(x) for x in rng.split(".."))
            out[(proc, hist, int(m[1]))] = (a, b, int(walk), int(clear), oc)
    return out


pub = table(sys.argv[1])
mine = {"head": runs(sys.argv[2]), "c4": runs(sys.argv[3])}
diff = 0
for (proc, hist, ph), want in sorted(pub.items()):
    got = mine[proc].get(("the unmutated gateware", hist, ph))
    if got != want:
        diff += 1
        print(f"DIFF {proc} {hist} +{ph}: published {want}, this review {got}")
defect_diff = 0
for proc, g in mine.items():
    for (design, hist, ph), v in g.items():
        if design == "the unmutated gateware":
            continue
        s = g.get(("the unmutated gateware", hist, ph))
        if s is None or s[:4] != v[:4]:
            defect_diff += 1
            print(f"DEFECT-DIFF {proc} {design} {hist} +{ph}: {v} vs sound {s}")
        if v[4] == "P":
            print(f"DEFECT-GRADED-PASS {proc} {design} {hist} +{ph}")
            defect_diff += 1
print(f"published cells: {len(pub)}; review windows: head {len(mine['head'])}, c4 {len(mine['c4'])}; "
      f"cells differing: {diff}; defect windows differing from the sound design or graded "
      f"PASS: {defect_diff}")
sys.exit(1 if diff or defect_diff else 0)
