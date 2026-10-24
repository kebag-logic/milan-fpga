#!/usr/bin/env python3
"""Compare the command table's verilator build forms for Vmilan_dp_crflic and
Vmilan_dp_tspec8 at a checkout, and each form's .sv source list against the
milan_dp Makefile's own SRCS list (expanded by make -pn).
usage: python3 tspec8_pattern_probe.py <checkout>"""
import difflib, json, re, subprocess, sys
from pathlib import Path
root = Path(sys.argv[1])
t = json.loads((root / "ci/image/command-table.json").read_text())
forms = {}
def walk(x):
    if isinstance(x, list):
        if x and all(isinstance(w, str) for w in x) and "-o" in x:
            i = x.index("-o")
            if i + 1 < len(x): forms.setdefault(x[i + 1], []).append(x)
        for v in x: walk(v)
    elif isinstance(x, dict):
        for v in x.values(): walk(v)
walk(t)
for k in ("Vmilan_dp_crflic", "Vmilan_dp_tspec8"):
    print(k, "forms:", len(forms.get(k, [])), "words:", [len(f) for f in forms.get(k, [])])
a, b = forms["Vmilan_dp_crflic"][0], forms["Vmilan_dp_tspec8"][0]
print("== crflic -> tspec8 word diff")
for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b).get_opcodes():
    if op != "equal": print(" ", op, a[i1:i2], "->", b[j1:j2])
db = subprocess.run(["make", "-pn", "-C", str(root / "tb/verilator/milan_dp"), "tspec8-build"],
                    capture_output=True, text=True).stdout
m = re.search(r"^SRCS :?= (.*)$", db, re.M)
srcs = m.group(1).split() if m else []
print("Makefile SRCS words (unexpanded):", len(srcs))
