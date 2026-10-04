#!/usr/bin/env python3
"""Mutation probes on a disposable copy of syn/resmap: does each self-test notice the mutation?

Usage: probe_selftests.py <copy root containing syn/resmap and syn/ooc>
Each arm rewrites one line in the copy, runs that script's --selftest, reports rc,
then restores the original bytes.
"""
import subprocess, sys
from pathlib import Path
root = Path(sys.argv[1]); d = root / "syn" / "resmap"
ARMS = [
  ("models: refused points kept in the stream fit", "resmap_models.py",
   'if point.get("patch") or point["name"] not in summary or refusals(summary, point["name"]):',
   'if point.get("patch") or point["name"] not in summary:'),
  ("models: refused points kept in the processor fits", "resmap_models.py",
   'if point["top"] != "KL_pp_shadow" or point["name"] not in summary or refusals(summary, point["name"]):',
   'if point["top"] != "KL_pp_shadow" or point["name"] not in summary:'),
  ("tables: page check reports stale as equal", "resmap_tables.py",
   "stale = text != args.page.read_text()", "stale = False"),
  ("map: partition tie disabled", "resmap_map.py",
   "        if total != rows[root][column]:\n            failures.append(f\"partition:",
   "        if False:\n            failures.append(f\"partition:"),
  ("sweep: guard refusal lines ignored", "yosys_sweep.py",
   'USER_GUARD = re.compile(r"^%(?:Warning|Error)-USER(?:ERROR|FATAL): (.*)$")',
   'USER_GUARD = re.compile(r"^NEVER(.*)$")'),
  ("sweep: summary tie disabled", "yosys_sweep.py",
   "        if tree[\"inclusive\"][top][column] != design[column]:", "        if False:"),
]
for what, name, old, new in ARMS:
    f = d / name; orig = f.read_text()
    assert orig.count(old) == 1, (what, orig.count(old))
    f.write_text(orig.replace(old, new))
    r = subprocess.run([sys.executable, str(f), "--selftest"], capture_output=True, text=True)
    f.write_text(orig)
    verdict = "CAUGHT (self-test fails)" if r.returncode else "NOT CAUGHT (self-test still passes)"
    print(f"{what:48s} -> {verdict}: {r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr.strip()[-120:]}")
