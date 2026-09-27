#!/usr/bin/env python3
"""R347-4 mutants of the round-4 tu oracle and plan contract.

Usage: python3 -B mutants_r4.py <repo-root> <scratch-dir>

Extracts HEAD with `git archive` into <scratch-dir>/tree, then for each
mutant rewrites tb/tools/torture_campaign.py there (exactly one anchor must
match), runs the planner self-test and the plan feature, and restores the
file. A mutant is KILLED when either gate exits nonzero; an anchor that does
not match exactly once is INVALID and never counted as a kill. The reviewed
clone is never written.
"""
from __future__ import annotations

import subprocess
import sys
import tarfile
import io
from pathlib import Path

F = "tb/tools/torture_campaign.py"
MUTANTS = (
    ("T01 anchor at first event", "last_discontinuity_s = max(events_s)",
     "last_discontinuity_s = min(events_s)"),
    ("T02 event at interval start excluded", "if start_s <= event_s < clear_s]",
     "if start_s < event_s < clear_s]"),
    ("T03 event at clear instant counted", "if start_s <= event_s < clear_s]",
     "if start_s <= event_s <= clear_s]"),
    ("T04 events outside the interval counted",
     "events_s = [event_s for event_s in discontinuities_s if start_s <= event_s < clear_s]",
     "events_s = list(discontinuities_s)"),
    ("T05 deadline exclusive", 'return ("PASS" if clear_s <= deadline_s else "FAIL",',
     'return ("PASS" if clear_s < deadline_s else "FAIL",'),
    ("T06 deadline from interval start",
     "deadline_s = last_discontinuity_s + holdover_bound_s + observation_resolution_s",
     "deadline_s = start_s + holdover_bound_s + observation_resolution_s"),
    ("T07 incomplete capture graded", "if (capture_complete is not True or len(interval_s) != 2",
     "if (len(interval_s) != 2"),
    ("T08 zero resolution refused", "or observation_resolution_s < 0:",
     "or observation_resolution_s <= 0:"),
    ("T09 non-finite values graded", " or not math.isfinite(value)", ""),
    ("T10 uncorrelated tu skipped", 'return "FAIL", {"why": "uncorrelated tu fails"}',
     'return "SKIP", {"why": "uncorrelated tu fails"}'),
    ("T11 kinds drop GM-identity edge",
     'tu_discontinuity_kinds=["PHC settime/adjtime", "fabric discontinuity", "GM-identity edge"],',
     'tu_discontinuity_kinds=["PHC settime/adjtime", "fabric discontinuity"],'),
    ("T12 double resolution",
     "deadline_s = last_discontinuity_s + holdover_bound_s + observation_resolution_s",
     "deadline_s = last_discontinuity_s + holdover_bound_s + 2 * observation_resolution_s"),
    ("T13 assertion text anchors first event",
     '"measure from the last recorded discontinuity before tu clears; "',
     '"measure from the first recorded discontinuity; "'),
    ("T14 assertion text drops accepted kinds",
     '"PHC settime/adjtime, fabric discontinuity, or GM-identity edge; "', '""'),
    ("T15 bool resolution accepted", "type(value) not in (int, float)",
     "not isinstance(value, (int, float))"),
    # Informational: the start-edge tolerance F1 asks for. Expected to SURVIVE,
    # showing the fix is compatible with every current arm.
    ("I01 start edge honors resolution (informational)",
     "if start_s <= event_s < clear_s]",
     "if start_s - observation_resolution_s <= event_s < clear_s]"),
)


def run(cmd: list[str], cwd: Path) -> int:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=900).returncode


def main() -> int:
    repo, scratch = Path(sys.argv[1]), Path(sys.argv[2])
    tree = scratch / "tree"
    if tree.exists():
        subprocess.run(["rm", "-rf", str(tree)], check=True)
    tree.mkdir(parents=True)
    blob = subprocess.run(["git", "-C", str(repo), "archive", "HEAD"], check=True,
                          capture_output=True).stdout
    tarfile.open(fileobj=io.BytesIO(blob)).extractall(tree, filter="data")
    target = tree / F
    original = target.read_text(encoding="utf-8")
    gates = ([sys.executable, "-B", F, "--self-test"],
             [sys.executable, "-B", "-m", "behave", "tests/features/torture_campaign_plan.feature",
              "-f", "plain", "--no-capture"])
    base = [run(g, tree) for g in gates]
    print(f"BASELINE self-test rc={base[0]} behave rc={base[1]}")
    if any(base):
        return 1
    killed = survived = invalid = 0
    for name, old, new in MUTANTS:
        if original.count(old) != 1:
            print(f"INVALID {name}: anchor count {original.count(old)}")
            invalid += 1
            continue
        target.write_text(original.replace(old, new), encoding="utf-8")
        rcs = [run(g, tree) for g in gates]
        target.write_text(original, encoding="utf-8")
        state = "KILLED" if any(rcs) else "SURVIVED"
        killed += state == "KILLED"
        survived += state == "SURVIVED"
        print(f"{state} {name}: self-test rc={rcs[0]} behave rc={rcs[1]}")
    print(f"TOTAL killed={killed} survived={survived} invalid={invalid}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
