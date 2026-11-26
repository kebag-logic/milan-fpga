#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Prove complete fast-job dispatch and execute its failure-to-context path (#1008)."""

from __future__ import annotations

from collections import Counter
from contextlib import redirect_stdout, redirect_stderr
import copy
from io import StringIO
import os
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace
from unittest.mock import patch

from ci_gate_workflows import ROOT, generate, load_template
from ci_runtime_workflows import SAME_REPOSITORY

sys.path.insert(0, str(ROOT / "sw/firmware/ctrl/test"))
import test_ctrl_firmware as firmware  # noqa: E402
import test_ctrl_firmware_shards as dispatch  # noqa: E402
sys.path.insert(0, str(ROOT / "sw/mailbox"))
import census_legs  # noqa: E402


def campaign_controls() -> None:
    """Use real dispatch and live tables, with a failed campaign injected into each leg."""
    for phase, table, module, count in ((1, firmware.ctrl_mutants.MUTANTS, firmware.ctrl_mutants, 4),):
        expected = Counter(item.name for item in table)
        actual = Counter(item.name for leg in range(count) for item in table[leg::count])
        assert actual == expected
        for leg in range(count):
            args = SimpleNamespace(shard=(phase, 4), self_test=True, jobs=4, slice=(1, 1),
                                   mutation_shard=(leg, count))
            with patch.object(module, "campaign", return_value=True) as campaign:
                assert firmware.run_selected(args, SimpleNamespace(reuse=Path("reuse")), Path("build"))
                assert campaign.call_args.args[-1] == (leg, count)
        print(f"PASS: phase {phase}, {len(table)} defects exactly once; every failed leg propagates")
    for argv in (["--campaign-shard", "0", "4"],
                 ["--shard", "0/4", "--self-test", "--campaign-shard", "0", "4"],
                 ["--shard", "1/4", "--self-test", "--campaign-shard", "4", "4"],
                 ["--shard", "1/4", "--self-test", "--campaign-shard", "0", "0"]):
        with redirect_stderr(StringIO()):
            try:
                firmware.main(argv)
            except SystemExit as exc:
                assert exc.code == 2
            else:
                raise AssertionError("accepted invalid campaign selection")


def census_controls() -> None:
    """Build receipts from the actual arm inventory; independently corrupt each proof field."""
    every = census_legs.inventory()
    identity = ("a" * 40, "b" * 40)
    records = []
    for leg in range(census_legs.LEGS):
        groups = census_legs.selection(every, leg)
        rows = [{"arm": arm.what, "ok": True, "line": "passed " + arm.what,
                 "through": None if arm.rule is None else True}
                for host, _, riders in groups for arm in (host, *riders)]
        records.append({"schema": 1, "head": identity[0], "tree": identity[1], "leg": leg,
                        "legs": census_legs.LEGS, "inventory": census_legs.names(every),
                        "selected": census_legs.names(groups), "rows": rows, "exit": 0})
    with redirect_stdout(StringIO()):
        assert census_legs.union(records, every, identity) == 0
    defects = []
    for leg in range(census_legs.LEGS):
        bad = copy.deepcopy(records)
        bad[leg]["exit"] = 1
        defects.append((f"failed leg {leg}", bad))
        defects.append((f"missing leg {leg}", records[:leg] + records[leg+1:]))
    for field, value in (("head", "c" * 40), ("tree", "c" * 40), ("inventory", []),
                         ("selected", []), ("rows", [])):
        bad = copy.deepcopy(records)
        bad[1][field] = value
        defects.append((field, bad))
    defects.append(("duplicate leg", [*records, records[1]]))
    for leg in range(1, census_legs.LEGS):
        bad = copy.deepcopy(records)
        next(row for row in bad[leg]["rows"] if row["through"] is not None)["through"] = False
        defects.append((f"rule removal escaped in leg {leg}", bad))
    for label, bad in defects:
        try:
            with redirect_stdout(StringIO()):
                rc = census_legs.union(bad, every, identity)
        except ValueError:
            rc = 1
        assert rc != 0, label
        print("PASS: census refuses planted " + label)
    print(f"PASS: census {len(census_legs.names(every))} executed arms exactly once with unchanged rule judge")


def workflow_controls() -> None:
    """Execute the generated required-context shell with each split job's failing result."""
    original = load_template(ROOT, "rtl-fast")
    workflow = generate("rtl-fast", original)
    jobs = workflow["jobs"]
    for name, count in (("firmware-control-mutants", 4), ("firmware-unit", 3),
                        ("publication-census-legs", census_legs.LEGS)):
        assert jobs[name]["strategy"] == {"fail-fast": True, "matrix": {"leg": list(range(count))}}
        assert "permissions" not in jobs[name]
    assert jobs["ci-fail-fast"]["if"] == SAME_REPOSITORY
    step = next(step for step in jobs["rtl-fast"]["steps"]
                if step["name"] == "Require every applicable fast gate to pass")
    env = {**os.environ, **{key: "success" for key in step["env"]}}
    assert subprocess.run(["bash", "-c", step["run"]], env=env, capture_output=True).returncode == 0
    for name in ("firmware-control-mutants", "firmware-unit", "publication-census-legs"):
        for result in ("failure", "cancelled"):
            changed = {**env, name.upper().replace("-", "_") + "_RESULT": result}
            if name == "publication-census-legs":
                changed["PUBLICATION_CENSUS_RESULT"] = "skipped"
            assert subprocess.run(["bash", "-c", step["run"]], env=changed,
                                  capture_output=True).returncode != 0
            print(f"PASS: planted {name} {result} fails required rtl-fast shell")
    # No unit command disappeared or changed; each original gate runs on exactly one leg.
    source = original["jobs"]["firmware-unit"]["steps"]
    target = jobs["firmware-unit"]["steps"]
    for step in source:
        if step.get("name", "").startswith(("Run the ", "Hold the ", "Prove the ")):
            same = [s for s in target if s.get("name") == step["name"]]
            assert len(same) == 1 and same[0]["run"] == step["run"]
            assert same[0]["if"] in ("${{ matrix.leg == 0 }}", "${{ matrix.leg == 1 }}", "${{ matrix.leg == 2 }}")
    print("PASS: original unit command bytes and exhaustive matrix conditions")


def main() -> int:
    """Positive controls plus omitted work, failed execution and cancellation plants."""
    campaign_controls()
    census_controls()
    workflow_controls()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
