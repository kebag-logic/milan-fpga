#!/usr/bin/env python3
"""R457-2: judge an interleaved --law-boundary probe log independently of the
suite's runner. Per phase: the harness's own [BOUNDARY] outcome, the probe's
PROBE-G fill count (read whether or not the window was gradable), the least
clearance, and the delay range of a graded window.

usage: judge_il.py sound|defect LOG
Exit 0 when: no NOT GRADABLE phase failed a check; on the sound design every
graded phase passed; on a defect every graded phase failed both law checks;
and every graded phase's least clearance is > 8 and every NOT GRADABLE one's
is <= 8.
"""
import re
import sys

kind, path = sys.argv[1], sys.argv[2]
text = open(path, errors="replace").read()
T = 100e6 / 48000.0
bad = []
rows = []
for m in re.finditer(r"\[BOUNDARY\] \+(\d+): (graded PASS|graded FAIL|NOT GRADABLE), (\d+) check", text):
    p, o, nf = int(m[1]), m[2], int(m[3])
    tag = f"T30 INTERNAL LAW +{p}"
    cl = re.search(re.escape(tag) + r": over .*?least clearance is (\d+) cycles", text)
    g = re.search(re.escape("[PROBE-G] " + tag) + r": [A-Z a-z]+; (\d+) PDUs read, (\d+) at fill 14", text)
    d = re.search(re.escape(tag) + r": 124 PDUs, fill at the PDU end (\d+)\.\.(\d+), first-event delay from it (\d+)\.\.(\d+) cycles", text)
    fails = re.findall(r"\[FAIL\] " + re.escape(tag) + r": ([^\n]*)", text)
    clear = int(cl[1]) if cl else None
    row = [p, o, nf, clear, f"{g[2]}/{g[1]}" if g else "-"]
    if d:
        lo, hi = int(d[3]), int(d[4])
        row += [f"{d[1]}..{d[2]}", f"{lo}..{hi}", f"{lo - 8 * T:.2f}", f"{9 * T + 1 - hi:.2f}"]
    else:
        row += ["-", "-", "-", "-"]
    rows.append(row)
    if o == "NOT GRADABLE" and nf:
        bad.append(f"+{p} NOT GRADABLE but failed {nf}")
    if o != "NOT GRADABLE" and clear is not None and clear <= 8:
        bad.append(f"+{p} graded at clearance {clear}")
    if o == "NOT GRADABLE" and clear is not None and clear > 8:
        bad.append(f"+{p} NOT GRADABLE at clearance {clear}")
    if kind == "sound" and o == "graded FAIL":
        bad.append(f"+{p} graded FAIL on the sound design: {fails}")
    if kind == "defect" and o == "graded PASS":
        bad.append(f"+{p} graded PASS on a defect")
    if kind == "defect" and o == "graded FAIL" and not (
            any("fill at every PDU end" in f for f in fails) and
            any("inside the law band" in f for f in fails)):
        bad.append(f"+{p} graded FAIL on a defect without both law checks: {fails}")
print("phase\toutcome\tfailed\tleast_clearance\tfill14/read\tfill\tdelay_cycles\tlower_edge_margin\tupper_edge_margin")
for r in sorted(rows):
    print("\t".join(str(x) for x in r))
ng = sorted(r[0] for r in rows if r[1] == "NOT GRADABLE")
print(f"# {len(rows)} phases; NOT GRADABLE {len(ng)}: {ng[0] if ng else '-'}..{ng[-1] if ng else '-'}"
      f" (contiguous: {ng == list(range(ng[0], ng[-1] + 1)) if ng else '-'})")
gm = [float(r[7]) for r in rows if r[7] != "-"] + [float(r[8]) for r in rows if r[8] != "-"]
if gm:
    print(f"# least band-edge margin over graded windows: {min(gm):.2f} cycles")
print("# problems: " + ("; ".join(bad) if bad else "none"))
sys.exit(1 if bad else 0)
