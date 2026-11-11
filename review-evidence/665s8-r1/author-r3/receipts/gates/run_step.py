#!/usr/bin/env python3
"""Run one `run:` step of a job again, in the job's existing clone, with run_wf.py's environment.

usage: run_step.py <workflow name> <head sha> <job> <scratch root> <python bin dir> <step id> <suffix>

For a step whose result was UNKNOWN (a wall-clock kill): the clone must be at the head and clean, the job's
own earlier steps having already run in it. The log and rc go beside the job's as <tag>-<suffix>.log/.rc,
so every attempt is kept.
"""
import os, subprocess, sys
from pathlib import Path
import yaml

HOME = "<scratch>/gates/home"
TOOLS = ("<scratch>/gates/bin:"
         "<data>/tools/pinned-verilator-5.050:<data>/tools/sv2v-v0.0.12:"
         "<data>/scratch/a662/make43/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin")
wf_name, head, job, root, venv, sid, suffix = sys.argv[1:8]
root = Path(root); work = root / job; wt = work / "wt"; logs = root / "logs"
run = lambda *a: subprocess.run(a, cwd=wt, check=True, capture_output=True, text=True).stdout.strip()
assert run("git", "rev-parse", "HEAD") == head
assert run("git", "status", "--porcelain") == ""
env = {k: v for k, v in os.environ.items() if k in ("LANG", "LC_ALL", "USER", "TERM")}
env.update(PATH=f"{venv}:{TOOLS}", HOME=HOME, RUNNER_TEMP=str(work / "runner_temp"), TMPDIR=str(work / "tmp"),
           GITHUB_WORKSPACE=str(wt), GITHUB_ENV=str(work / "github_env"), GITHUB_OUTPUT=str(work / "github_output"),
           GITHUB_PATH=str(work / "github_path"), GITHUB_SHA=head, CI="true", GIT_ALLOW_PROTOCOL="file:https",
           PYTHONHASHSEED="0", COURSIER_MODE="offline", SBT_OPTS="-Dsbt.offline=true",
           VERILATOR="<data>/tools/pinned-verilator-5.050/verilator", VERILATOR_VERSION="v5.050",
           YOSYS_VERSION="v0.66", TSN_GEN_ROOT="<home>/milan-fpga-management/tools/tsn-gen-deca300c",
           EVENT_NAME="pull_request", PR_BASE_REF="dev-soft-core", PR_HEAD_SHA=head, PUSH_BEFORE_SHA="",
           GITHUB_EVENT_NAME="pull_request", TARGET_SHA=head, GITHUB_REPOSITORY="kebag-logic/milan-fpga",
           GITHUB_REF="refs/heads/665-s8-wire-timing", PR_DRAFT="false")
for line in (work / "github_env").read_text().splitlines():
    if "=" in line:
        k, v = line.split("=", 1)
        env[k] = v
wf = yaml.safe_load((wt / f".github/workflows/{wf_name}.yml").read_text())
step = next(s for n, s in enumerate(wf["jobs"][job]["steps"]) if "run" in s and (s.get("id") or f"step{n}") == sid)
for k, v in (step.get("env") or {}).items():
    if isinstance(v, str) and "${{" not in v:
        env[k] = v
script = work / f"{sid}-{suffix}.sh"
script.write_text(step["run"])
tag = f"{wf_name}__{job}__{sid}-{suffix}"
with open(logs / f"{tag}.log", "w") as out:
    out.write(f"# head {head} workflow {wf_name} job {job} step {sid} ({suffix}): {step.get('name')}\n# clone {wt}\n")
    out.flush()
    rc = subprocess.run(["bash", "-e", str(script)], cwd=wt / step.get("working-directory", "."), env=env, stdout=out,
                        stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL).returncode
(logs / f"{tag}.rc").write_text(f"{rc}\n")
(logs / f"{tag}.tree-after.txt").write_text(run("git", "status", "--porcelain") + "\n")
print(f"{tag}\trc={rc}", flush=True)
