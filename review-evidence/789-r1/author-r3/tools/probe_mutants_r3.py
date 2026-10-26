#!/usr/bin/env python3
"""Generator mutants after and in rtl-fast's Yosys derivation, each judged by the three hosted judges.

Usage: python3 -I probe_mutants_r3.py <tree> <scratch-dir> <out.json> <submodule-source> <jobs>

<tree> is an export of one commit. <submodule-source> is a worktree whose initialised submodules (verified at
<tree>'s gitlinks) are linked into each copy, because other self-test arms read the testbench Makefiles that
include them.

A K mutant inserts lines at the end of bind_fast_tool_key, the key binding stage generate() runs after the
shared install and runtime transforms; K01 is the drop R707-2 calls N11. A G mutant inserts lines in
fast_yosys_tool, the derivation, just before the verdict is wired (the round-2 set). A D mutant replaces
text in the generator. Each mutant regenerates the
workflows with the mutated generator, then runs `ci_gate_workflows.py --check`, `ci_gate_workflows_selftest.py`
and `ci_events.py --check`. A mutant SURVIVES when all three exit 0. The control is the unmutated copy.
"""

import json
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

DERIVATION = "    require_fast_tool(jobs[FAST_AGGREGATE])\n"
BINDING = '        step["with"]["key"] = step["with"]["key"].replace(FAST_TOOL_RECIPE, recipe)\n'
REPLACE = "replace"
SUBMODULES = ("gptp-processor", "protocol-processor", "third_party/verilog-axis")
OOC = "Prove ooc.sh generates the ROMs and fails on a failed top"


def derived_drop(name: str) -> str:
    """Remove one retained yosys-elaboration step from the derivation's output."""
    return '    consumer["steps"] = [step for step in consumer["steps"] if step.get("name") != ' + repr(name) + "]\n"


def bound_drop(job: str, name: str) -> str:
    """Remove one step of an emitted job after the key is bound."""
    return ('    workflow["jobs"][' + repr(job) + ']["steps"] = [step for step in workflow["jobs"][' + repr(job)
            + ']["steps"] if step.get("name") != ' + repr(name) + "]\n")


def bound_step(job: str, name: str) -> str:
    """An expression for one named step of an emitted job."""
    return ('next(step for step in workflow["jobs"][' + repr(job) + ']["steps"] if step.get("name") == '
            + repr(name) + ")")


CONSUMER = "yosys-elaboration"
TOOL = "yosys-tool"
MUTANTS = {
    "control": None,
    "K01 binding drops Prove the result cache refuses a planted entry (N11)":
        (BINDING, bound_drop(CONSUMER, "Prove the result cache refuses a planted entry")),
    "K02 binding drops Elaborate the integration-heavy tops":
        (BINDING, bound_drop(CONSUMER, "Elaborate the integration-heavy tops")),
    "K03 binding drops the version proof":
        (BINDING, bound_drop(CONSUMER, "Install the pinned Yosys and prove the version")),
    "K04 binding drops Install the pinned sv2v release": (BINDING, bound_drop(CONSUMER, "Install the pinned sv2v release")),
    "K05 binding drops Fetch RTL dependencies": (BINDING, bound_drop(CONSUMER, "Fetch RTL dependencies")),
    "K06 binding swaps the two ooc self-tests": (BINDING, (
        '    steps = workflow["jobs"][' + repr(CONSUMER) + ']["steps"]\n'
        '    first = [step.get("name") for step in steps].index(' + repr(OOC) + ')\n'
        '    steps[first], steps[first + 1] = steps[first + 1], steps[first]\n')),
    "K07 binding rewrites a self-test body":
        (BINDING, "    " + bound_step(CONSUMER, "Prove the result cache refuses a planted entry") + '["run"] = "true\\n"\n'),
    "K08 binding adds a consumer step": (BINDING, (
        '    workflow["jobs"][' + repr(CONSUMER) + ']["steps"].append({"name": "Planted step", "run": "true\\n"})\n')),
    "K09 binding adds a tool step after the build": (BINDING, (
        '    workflow["jobs"][' + repr(TOOL) + ']["steps"].insert(-2, {"name": "Touch the built tree", '
        '"run": "touch /opt/yosys/planted\\n"})\n')),
    "K10 binding rewrites the tool evidence record":
        (BINDING, "    " + bound_step(TOOL, "Record actual job execution") + '["run"] = "touch /opt/yosys/planted\\n"\n'),
    "K11 binding sets a workflow env after the digest": (BINDING, '    workflow["env"]["CXXFLAGS"] = "-O0"\n'),
    "K12 binding gives the tool job an env after the digest":
        (BINDING, '    workflow["jobs"][' + repr(TOOL) + ']["env"] = {"CXXFLAGS": "-O0"}\n'),
    "K13 binding drops another job's step": (BINDING, bound_drop("verilator-lint", "Fetch RTL dependencies")),
    "K14 binding binds the restore to another recipe": (BINDING, (
        "    restore = " + bound_step(CONSUMER, "Restore the pinned Yosys build") + "\n"
        '    restore["with"]["key"] = re.sub(r"recipe-[0-9a-f]{64}", "recipe-" + "0" * 64, '
        'restore["with"]["key"])\n')),
    "K15 binding drops the tool build": (BINDING, bound_drop(TOOL, "Build Yosys from source on cache miss")),
    "G01 derivation drops Elaborate the integration-heavy tops":
        (DERIVATION, derived_drop("Elaborate the integration-heavy tops")),
    "G02 derivation drops the version proof": (DERIVATION, derived_drop("Install the pinned Yosys and prove the version")),
    "G03 derivation drops Fetch RTL dependencies": (DERIVATION, derived_drop("Fetch RTL dependencies")),
    "G04 derivation drops Prove the result cache refuses a planted entry":
        (DERIVATION, derived_drop("Prove the result cache refuses a planted entry")),
    "G05 derivation drops Install the pinned sv2v release": (DERIVATION, derived_drop("Install the pinned sv2v release")),
    "G06 derivation drops " + OOC: (DERIVATION, derived_drop(OOC)),
    "G07 derivation drops Prove both synthesis flows refuse active elaboration guards":
        (DERIVATION, derived_drop("Prove both synthesis flows refuse active elaboration guards")),
    "G08 derivation drops Prove the OOC read sets come from run.sh and refuse a bad one":
        (DERIVATION, derived_drop("Prove the OOC read sets come from run.sh and refuse a bad one")),
    "G09 derivation swaps the two ooc self-tests": (DERIVATION, (
        '    steps = consumer["steps"]\n'
        '    first = [step.get("name") for step in steps].index(' + repr(OOC) + ')\n'
        '    steps[first], steps[first + 1] = steps[first + 1], steps[first]\n')),
    "G10 derivation adds a tool-job step": (DERIVATION, '    tool["steps"].append({"name": "Planted step", "run": "true\\n"})\n'),
    # A replacement mutant: (REPLACE, old text, new text) in the generator.
    "D01 the digest omits the workflow defaults":
        (REPLACE, 'for key in ("env", "defaults")}', 'for key in ("env",)}'),
}
JUDGES = (("ci_gate_workflows --check", ["python3", "scripts/ci_gate_workflows.py", "--check"]),
          ("ci_gate_workflows_selftest", ["python3", "scripts/ci_gate_workflows_selftest.py"]),
          ("ci_events --check", ["python3", "scripts/ci_events.py", "--check"]))


