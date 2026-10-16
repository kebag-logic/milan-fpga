"""Run every gate step of the committed docs workflow natively, one log and rc per step.

Usage: run_docs_gates.py <repo> <out> <venv> <scratch>
Runner-install steps are replaced by the prepared venv and the pinned sv2v.
"""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import yaml

repo, out, venv, scratch = (Path(a) for a in sys.argv[1:5])
out.mkdir(parents=True)
scratch.mkdir(parents=True, exist_ok=True)
SKIP = {
    "Set CPU-derived job budgets": "exported below from nproc",
    "Install the python gate dependencies": "venv",
    "Install the pinned Markdown renderer": "venv",
    "Install diagram gate dependencies": "venv; rsvg-convert is on the host",
    "Install the pinned sv2v release": "the pinned sv2v v0.0.12 binary is on PATH",
    "Record executed gate outcomes": "hosted evidence plumbing",
    "Record actual job execution": "hosted evidence plumbing",
    "Fetch inventory dependencies": None,
    "Resolve exact package downloads 6": "apt download planner; this host has no apt and already carries rsvg-convert",
}
wf = yaml.safe_load((repo / ".github/workflows/docs.yml").read_text())
cpus = os.cpu_count()
temp = scratch / "runner-temp"
(temp / "gate-results").mkdir(parents=True, exist_ok=True)
env = dict(os.environ)
env.update({
    "PATH": f"{venv}/bin:$VALIDATION_TOOLS/sv2v-v0.0.12:" + env["PATH"],
    "RUNNER_TEMP": str(temp), "GITHUB_OUTPUT": str(scratch / "github_output"),
    "GITHUB_ENV": str(scratch / "github_env"), "GITHUB_PATH": str(scratch / "github_path"),
    "PIP_CONSTRAINT": str(repo / "ci/constraints-ci.txt"),
    "TMPDIR": str(scratch / "tmp"),
    "CI_BUILD_JOBS": str(cpus), "CI_TOOL_BUILD_JOBS": str(min(cpus, 8)),
    "CI_CAMPAIGN_JOBS": str(min(cpus, 4)), "VERILATOR_JOBS": str(cpus),
    "SIM_JOBS": str(min(cpus, 4)), "MAKEFLAGS": "-j1 --no-print-directory",
    "EVENT_NAME": "push", "PUSH_BEFORE_SHA": "9ef717727e6fdac11ee7f01672fefae948452343",
})
(scratch / "tmp").mkdir(exist_ok=True)
nogit = scratch / "nogit"
if not nogit.exists():
    nogit.mkdir()
    arc = subprocess.run(["git", "-C", str(repo), "archive", "HEAD"], capture_output=True, check=True).stdout
    subprocess.run(["tar", "-x", "-C", str(nogit)], input=arc, check=True)
plan = []
order = [("docs-gates-0", repo), ("docs-check-no-git", nogit), ("docs-gates-2", repo), ("docs-gates-1", repo)]
for job, cwd in order:
    for index, step in enumerate(wf["jobs"][job]["steps"]):
        name = step.get("name", "")
        if "run" not in step or name in SKIP:
            continue
        if job in ("docs-gates-1", "docs-gates-2") and index < 14:
            continue  # the shared setup and source steps already ran in docs-gates-0
        script = step["run"]
        if name == "Install and verify the pinned RV32 SDK":
            script = script.replace('"$HOME/br-milan-rv32/host"', f'"{scratch}/rv32-sdk-check/host"')
        if name == "Retain checkout identity before removing metadata":
            cwd_ = repo
        else:
            cwd_ = cwd
        plan.append((f"{job}/{index} {name}", cwd_, script))
summary = []
for n, (label, cwd, script) in enumerate(plan, 1):
    path = out / f"{n:02d}.sh"
    path.write_text(script)
    began = time.monotonic()
    with (out / f"{n:02d}.log").open("w") as log:
        rc = subprocess.run(["bash", "-e", str(path)], cwd=cwd, env=env, stdout=log,
                            stderr=subprocess.STDOUT).returncode
    row = {"n": n, "label": label, "rc": rc, "seconds": round(time.monotonic() - began)}
    summary.append(row)
    print(f"{n:02d}\t{rc}\t{row['seconds']}s\t{label}", flush=True)
(out / "summary.json").write_text(json.dumps(summary, indent=1))
print("FAILED" if any(r["rc"] for r in summary) else "ALL STEPS RC 0")
