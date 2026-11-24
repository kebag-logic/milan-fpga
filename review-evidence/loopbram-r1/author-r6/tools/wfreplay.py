"""Replay selected `run:` steps of one workflow at a checkout, as the hosted job runs them.

Usage: wfreplay.py <checkout> <workflow.yml> <outdir> --list
       wfreplay.py <checkout> <workflow.yml> <outdir> --steps N[,N...]

--list prints the numbered step table (job, step index, id, name) of every `run:` step.
--steps runs the named table rows one after another with bash -e (the runner's
default shell), the job's own environment variables, and a per-step RUNNER_TEMP (PIP_CONSTRAINT is
left unset: the local venv is pre-provisioned, so each step's install is a no-op),
then appends each outcome to <outdir>/results.json. The docs-check-no-git job runs
in an exported copy without git metadata, as on the hosted runner.
"""
import json
import os
import subprocess
import sys
import tarfile
import time
from pathlib import Path

import yaml

checkout, workflow, out = Path(sys.argv[1]).resolve(), sys.argv[2], Path(sys.argv[3]).resolve()
out.mkdir(parents=True, exist_ok=True)
document = yaml.safe_load((checkout / workflow).read_text())
table = []
for job, body in document["jobs"].items():
    for index, step in enumerate(body.get("steps", [])):
        if "run" in step:
            table.append((job, index, step.get("id", ""), step.get("name", ""), step["run"]))
if sys.argv[4] == "--list":
    for n, (job, index, ident, name, _) in enumerate(table):
        print(f"{n}\t{job}\t{index}\t{ident}\t{name}")
    sys.exit(0)
rows = [int(word) for word in sys.argv[5].split(",")]
venv = "$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python3"
shim = out / "shim"
shim.mkdir(exist_ok=True)
for name in ("python3", "python"):
    wrapper = shim / name
    wrapper.write_text(f'#!/bin/sh\nexec {venv} "$@"\n')
    wrapper.chmod(0o755)
head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=checkout, text=True).strip()
base = subprocess.check_output(["git", "rev-parse", "HEAD^1"], cwd=checkout, text=True).strip()
results_path = out / "results.json"
results = json.loads(results_path.read_text())["steps"] if results_path.exists() else []
for n in rows:
    job, index, ident, name, script = table[n]
    cwd = checkout
    if job == "docs-check-no-git":
        cwd = out / "nogit-copy"
        if not cwd.exists():
            cwd.mkdir()
            archive = out / "head.tar"
            subprocess.run(["git", "archive", "--format=tar", "-o", str(archive), "HEAD"], cwd=checkout, check=True)
            with tarfile.open(archive) as tar:
                tar.extractall(cwd, filter="tar")
            archive.unlink()
            (cwd / ".git").mkdir()
    temp = out / "runner" / f"{n:03d}"
    temp.mkdir(parents=True, exist_ok=True)
    nproc = os.cpu_count() or 1
    env = dict(os.environ, PATH=f"{shim}:/usr/local/bin:/usr/bin:/bin", RUNNER_TEMP=str(temp),
               GITHUB_OUTPUT=str(temp / "output"), GITHUB_ENV=str(temp / "env"),
               GITHUB_STEP_SUMMARY=str(temp / "summary"), GITHUB_WORKSPACE=str(checkout),
               GITHUB_SHA=head, EVENT_NAME="pull_request", PR_BASE_REF="dev-soft-core",
               PUSH_BEFORE_SHA=base, TMPDIR=str(temp), PYTHONDONTWRITEBYTECODE="1",
               CI_BUILD_JOBS="4", CI_TOOL_BUILD_JOBS="4", CI_CAMPAIGN_JOBS="4", VERILATOR_JOBS="4",
               SIM_JOBS="4", MAKEFLAGS="-j1 --no-print-directory")
    log = out / f"{n:03d}-{job}-{index}.log"
    start = time.time()
    with log.open("w") as stream:
        stream.write(f"JOB {job} STEP {index} {ident} {name}\nHEAD {head}\n")
        stream.flush()
        rc = subprocess.run(["bash", "--noprofile", "--norc", "-eo", "pipefail", "-c", script], cwd=cwd,
                            env=env, stdout=stream, stderr=subprocess.STDOUT).returncode
    dirty = subprocess.check_output(["git", "status", "--porcelain"], cwd=checkout, text=True)
    row = dict(n=n, job=job, step=index, id=ident, name=name, exit=rc,
               seconds=round(time.time() - start, 1), log=log.name, tree_dirty_after=bool(dirty))
    results = sorted([r for r in results if r["n"] != n] + [row], key=lambda r: r["n"])
    results_path.write_text(json.dumps(dict(head=head, workflow=workflow, steps=results), indent=2) + "\n")
    print(f"{n:03d} {job} {ident} {name}: exit {rc} in {row['seconds']} s", flush=True)
