#!/usr/bin/env python3
"""Offline, data-only act mapping of one exported head: no act and no Docker.

Usage: python3 -I act_offline_mapping.py <trusted-act_ci.py> <exported-tree> <head>

Loads dev's trusted runner as a module, runs its validate_workflow_sandbox over all four workflows of the tree,
and prints rtl-fast's dependency stages (a job with no need is stage 1) for the tool job, its consumer
and the aggregate.
"""

import importlib.util
import pathlib
import sys

import yaml


def main() -> int:
    """Validate the four sandboxes and print the three stages."""
    runner, tree, head = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), sys.argv[3]
    spec = importlib.util.spec_from_file_location("trusted_act_ci", runner)
    module = importlib.util.module_from_spec(spec)
    sys.modules["trusted_act_ci"] = module
    spec.loader.exec_module(module)
    print("Offline data-only sandbox and dependency mapping; no act or Docker execution.")
    print("Head: " + head)
    module.validate_workflow_sandbox(tree, list(module.WORKFLOWS))
    print("All " + str(len(module.WORKFLOWS)) + " workflow sandboxes accepted: " + ", ".join(module.WORKFLOWS))
    jobs = yaml.safe_load(tree.joinpath(".github/workflows/rtl-fast.yml").read_text())["jobs"]
    stage, placed = {}, set()
    while len(placed) < len(jobs):
        ready = [job for job in jobs if job not in placed and all(
            need in placed for need in ([jobs[job].get("needs")] if isinstance(jobs[job].get("needs"), str)
                                        else jobs[job].get("needs", [])))]
        if not ready:
            raise SystemExit("dependency cycle")
        for job in ready:
            needs = [jobs[job]["needs"]] if isinstance(jobs[job].get("needs"), str) else jobs[job].get("needs", [])
            stage[job] = 1 + max((stage[n] for n in needs), default=0)
            placed.add(job)
    for job in ("yosys-tool", "yosys-elaboration", "rtl-fast"):
        print("stage " + str(stage[job]) + ": " + job + ": " + jobs[job].get("name", job))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