def words(text: str) -> str:
    """Why a judge refused: its last line, which is the exception or the refusal it printed."""
    lines = [line for line in text.splitlines() if line.strip()]
    return (lines[-1].strip() if lines else "")[:600]


def run_one(index: int, label: str, tree: Path, scratch: Path, modules: Path) -> dict:
    """Copy, mutate, regenerate and judge one mutant."""
    copy = scratch / ("m" + str(index))
    shutil.rmtree(copy, ignore_errors=True)
    shutil.copytree(tree, copy, symlinks=True)
    for module in SUBMODULES:
        target = copy / module
        if target.is_dir() and not any(target.iterdir()):
            target.rmdir()
        target.symlink_to(modules / module, target_is_directory=True)
    generator = copy / "scripts/ci_gate_workflows.py"
    text = generator.read_text()
    mutation = MUTANTS[label]
    row = {"mutant": label}
    if mutation is not None:
        anchor, insertion = mutation[-2:]
        if text.count(anchor) != 1:
            shutil.rmtree(copy, ignore_errors=True)
            return {**row, "outcome": "ERROR anchor count " + str(text.count(anchor))}
        # A derivation insertion goes before its anchor; a binding insertion after the loop the anchor ends.
        text = text.replace(anchor, insertion if mutation[0] == REPLACE
                            else insertion + anchor if anchor == DERIVATION else anchor + insertion)
        generator.write_text(text)
    regen = subprocess.run(["python3", "scripts/ci_gate_workflows.py"], cwd=copy, capture_output=True, text=True)
    row["regenerate_rc"] = regen.returncode
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
        row["outcome"] = "PASS (control)" if mutation is None else "SURVIVED"
    else:
        row["outcome"] = "KILLED"
    shutil.rmtree(copy, ignore_errors=True)
    return row


def main() -> int:
    """Run every mutant and write one row each."""
    tree, scratch, out, modules = (Path(arg) for arg in sys.argv[1:5])
    jobs = int(sys.argv[5])
    scratch.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(jobs) as pool:
        rows = list(pool.map(lambda pair: run_one(pair[0], pair[1], tree, scratch, modules), enumerate(MUTANTS)))
    for row in rows:
        verdicts = row.get("judges", {})
        print(row["outcome"], "|", row["mutant"], "|",
              row.get("regenerate_words") or "; ".join(
                  name + " rc=" + str(v["rc"]) + (": " + v["words"] if "words" in v else "")
                  for name, v in verdicts.items()))
    out.write_text(json.dumps(rows, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
