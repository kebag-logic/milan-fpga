#!/usr/bin/env python3
"""Extract the mutation arm's verdict lines ([PASS]/[FAIL] and the tally) from
each log, normalise the temporary directory path and the planted line number
(the merge-tested datapath differs by lines), and report whether every log
carries the same lines in the same order.
Usage: compare_arm_lines.py <log>..."""
import re, sys
seqs = {}
for path in sys.argv[1:]:
    lines = []
    on = False
    for ln in open(path, errors="replace"):
        ln = ln.rstrip("\n")
        if "python3 mutants.py" in ln: on = True; continue
        if not on: continue
        if ln.startswith(("[PASS]", "[FAIL]")) or re.match(r"\d+ checks:", ln):
            ln = re.sub(r"/\S*/capture-coherence-mutants-[^/]+/", "<tmp>/", ln)
            ln = re.sub(r"milan_datapath\.sv:\d+:\d+", "milan_datapath.sv:<L>:<C>", ln)
            lines.append(ln)
        if re.match(r"\d+ checks:", ln): break
    seqs[path] = lines
    print(f"{len(lines):3d} lines  {lines[-1] if lines else '-'}  {path.split('/')[-1]}")
ref = next(iter(seqs.values()))
for p, s in seqs.items():
    print(("IDENTICAL" if s == ref else "DIFFERS  ") + " to the first: " + p.split('/')[-1])
    if s != ref:
        for a, b in zip(ref, s):
            if a != b: print("   first:", a, "\n   this: ", b); break
