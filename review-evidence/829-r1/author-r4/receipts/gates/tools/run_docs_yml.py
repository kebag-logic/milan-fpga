#!/usr/bin/env python3
"""Run one job of .github/workflows/docs.yml, step by step, on a fresh clean clone of a commit.

usage: run_docs_yml.py <head sha> <job> <scratch root>

The step list comes from the workflow in the clone, never from a list kept here.
Only NOT_RUN below may stand between a `run:` step and its rc file, each with its
reason; verify_docs_yml.py fails on any step with neither an rc of 0 nor an entry.
"""
import json, os, subprocess, sys
from pathlib import Path
import yaml

LANE = "$LANES/583-arty"
ORIGIN = "https://github.com/kebag-logic/milan-fpga.git"
VENV = "$VALIDATION_STORAGE/829-a725c/gates/venv/bin"
HOME = "$VALIDATION_STORAGE/829-a725c/gates/home"
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
run = lambda *a, cwd=None: subprocess.run(a, cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()
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

temp = work / "runner_temp"; temp.mkdir(exist_ok=True)
tmp = work / "tmp"; tmp.mkdir(exist_ok=True)
gh_env = work / "github_env"; gh_env.touch()
gh_out = work / "github_output"; gh_out.touch()
env = {k: v for k, v in os.environ.items() if k in ("LANG", "LC_ALL", "USER", "TERM")}
env.update(PATH=f"{VENV}:{TOOLS}", HOME=HOME, RUNNER_TEMP=str(temp), TMPDIR=str(tmp),
           GITHUB_WORKSPACE=str(wt), GITHUB_ENV=str(gh_env), GITHUB_OUTPUT=str(gh_out),
           GITHUB_SHA=head, CI="true", GIT_ALLOW_PROTOCOL="file:https",
           VERILATOR="$VALIDATION_TOOLS/pinned-verilator-5.050/verilator",
           TSN_GEN_ROOT="$MANAGEMENT/tools/tsn-gen-deca300c")
STEP_ENV = {"gate_8": dict(EVENT_NAME="pull_request", PR_BASE_REF="dev", PUSH_BEFORE_SHA="")}

wf = yaml.safe_load((wt / ".github/workflows/docs.yml").read_text())
steps = wf["jobs"][job]["steps"]
failed = 0
for n, step in enumerate(steps):
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
    e = dict(env); e.update(STEP_ENV.get(sid, {}))
    # as GitHub runs a `run:` step with no shell named
    script = work / f"{sid}.sh"
    script.write_text(step["run"])
    log = logs / f"{tag}.log"
    with open(log, "w") as out:
        out.write(f"# head {head} job {job} step {sid}: {step.get('name')}\n# clone {wt}\n")
        out.flush()
        rc = subprocess.run(["bash", "-e", str(script)], cwd=wt, env=e, stdout=out,
                            stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL).returncode
    (logs / f"{tag}.rc").write_text(f"{rc}\n")
    print(f"{tag}\trc={rc}", flush=True)
    failed += rc != 0
    if job == "docs-check-no-git" and sid == "ci_step_3":
        break
if job != "docs-check-no-git":
    status = run("git", "status", "--porcelain", cwd=wt)
    (logs / f"{job}__tree-after.txt").write_text(f"head {run('git','rev-parse','HEAD',cwd=wt)}\nstatus:\n{status}\n")
(logs / f"{job}__DONE").write_text(f"failed {failed}\n")
print(f"{job} done, failed {failed}", flush=True)
