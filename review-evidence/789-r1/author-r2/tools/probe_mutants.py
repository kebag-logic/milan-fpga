#!/usr/bin/env python3
"""Generator mutants of rtl-fast's Yosys derivation, each judged by the three hosted judges.

Usage: python3 -I probe_mutants.py <tree> <scratch-dir> <out.json> <submodule-source>

<submodule-source> is a worktree whose initialised submodules (verified at <tree>'s gitlinks) are
linked into each copy, because other self-test arms read the testbench Makefiles that include them.

Each mutant edits scripts/ci_gate_workflows.py in a fresh copy of <tree> (one anchored insertion in
fast_yosys_tool, just before the verdict is wired), regenerates the workflows with the mutated
generator, then runs `ci_gate_workflows.py --check`, `ci_gate_workflows_selftest.py` and
`ci_events.py --check`. A mutant SURVIVES when all three exit 0. The control is the unmutated copy.
"""

import json
import shutil
import subprocess
import sys
from pathlib import Path

ANCHOR = "    require_fast_tool(jobs[FAST_AGGREGATE])\n"


def drop(name: str) -> str:
    """Remove one retained yosys-elaboration step from the derivation's output."""
    return '    consumer["steps"] = [step for step in consumer["steps"] if step.get("name") != ' + repr(name) + "]\n"


MUTANTS = {
    "control": None,
    "G01 drop Elaborate the integration-heavy tops": drop("Elaborate the integration-heavy tops"),
    "G02 drop the version proof": drop("Install the pinned Yosys and prove the version"),
    "G03 drop Fetch RTL dependencies": drop("Fetch RTL dependencies"),
    "G04 drop Prove the result cache refuses a planted entry": drop("Prove the result cache refuses a planted entry"),
    "G05 drop Install the pinned sv2v release": drop("Install the pinned sv2v release"),
    "G06 drop Prove ooc.sh generates the ROMs and fails on a failed top":
        drop("Prove ooc.sh generates the ROMs and fails on a failed top"),
    "G07 drop Prove both synthesis flows refuse active elaboration guards":
        drop("Prove both synthesis flows refuse active elaboration guards"),
    "G08 drop Prove the OOC read sets come from run.sh and refuse a bad one":
        drop("Prove the OOC read sets come from run.sh and refuse a bad one"),
    "G09 swap the two ooc self-tests": (
        '    steps = consumer["steps"]\n'
        '    first = [step.get("name") for step in steps].index('
        '"Prove ooc.sh generates the ROMs and fails on a failed top")\n'
        '    steps[first], steps[first + 1] = steps[first + 1], steps[first]\n'),
    "G10 extra step in the tool job": '    tool["steps"].append({"name": "Planted step", "run": "true\\n"})\n',
}
JUDGES = (("ci_gate_workflows --check", ["python3", "scripts/ci_gate_workflows.py", "--check"]),
          ("ci_gate_workflows_selftest", ["python3", "scripts/ci_gate_workflows_selftest.py"]),
          ("ci_events --check", ["python3", "scripts/ci_events.py", "--check"]))


SUBMODULES = ("gptp-processor", "protocol-processor", "third_party/verilog-axis")


def words(text: str) -> str:
    """Why a judge refused: its last line, which is the exception or the refusal it printed."""
    lines = [line for line in text.splitlines() if line.strip()]
    return (lines[-1].strip() if lines else "")[:400]


def main() -> int:
    tree, scratch, out, modules = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4])
    rows = []
    for label, insertion in MUTANTS.items():
        copy = scratch / ("m" + str(len(rows)))
        shutil.rmtree(copy, ignore_errors=True)
        shutil.copytree(tree, copy, symlinks=True)
        for module in SUBMODULES:
            target = copy / module
            if target.is_dir() and not any(target.iterdir()):
                target.rmdir()
            target.symlink_to(modules / module, target_is_directory=True)
        generator = copy / "scripts/ci_gate_workflows.py"
        text = generator.read_text()
        assert text.count(ANCHOR) == 1, label
        if insertion is not None:
            generator.write_text(text.replace(ANCHOR, insertion + ANCHOR))
        regen = subprocess.run(["python3", "scripts/ci_gate_workflows.py"], cwd=copy, capture_output=True, text=True)
        row = {"mutant": label, "regenerate_rc": regen.returncode}
        if regen.returncode != 0:
            row["regenerate_words"] = words(regen.stdout + regen.stderr)
        verdicts = {}
        for name, command in JUDGES:
            done = subprocess.run(command, cwd=copy, capture_output=True, text=True)
            verdicts[name] = {"rc": done.returncode}
            if done.returncode != 0:
                verdicts[name]["words"] = words(done.stdout + done.stderr)
        row["judges"] = verdicts
        if regen.returncode != 0:
            row["outcome"] = "REFUSED by the generator"
        elif all(verdict["rc"] == 0 for verdict in verdicts.values()):
            row["outcome"] = "PASS (control)" if insertion is None else "SURVIVED"
        else:
            row["outcome"] = "KILLED"
        rows.append(row)
        shutil.rmtree(copy, ignore_errors=True)
        print(row["outcome"], "|", label, "|",
              row.get("regenerate_words") or "; ".join(name + " rc=" + str(v["rc"]) + (": " + v["words"] if "words" in v else "")
                                                       for name, v in verdicts.items()))
    out.write_text(json.dumps(rows, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
