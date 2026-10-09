#!/usr/bin/env python3
"""Show whether the recipe's placement marker is what keeps a split route out of all-fabric acceptance.

Usage: probe_marker.py <repo> <scratch>
Builds the gate self-test's synthetic route fixture twice: an accepted all-fabric
record, and an F0-F4 candidate that keeps one wrapper (which pp_placement permits).
Runs the head's gate CLI on the candidate with and without the recipe's marker line.
Prints one row per case: label, expected, observed exit, baseline-changed, first reason.
"""

import json
from pathlib import Path
import shutil
import sys

repo, scratch = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(repo / "syn/ooc"))
import pp_placement  # noqa: E402
import pp_resource_gate as gate  # noqa: E402
from pp_resource_gate_selftest import POLICY, cli, fixture  # noqa: E402
from pp_placement_selftest import census_text  # noqa: E402

shutil.rmtree(scratch, ignore_errors=True)
scratch.mkdir(parents=True)
base = fixture(scratch / "base", "route")
entry = {"record": gate.record(base, "route"), **POLICY}
pristine = json.dumps({"endpoints": {"route-1x1": entry}})

candidate = fixture(scratch / "f0f4", "route")
script = candidate / "baseline_integrated.tcl"
legacy = script.read_text()
# F0-F4 population with the wrapper retained for AECP: wrapper 1, moved engines 0.
(candidate / pp_placement.REPORT).write_text(census_text("f0-f4", (1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1)))
failures = 0


def case(label: str, marked: bool, args: list[str], wanted: int) -> None:
    global failures
    baseline = scratch / "baseline.json"
    baseline.write_text(pristine)
    script.write_text((pp_placement.MARKER + "f0-f4\n" if marked else "") + legacy)
    status, lines = cli(*args[:1], candidate, "--endpoint", "route-1x1", "--baseline", baseline, *args[1:])
    changed = baseline.read_text() != pristine
    reason = next((line for line in lines if "NOT COMPARABLE" in line or "RESULT" in line), lines[-1] if lines else "")
    verdict = "as-expected" if status == wanted else "UNEXPECTED"
    failures += status != wanted
    print(f"{label}\twanted {wanted}\tgot {status}\tbaseline_changed={changed}\t{verdict}\t{reason[:150]}")


print("case\twanted\tobserved\tbaseline\tverdict\treason")
case("marked: check --placement f0-f4", True, ["check", "--placement", "f0-f4"], 0)
case("marked: check as all-fabric", True, ["check"], 2)
case("marked: record --write as all-fabric", True, ["record", "--write"], 2)
case("marked: record --write --placement f0-f4", True, ["record", "--write", "--placement", "f0-f4"], 2)
case("unmarked: check --placement f0-f4", False, ["check", "--placement", "f0-f4"], 2)
# Without the marker the same split directory is indistinguishable from all-fabric:
case("unmarked: check as all-fabric", False, ["check"], 0)
case("unmarked: record --write as all-fabric", False, ["record", "--write"], 0)
# The default selection reads no engine population: drop the SRP engine from the hierarchy too.
hierarchy = candidate / "baseline_hierarchy.rpt"
hierarchy.write_text("".join(line for line in hierarchy.read_text().splitlines(keepends=True) if "u_srp" not in line))
case("unmarked, SRP absent from hierarchy: check as all-fabric", False, ["check"], 0)
baseline = scratch / "baseline.json"
status, lines = cli("check", candidate, "--endpoint", "route-1x1", "--baseline", baseline)
print("  default-selection report lines: " + " | ".join(line.strip() for line in lines if "u_srp" in line or "RESULT" in line))
print(f"probe_marker: {failures} unexpected")
