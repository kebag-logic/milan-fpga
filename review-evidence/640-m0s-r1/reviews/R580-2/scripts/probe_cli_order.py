#!/usr/bin/env python3
"""R580-2 probe P10: argument order of `record --write` on the running interpreter.

Usage: python3 -B probe_cli_order.py <repo> <scratch>
Builds the gate self-test route fixture, plants the wrapper-retaining F0-F4 hierarchy
(no marker, no census), and runs record with --write before and after the directory.
"""
import json
import shutil
import sys
from pathlib import Path

repo, scratch = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(repo / "syn/ooc"))
import pp_resource_gate as gate  # noqa: E402
from pp_resource_gate_selftest import POLICY, cli, fixture  # noqa: E402

shutil.rmtree(scratch, ignore_errors=True)
folder = fixture(scratch / "f", "route")
pristine = json.dumps({"endpoints": {"route-1x1": {"record": gate.record(folder, "route"), **POLICY}}})
report = folder / "baseline_hierarchy.rpt"
report.write_text("".join(line for line in report.read_text().splitlines(keepends=True)
                          if not any(m in line for m in ("KL_adp_engine", "KL_pp_acmp_listener", "KL_acmp_talker",
                                                          "KL_srp_top", "| KL_maap |"))))
print(sys.version.split()[0])
for label, argv in (("documented: record <dir> --endpoint E --write", ("record", folder, "--write")),
                    ("self-test order: record --write <dir> --endpoint E", ("record", "--write", folder))):
    baseline = scratch / "baseline.json"
    baseline.write_text(pristine)
    status, lines = cli(*argv, "--endpoint", "route-1x1", "--baseline", baseline)
    print(f"{label}\texit {status}\tbaseline_changed={baseline.read_text() != pristine}\t{(lines[-1] if lines else '')[:200]}")
