#!/usr/bin/env python3
"""Compare the Tcl hook echoed in an implementation log with the head blob.
Usage: echoed_hook_vs_head.py <vivado.log> <repo> <rev>"""
import re, subprocess, sys
log, repo, rev = sys.argv[1:4]
lines = open(log, encoding="utf-8", errors="replace").read().splitlines()
start = next(i for i, l in enumerate(lines) if l.startswith("# source {") and "clock_constraints.tcl" in l)
end = next(i for i in range(start, len(lines)) if lines[i] == "# kl_quasi_static_constraints")
echo = [re.sub(r"^## ?", "", l) for l in lines[start + 1:end]]
head = subprocess.run(["git", "-C", repo, "show", f"{rev}:sw/litex/clock_constraints.tcl"],
                      capture_output=True, text=True, check=True).stdout.splitlines()
# Vivado echoes code lines, not comment lines.
e = [l.rstrip() for l in echo if l.strip() and not l.lstrip().startswith("#")]
h = [l.rstrip() for l in head if l.strip() and not l.lstrip().startswith("#")]
print(log, "echoed", len(e), "head", len(h), "IDENTICAL" if e == h else "DIFFER")
if e != h:
    import difflib; print("\n".join(list(difflib.unified_diff(h, e, lineterm=""))[:40]))
