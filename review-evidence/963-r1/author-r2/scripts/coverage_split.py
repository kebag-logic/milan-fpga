#!/usr/bin/env python3
"""coverage_split.py TREE run NAME KEEP | TREE check KEEP: the firmware coverage ratchet (fw_coverage.py --check) in
foreground-sized units, by its own functions. `run NAME` runs one of fw_coverage.GATES in coverage mode into KEEP/NAME
with exactly the argv fw_coverage.coverage_runs gives it (no --lwsrp, --jobs 4), and fails as it does. `check` reads
both directories through the path --check takes: collect, tally, apply_exclusions over the README's table, compare
against coverage.ratchet, and prints its findings and its verdict line."""
import subprocess
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / 'sw/firmware/gtest'))
import fw_coverage as c  # noqa: E402

mode = sys.argv[2]
print(f"toolchain: {c.fw_gtest.toolchain()}", flush=True)
if mode == 'run':
    name, keep = sys.argv[3], Path(sys.argv[4]).resolve()
    gate = dict(c.GATES)[name]
    argv = [sys.executable, str(gate), "--coverage", str(keep / name), "--jobs", "4"]
    print(f"argv: {argv}", flush=True)
    res = subprocess.run(argv, capture_output=True, text=True, check=False)
    tail = "\n".join((res.stdout + res.stderr).strip().splitlines()[-8:])
    print(f"[{'ok' if res.returncode == 0 else 'FAIL'}] {name} coverage run\n{tail}")
    sys.exit(0 if res.returncode == 0 else 2)
keep = Path(sys.argv[3]).resolve()
merged = c.collect([keep / name for name, _ in c.GATES])
raw = c.tally(merged)
kept_lines, found = c.apply_exclusions(merged, c.exclusions(c.README.read_text(encoding="utf-8")))
kept = c.tally(kept_lines)
c.report(raw, kept)
drops = c.compare(kept, c.read_ratchet(c.RATCHET.read_text(encoding="utf-8")) if c.RATCHET.exists() else {})
for x in found + drops:
    print(f"FINDING: {x}")
print(f"firmware coverage: {'FAIL' if found or drops else 'PASS'} ({len(kept)} files)")
sys.exit(1 if found or drops else 0)
