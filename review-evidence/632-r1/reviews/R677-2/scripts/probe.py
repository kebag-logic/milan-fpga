#!/usr/bin/env python3
"""Disposable fault probe for tb/verilator/media_phase at the reviewed head.

usage: probe.py <tree> <name> <file-rel-to-tree> <anchor> <replacement> <make-args...>

<tree> is a disposable copy of the head (git archive of hdl, tb/common,
tb/verilator/media_phase, tb/verilator/mmcm_servo). The anchor must occur
exactly once; the substituted file is written in place in that copy only.
Then `make -C <tree>/tb/verilator/media_phase <make-args>` runs; its log and
exit code are printed. A probe "is caught" when make exits non-zero with a
[FAIL] line; it "survives" when make exits 0.
"""
import subprocess
import sys
from pathlib import Path

tree, name, rel, anchor, repl = sys.argv[1:6]
make_args = sys.argv[6:]
src = Path(tree) / rel
text = src.read_text()
n = text.count(anchor.encode().decode("unicode_escape")) if "\\n" in anchor else text.count(anchor)
anc = anchor.encode().decode("unicode_escape") if "\\n" in anchor else anchor
rep = repl.encode().decode("unicode_escape") if "\\n" in repl else repl
if text.count(anc) != 1:
    print(f"PROBE {name}: anchor found {text.count(anc)} times, not applied")
    sys.exit(2)
src.write_text(text.replace(anc, rep))
p = subprocess.run(["make", "-C", str(Path(tree) / "tb/verilator/media_phase")] + make_args,
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
fails = [l for l in p.stdout.splitlines() if "[FAIL]" in l or "FAILED" in l or "failures:" in l]
print(p.stdout[-200000:])
print(f"PROBE {name}: make rc={p.returncode}; " + ("CAUGHT" if p.returncode != 0 else "SURVIVED"))
for l in fails:
    print("  " + l)
sys.exit(0)
