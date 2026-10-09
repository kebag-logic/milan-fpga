#!/usr/bin/env python3
"""Probe: what a printed `record` (no --write) does for each default-population plant.

Builds the gate self-test's route fixture in a scratch directory, plants the
wrapper row removed (the self-test's "wrapper absent" case, the one the head
exempts from the printed-record assertion) and a wrapper-retaining F0-F4
population, and prints the exit status and the reason for a printed record in the
documented order. Writes nothing outside <scratch>.

Usage: probe_wrapper_absent_printed.py <repo> <scratch>
"""

import shutil
import sys
from pathlib import Path

repo, scratch = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(repo / "syn/ooc"))
from pp_resource_gate_selftest import cli, fixture  # noqa: E402

shutil.rmtree(scratch, ignore_errors=True)
folder = fixture(scratch / "f", "route")
report = folder / "baseline_hierarchy.rpt"
original = report.read_text()
rows = original.splitlines(keepends=True)
wrapper = next(line for line in rows if "| KL_pp_shadow |" in line)
moved = ("KL_adp_engine", "KL_pp_acmp_listener", "KL_acmp_talker", "KL_srp_top", "| KL_maap |")
print(sys.version.split()[0])
for label, text in (("wrapper absent", original.replace(wrapper, "")),
                    ("wrapper-retaining f0-f4", "".join(line for line in rows if not any(m in line for m in moved)))):
    report.write_text(text)
    status, lines = cli("record", folder, "--endpoint", "route-1x1")
    reason = next((line for line in lines if "NOT COMPARABLE" in line), lines[1] if len(lines) > 1 else "")
    print(f"{label}\tprinted record exit {status}\t{reason[:200]}")
report.write_text(original)
