#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Check P2's two DIFFERENT rows against the manager's P2 ruling (issue #640 comment 6089329720).

Usage: p2_ruling_check.py trees <repo> <base-commit> <scratch>
       p2_ruling_check.py cases <tree> <out>
  "trees": lay out base, head and hybrid trees under <scratch>
     base   = base-commit syn/ooc
     head   = working-tree syn/ooc (the exact head)
     hybrid = base gate code (pp_resource_gate.py, pp_baseline_rank.py) with the head's fixture modules
              (pp_resource_gate_selftest.py, pp_placement_selftest.py, pp_placement.py)
  "cases": run --fuzz 3000 --seed 234 in-process from <tree>, recording each case's label,
     broken flag and exit statuses in order, and the printed summary; write them to <out> as JSON.
The repository is read only.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

HEAD_FIXTURE = ("pp_resource_gate_selftest.py", "pp_placement_selftest.py", "pp_placement.py")


def trees(repo: Path, base: str, scratch: Path) -> None:
    shutil.rmtree(scratch, ignore_errors=True)
    for name in ("base", "head", "hybrid"):
        (scratch / name / "syn/ooc").mkdir(parents=True)
        (scratch / name / "docs/design").mkdir(parents=True)
    listing = subprocess.run(["git", "-C", str(repo), "ls-tree", "--name-only", base, "syn/ooc/"],
                             check=True, capture_output=True, text=True).stdout.split()
    for entry in listing:
        if entry.endswith((".py", ".json")):
            data = subprocess.run(["git", "-C", str(repo), "show", f"{base}:{entry}"], check=True,
                                  capture_output=True).stdout
            for name in ("base", "hybrid"):
                (scratch / name / entry).write_bytes(data)
    for path in sorted((repo / "syn/ooc").iterdir()):
        if path.suffix in (".py", ".json"):
            shutil.copy2(path, scratch / "head/syn/ooc" / path.name)
    for module in HEAD_FIXTURE:
        shutil.copy2(repo / "syn/ooc" / module, scratch / "hybrid/syn/ooc" / module)
    for name, rev in (("base", base), ("hybrid", base), ("head", "HEAD")):
        data = subprocess.run(["git", "-C", str(repo), "show", f"{rev}:docs/design/AREA_BUDGET.md"], check=True,
                              capture_output=True).stdout
        (scratch / name / "docs/design/AREA_BUDGET.md").write_bytes(data)


def cases(tree: Path, out: Path) -> None:
    sys.path.insert(0, str(tree / "syn/ooc"))
    import contextlib
    import io
    import pp_resource_gate as gate
    import pp_resource_gate_selftest as generated
    log, pending = [], {}
    mutate_json, mutate_report, run_case = generated.mutate_json, generated.mutate_report, gate.run_case

    def wrap_json(rng, base):
        result = mutate_json(rng, base)
        pending["label"], pending["broken"] = f"baseline: {result[0]}", result[2]
        return result

    def wrap_report(rng, name, text, kind):
        result = mutate_report(rng, name, text, kind)
        pending["label"], pending["broken"] = f"{name}: {result[0]}", result[2]
        pending["files"] = sorted(result[1])
        return result

    def wrap_run(work, target, files, data, audit):
        runs = run_case(work, target, files, data, audit)
        log.append({"target": target[1], "label": pending.pop("label", "control"),
                    "broken": pending.pop("broken", False), "statuses": [run[1] for run in runs],
                    "reason": [line for run in runs for line in run[2] if "NOT COMPARABLE" in line][:1]})
        pending.clear()
        return runs

    generated.mutate_json, generated.mutate_report, gate.run_case = wrap_json, wrap_report, wrap_run
    printed = io.StringIO()
    with contextlib.redirect_stdout(printed):
        status = gate.fuzz(3000, 234)
    summary = [line for line in printed.getvalue().splitlines() if "failures" in line]
    out.write_text(json.dumps({"tree": tree.name, "status": status, "summary": summary, "cases": log}, indent=0))


if __name__ == "__main__":
    if sys.argv[1] == "trees":
        trees(Path(sys.argv[2]).resolve(), sys.argv[3], Path(sys.argv[4]).resolve())
    else:
        cases(Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve())
