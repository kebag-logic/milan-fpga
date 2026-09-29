#!/usr/bin/env python3
"""R394-4: compare the mutation arm's verdict lines across runs with different worker counts.
Keeps the lines from the `[i]  N builds` banner through the `N checks:` tally, drops the banner
(it names the worker count), and normalises the temp-dir path and the planted-break line:column
(the hosted run is on the PR merge ref, whose milan_datapath.sv is a few lines shorter).
  python3 r394_arm_compare.py <log> <log> [...]"""
import re, sys
def arm(path):
    out, on = [], False
    for ln in open(path, encoding="utf-8", errors="replace"):
        ln = ln.rstrip("\n")
        if re.match(r"\[i\]  \d+ builds on", ln):
            on = True
            continue
        if on:
            ln = re.sub(r"/\S*/capture-coherence-mutants-[^/]+/", "<TMP>/", ln)
            ln = re.sub(r"(milan_datapath\.sv):\d+:\d+:", r"\1:<L>:<C>:", ln)
            out.append(ln)
            if re.match(r"\d+ checks: ", ln):
                break
    return out
runs = [arm(p) for p in sys.argv[1:]]
for p, r in zip(sys.argv[1:], runs):
    print(f"{p}: {len(r)} lines, tally {r[-1] if r else 'NONE'!r}")
same = all(r == runs[0] for r in runs[1:])
print(f"identical verdict lines in identical order: {same}")
if not same:
    import difflib
    for r, p in zip(runs[1:], sys.argv[2:]):
        print("\n".join(difflib.unified_diff(runs[0], r, sys.argv[1], p, lineterm="")))
sys.exit(0 if same else 1)
