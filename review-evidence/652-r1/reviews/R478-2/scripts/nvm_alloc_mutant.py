#!/usr/bin/env python3
"""Plant one defect in a disposable copy of the exported head tree's
scripts/nvm_allocation_table.py (each OLD must occur exactly once; several
OLD/NEW pairs allowed), then run the record-space gate's unmutated check and
its three allocation-table controls in that copy. The clone is never written.
Usage: nvm_alloc_mutant.py <head export> <scratch dest> [OLD NEW]...
A control 'catches' when it exits 1 with its required FINDING text."""
import shutil
import subprocess
import sys
from pathlib import Path

src, dest = Path(sys.argv[1]), Path(sys.argv[2])
pairs = [a.encode().decode("unicode_escape") for a in sys.argv[3:]]
if dest.exists():
    shutil.rmtree(dest)
shutil.copytree(src, dest, symlinks=True)
mod = dest / "scripts" / "nvm_allocation_table.py"
text = mod.read_text()
for old, new in zip(pairs[::2], pairs[1::2]):
    assert text.count(old) == 1, f"anchor occurs {text.count(old)} times: {old!r}"
    text = text.replace(old, new)
mod.write_text(text)
want = {None: None, "stale_allocation_table": "1x1 user name reads 1",
        "short_allocation_row": "user name has no 8x8 figure",
        "long_allocation_row": "user name has 1 cell(s) past the 8x8 column"}
for control, needle in want.items():
    argv = [sys.executable, "scripts/check_nvm_record_space.py", "--quiet"]
    if control:
        argv.append(f"--mutate={control}")
    run = subprocess.run(argv, cwd=dest, capture_output=True, text=True)
    out = run.stdout + run.stderr
    hit = needle is not None and any(l.startswith("FINDING:") and needle in l for l in out.splitlines())
    tb = "Traceback (most recent call last):" in out
    verdict = ("clean" if run.returncode == 0 else "FINDINGS") if control is None else \
              ("caught" if run.returncode == 1 and hit and not tb else "MISSED")
    print(f"{control or 'unmutated check'}: rc={run.returncode} traceback={tb} -> {verdict}")
    for line in out.splitlines():
        if line.startswith("FINDING:") or line.startswith("Traceback") or "Error" in line[:40]:
            print(f"    {line[:240]}")
shutil.rmtree(dest)
