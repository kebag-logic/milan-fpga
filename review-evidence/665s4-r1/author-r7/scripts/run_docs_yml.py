#!/usr/bin/env python3
"""Run one job of .github/workflows/docs.yml, step by step, on a fresh clean clone of a commit.

usage: run_docs_yml.py <head sha> <job> <scratch root>

The step list comes from the workflow in the clone, never from a list kept here.
Only NOT_RUN (not_run.json beside this file) may stand between a `run:` step and its
rc file, each with its reason; verify_docs_yml.py fails on any step with neither an rc
of 0 nor an entry.

As on a fresh hosted runner, each job has its own empty HOME and its own new virtual
environment under its scratch directory, so `$HOME/br-milan-rv32/host` is absent and
ci_rv32_sdk.py downloads, digest-checks, relocates and verifies the pinned SDK itself.
Neither the installer nor the workflow is changed, and no SDK or receipt is copied in.
The job's and each step's own `env:` is applied, `${{ github.workspace }}` read as the
clone. A failed step is recorded and the job goes on, so one run shows every failure;
the verifier refuses any rc but 0.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

import yaml

LANE = "$LANES/665-s4-f1-target"
ORIGIN = "https://github.com/kebag-logic/milan-fpga.git"
PY312 = "$VALIDATION_TOOLS/uvpy/cpython-3.12.3-linux-x86_64-gnu/bin/python3.12"
BASE = "a68536fa4cf8ce65c513874722de2e3ba83c2d00"
TOOLS = ("$VALIDATION_TOOLS/pinned-verilator-5.050:$VALIDATION_TOOLS/sv2v-v0.0.12:"
         "$VALIDATION_STORAGE/scratch/a662/make43/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin")
NOT_RUN = json.loads(Path(__file__).with_name("not_run.json").read_text())

head, job, root = sys.argv[1:4]
root = Path(root)
work = root / job
logs = root / "logs"
logs.mkdir(parents=True, exist_ok=True)
wt = work / "wt"
assert not wt.exists(), f"{wt} exists: a job runs on a fresh clone"
wt.parent.mkdir(parents=True, exist_ok=True)


def run(*a, cwd=None, env=None):
    return subprocess.run(a, cwd=cwd, env=env, check=True, capture_output=True, text=True).stdout.strip()


run("git", "clone", "-q", "--shared", "--no-checkout", LANE, str(wt))
run("git", "fetch", "-q", LANE, head, cwd=wt)
run("git", "-c", "advice.detachedHead=false", "checkout", "-q", "--detach", head, cwd=wt)
assert run("git", "rev-parse", "HEAD", cwd=wt) == head
assert run("git", "status", "--porcelain", cwd=wt) == ""
run("git", "remote", "set-url", "origin", ORIGIN, cwd=wt)
# A submodule's objects come from the lane's own clone, its gitlink from this commit.
gm = run("git", "config", "--blob", f"{head}:.gitmodules", "--get-regexp", r"^submodule\..*\.path$", cwd=wt)
for line in gm.splitlines():
    dep = line.split()[1]
    if (Path(LANE) / dep / ".git").exists():
        run("git", "config", f"submodule.{dep}.url", f"{LANE}/{dep}", cwd=wt)

home = work / "home"
home.mkdir()
assert not any(home.iterdir()), f"{home} is not empty: a job starts from an empty HOME"
temp = work / "runner_temp"
temp.mkdir()
tmp = work / "tmp"
tmp.mkdir()
gh_env = work / "github_env"
gh_env.touch()
gh_out = work / "github_output"
gh_out.touch()
venv = work / "venv"
run(PY312, "-m", "venv", str(venv))
env = {k: v for k, v in os.environ.items() if k in ("LANG", "LC_ALL", "USER", "TERM")}
env.update(PATH=f"{venv}/bin:{TOOLS}", HOME=str(home), RUNNER_TEMP=str(temp), TMPDIR=str(tmp),
           GITHUB_WORKSPACE=str(wt), GITHUB_ENV=str(gh_env), GITHUB_OUTPUT=str(gh_out),
           GITHUB_SHA=head, CI="true", GIT_ALLOW_PROTOCOL="file:https",
           VERILATOR="$VALIDATION_TOOLS/pinned-verilator-5.050/verilator",
           TSN_GEN_ROOT="$MANAGEMENT/tools/tsn-gen-deca300c")
STEP_ENV = {"gate_8": dict(EVENT_NAME="push", PR_BASE_REF="dev-soft-core", PUSH_BEFORE_SHA=BASE)}

wf = yaml.safe_load((wt / ".github/workflows/docs.yml").read_text())
body = wf["jobs"][job]
for k, v in (body.get("env") or {}).items():
    env[k] = str(v).replace("${{ github.workspace }}", str(wt))
# The pip half of the apt step not run here (not_run.json): the step's own pin, under the job's constraints.
if any(s.get("id") in ("ci_step_10", "ci_step_8") and "wavedrom==" in s.get("run", "") for s in body["steps"]):
    run(f"{venv}/bin/python3", "-m", "pip", "install", "--quiet", "wavedrom==2.0.3.post3", cwd=wt, env=env)

failed = 0
for n, step in enumerate(body["steps"]):
    if "run" not in step:
        continue
    sid = step.get("id") or f"step{n}"
    tag = f"{job}__{sid}"
    if f"{job}/{sid}" in NOT_RUN or sid in NOT_RUN:
        continue
    for line in gh_env.read_text().splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            env[k] = v
    e = dict(env)
    e.update(STEP_ENV.get(sid, {}))
    e.update({k: str(v).replace("${{ github.workspace }}", str(wt)) for k, v in (step.get("env") or {}).items()
              if "${{" not in str(v).replace("${{ github.workspace }}", "")})
    for dep in ("protocol-processor", "gptp-processor"):
        if (wt / dep / ".git").exists():
            assert run("git", "rev-parse", "--show-toplevel", cwd=wt / dep) == str(wt / dep)
            run("git", "remote", "get-url", "origin", cwd=wt / dep)
    # as GitHub runs a `run:` step with no shell named
    script = work / f"{sid}.sh"
    script.write_text(step["run"])
    log = logs / f"{tag}.log"
    with open(log, "w") as out:
        out.write(f"# head {head} job {job} step {sid}: {step.get('name')}\n# clone {wt}\n")
        out.flush()
        argv = ["bash", "-e", str(script)]
        if sid == "gate_42":
            isolated = work / "offline-source"
            run("git", "clone", "--no-local", "-q", str(wt), str(isolated))
            (isolated / "offline-step.sh").write_text(step["run"])
            argv = ["docker", "run", "--rm", "--network=none", "--memory=4g",
                    "--cpuset-cpus=" + ",".join(map(str, sorted(os.sched_getaffinity(0)))),
                    "-v", f"{isolated}:/workspace:ro", "-w", "/workspace",
                    "-e", "GITHUB_WORKSPACE=/workspace",
                    "ghcr.io/kebag-logic/milan-ci-tools:recipe-712f7b38",
                    "bash", "-e", "/workspace/offline-step.sh"]
        rc = subprocess.run(argv, cwd=wt, env=e, stdout=out,
                            stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL).returncode
    (logs / f"{tag}.rc").write_text(f"{rc}\n")
    print(f"{tag}\trc={rc}", flush=True)
    failed += rc != 0
    if job == "docs-check-no-git" and sid == "ci_step_3":
        break
if job != "docs-check-no-git":
    status = run("git", "status", "--porcelain", cwd=wt)
    (logs / f"{job}__tree-after.txt").write_text(f"head {run('git', 'rev-parse', 'HEAD', cwd=wt)}\nstatus:\n{status}\n")
(logs / f"{job}__DONE").write_text(f"failed {failed}\n")
print(f"{job} done, failed {failed}", flush=True)
