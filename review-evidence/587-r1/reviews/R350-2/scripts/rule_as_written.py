#!/usr/bin/env python3
r"""Apply the committed export_comparison normalization rule literally to two independent exports.

usage: rule_as_written.py REPO_A WORK_A REPO_B WORK_B

Rule (docs/findings/PP_SHADOW_BASELINE_50MHZ_INPUTS.json export_comparison.normalization):
replace each absolute build root with $BUILD, then the absolute checkout root with $REPO;
strip /\*.*?\*/ (DOTALL), then //[^\n]*; hash UTF-8 bytes. Tcl and XDC compare after both
root replacements only. Prints digests and equalities; exit 1 if the Verilog digests differ
from each other or from the committed value, or if any Tcl/XDC pair differs.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

ra, wa, rb, wb = sys.argv[1:]
committed = json.loads((Path(ra) / "docs/findings/PP_SHADOW_BASELINE_50MHZ_INPUTS.json").read_text())["export_comparison"]
print("committed rule:", committed["normalization"])


def roots(text, repo, work):
    text = text.replace(work, "$BUILD")
    return text.replace(repo, "$REPO")


def verilog(repo, work):
    text = (Path(work) / "ax8x8/gateware/alinx_ax7101.v").read_text(encoding="utf-8")
    print(f"  occurrences build_root={text.count(work)} checkout_root={text.count(repo)}")
    text = roots(text, repo, work)
    left = [l for l in text.splitlines() if "$BUILD" in l]
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    text = re.sub(r"//[^\n]*", "", text)
    print(f"  $BUILD-bearing lines before comment strip={len(left)}; after strip={text.count('$BUILD')}; $REPO after strip={text.count('$REPO')}")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


bad = 0
print("export A"); da = verilog(ra, wa); print(f"  normalized_sha256={da}")
print("export B"); db = verilog(rb, wb); print(f"  normalized_sha256={db}")
for label, d in (("A", da), ("B", db)):
    ok = d == committed["normalized_verilog_sha256"]
    bad += not ok
    print(f"{'OK  ' if ok else 'DIFF'} export {label} digest == committed")
gw = "ax8x8/gateware"
names = sorted(p.name for p in (Path(wa) / gw).iterdir() if p.suffix in (".tcl", ".xdc"))
for n in names:
    ta = roots((Path(wa) / gw / n).read_text(), ra, wa)
    tb = roots((Path(wb) / gw / n).read_text(), rb, wb)
    ok = ta == tb
    bad += not ok
    print(f"{'OK  ' if ok else 'DIFF'} {n} equal after both root replacements "
          f"(raw equal={(Path(wa) / gw / n).read_bytes() == (Path(wb) / gw / n).read_bytes()})")
print(f"RESULT mismatches={bad}")
sys.exit(1 if bad else 0)
