#!/usr/bin/env python3
"""Round-2 receipts for R897-1-F1, run against a lane checkout.

Usage: python3 -I skipped_matrix_receipts.py CHECKOUT ROUND1_COMMIT
1. The committed self-test control, applied to the round-1 committed workflows, must refuse them.
2. Every job with no matrix, in every generated workflow, at HEAD and at ROUND1_COMMIT: list each
   `${{ matrix.` occurrence (the expression-in-key pattern), and each expression in the watcher's
   two job lists.
3. A generator plant: a job whose display name equals an unexpanded matrix name must be refused.
"""
import copy
import json
from pathlib import Path
import re
import subprocess
import sys

import yaml

root = Path(sys.argv[1]).resolve()
round1 = sys.argv[2]
sys.dont_write_bytecode = True
sys.path.insert(0, str(root / "scripts"))
import ci_fail_fast_selftest as control  # noqa: E402
from ci_gate_workflows import ROOT, load_template  # noqa: E402
from ci_runtime_workflows import generate  # noqa: E402

NAMES = ("docs", "elaborate", "rtl", "rtl-fast")


def at(commit: str, name: str) -> dict:
    """One workflow file's bytes at a commit."""
    text = subprocess.run(["git", "-C", str(root), "show", f"{commit}:.github/workflows/{name}.yml"],
                          check=True, capture_output=True, text=True).stdout
    return yaml.safe_load(text)


print("1. committed control against the round-1 committed workflows at", round1)
for name in NAMES:
    workflow = at(round1, name)
    try:
        control.watcher_runtime_control(workflow)
    except AssertionError as caught:
        print(f"   {name}: CAUGHT: {caught}")
    else:
        print(f"   {name}: passes (no skipped matrix)")

print("2. matrix expressions inside jobs with no matrix")
for label, commit in (("HEAD", "HEAD"), ("round 1", round1)):
    for name in NAMES:
        workflow = at(commit, name)
        for job_id, job in workflow["jobs"].items():
            if "matrix" in job.get("strategy", {}):
                continue
            text = json.dumps(job)
            hits = sorted(set(re.findall(r"\$\{\{\s*matrix[^}]*\}\}", text)))
            if hits:
                print(f"   {label} {name}:{job_id}: {hits}")
        observer = next(s for s in workflow["jobs"]["ci-fail-fast"]["steps"] if s.get("id") == "ci_observe")
        for key in ("EXPECTED_JOBS", "SKIPPED_MATRICES"):
            found = re.findall(r"\$\{\{.*?\}\}", observer["env"][key])
            print(f"   {label} {name} {key}: {len(found)} expression(s) {sorted(set(found))}")

print("3. generator plant: the shard matrix left unnamed, and a plain job named as its unexpanded id")
source = load_template(ROOT, "rtl-fast")
unnamed = copy.deepcopy(source)
del unnamed["jobs"]["firmware-boundary-shards"]["name"]
generate("rtl-fast", unnamed)
print("   control: the unnamed matrix alone generates (raw 'firmware-boundary-shards', expanded "
      "'firmware-boundary-shards (0, 3)' ...)")
planted = copy.deepcopy(unnamed)
planted["jobs"]["planted-collision"] = {"name": "firmware-boundary-shards", "runs-on": "ubuntu-24.04",
                                        "steps": [{"run": "true"}]}
try:
    generate("rtl-fast", planted)
except ValueError as caught:
    print("   REFUSED:", caught)
else:
    print("   NOT REFUSED")
    sys.exit(1)
