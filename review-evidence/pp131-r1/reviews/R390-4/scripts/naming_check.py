#!/usr/bin/env python3
"""Reviewer focused re-run of the parent naming ratchet for the protocol-
processor tree only, through the parent's own measure_naming.scan_text() and
its naming.budget (fetched read-only from milan-fpga 7a7582f0): candidates at
each rev whose identity is not in the budget are NEW (the gate's failure).
Usage: naming_check.py <parent-scripts-dir> <processor-clone> <rev> ..."""
import subprocess, sys
sys.path.insert(0, sys.argv[1])
import measure_naming as mn
recorded = set(l.split("#")[0].strip() for l in open(sys.argv[1] + "/naming.budget")
               if l.split("#")[0].strip())
clone = sys.argv[2]
for rev in sys.argv[3:]:
    files = [f for f in subprocess.run(["git", "-C", clone, "ls-tree", "-r", "--name-only",
                                         rev, "hdl"], capture_output=True, text=True,
                                        check=True).stdout.split() if f.endswith(".sv")]
    new, cands = [], 0
    for f in files:
        text = subprocess.run(["git", "-C", clone, "show", f"{rev}:{f}"],
                              capture_output=True, text=True, check=True).stdout
        c, _e, _st = mn.scan_text(text)
        for module, name, unit, doc, reason in c:
            cands += 1
            ident = f"protocol-processor:{f}:{module}:{name}"
            if ident not in recorded:
                new.append(f"{ident} ({unit}; {reason or 'hides unit'})")
    print(f"{rev[:10]}: {cands} candidates, {len(new)} not in the budget")
    for n in new:
        print("   NEW", n)
