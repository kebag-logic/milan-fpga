#!/usr/bin/env python3
"""Offline bootstrap probe: load a runner copy (dev's trusted act_ci.py or the head's) from a file
and call only its validate_workflow_sandbox on a tree's shipping workflows. No Docker, no act.

Usage: bootstrap_probe.py <runner-act_ci.py> <label> <tree-root> <tree-label>
Prints ACCEPTED or the Refusal text, plus the runner's RUNS_ON_LABELS.
"""
import importlib.util
import pathlib
import sys

runner, label, root, tree_label = sys.argv[1], sys.argv[2], pathlib.Path(sys.argv[3]), sys.argv[4]
spec = importlib.util.spec_from_file_location("act_ci_probe", runner)
module = importlib.util.module_from_spec(spec)
sys.modules["act_ci_probe"] = module
spec.loader.exec_module(module)
workflows = tuple(module.WORKFLOWS)
try:
    module.validate_workflow_sandbox(root, workflows)
    verdict = "ACCEPTED"
except module.Refusal as exc:
    verdict = f"REFUSED: {exc}"
print(f"{label} runner (RUNS_ON_LABELS={module.RUNS_ON_LABELS}) on {tree_label} workflows {workflows}: {verdict}")
