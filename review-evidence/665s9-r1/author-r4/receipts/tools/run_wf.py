#!/usr/bin/env python3
"""Run one job of one workflow, step by step, on a fresh clean clone of a commit (adapted from the docs.yml runner).

usage: run_wf.py <head sha> <workflow file name> <job> <scratch root>

The step list comes from the workflow in the clone, never from a list kept here.
Only not_run.json may stand between a `run:` step and its rc file, each with its reason;
verify_wf.py fails on any step with neither an rc of 0 nor an entry.
"""
import json, os, subprocess, sys
from pathlib import Path
import yaml

LANE = "<lane>"
ORIGIN = "https://github.com/kebag-logic/milan-fpga.git"
S = Path("<scratch>")
VENV = str(S / "venv/bin")
HOME = str(S / "home")
TOOLS = ("<tools>/pinned-verilator-5.050:<tools>/sv2v-v0.0.12:"
         "<data>/scratch/a662/make43/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin")
NOT_RUN = json.loads(Path(__file__).with_name("not_run.json").read_text())

head, wfname, job, root = sys.argv[1:5]
root = Path(root)
work = root / f"{wfname}__{job}"
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
gm = run("git", "config", "--blob", f"{head}:.gitmodules", "--get-regexp", r"^submodule\..*\.path$", cwd=wt)
for line in gm.splitlines():
    dep = line.split()[1]
    if (Path(LANE) / dep / ".git").exists():
        run("git", "config", f"submodule.{dep}.url", f"{LANE}/{dep}", cwd=wt)

temp = work / "runner_temp"; temp.mkdir(exist_ok=True)
tmp = work / "tmp"; tmp.mkdir(exist_ok=True)
Path(HOME).mkdir(parents=True, exist_ok=True)
gh_env = work / "github_env"; gh_env.touch()
gh_out = work / "github_output"; gh_out.touch()
gh_path = work / "github_path"; gh_path.touch()
env = {k: v for k, v in os.environ.items() if k in ("LANG", "LC_ALL", "USER", "TERM")}
extra = json.loads(os.environ.get("RUN_WF_ENV", "{}"))
env.update(PATH=f"{VENV}:{TOOLS}", HOME=HOME, RUNNER_TEMP=str(temp), TMPDIR=str(tmp),
           GITHUB_WORKSPACE=str(wt), GITHUB_ENV=str(gh_env), GITHUB_OUTPUT=str(gh_out), GITHUB_PATH=str(gh_path),
           GITHUB_SHA=head, GITHUB_EVENT_NAME="pull_request", GITHUB_BASE_REF="dev-soft-core", CI="true",
           GIT_ALLOW_PROTOCOL="file:https", PYTHONHASHSEED="0",
           VERILATOR="<tools>/pinned-verilator-5.050/verilator",
           TSN_GEN_ROOT="<home>/milan-fpga-management/tools/tsn-gen-deca300c")
env.update(extra)
STEP_ENV = json.loads(os.environ.get("RUN_WF_STEP_ENV", "{}"))

wf = yaml.safe_load((wt / ".github/workflows" / wfname).read_text())
steps = wf["jobs"][job]["steps"]
failed = 0
for n, step in enumerate(steps):
    if "run" not in step:
        continue
    sid = step.get("id") or f"step{n}"
    tag = f"{wfname}__{job}__{sid}"
    if f"{wfname}/{job}/{sid}" in NOT_RUN or f"{wfname}/{sid}" in NOT_RUN or f"*/{job}/{sid}" in NOT_RUN or f"*/*/{sid}" in NOT_RUN:
        continue
    for line in gh_env.read_text().splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            env[k] = v
    extra_path = [p for p in gh_path.read_text().splitlines() if p.strip()]
    e = dict(env); e.update(STEP_ENV.get(f"{job}/{sid}", {}))
    if extra_path:
        e["PATH"] = ":".join(reversed(extra_path)) + ":" + e["PATH"]
    for k, v in (step.get("env") or {}).items():
        if isinstance(v, str) and "${{" not in v:
            e[k] = v
    script = work / f"{sid}.sh"
    script.write_text(step["run"])
    log = logs / f"{tag}.log"
    with open(log, "w") as out:
        out.write(f"# head {head} workflow {wfname} job {job} step {sid}: {step.get('name')}\n")
        out.flush()
        rc = subprocess.run(["bash", "-e", str(script)], cwd=wt, env=e, stdout=out,
                            stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL).returncode
    (logs / f"{tag}.rc").write_text(f"{rc}\n")
    print(f"{tag}\trc={rc}", flush=True)
    failed += rc != 0
status = run("git", "status", "--porcelain", cwd=wt)
(logs / f"{wfname}__{job}__tree-after.txt").write_text(f"head {run('git','rev-parse','HEAD',cwd=wt)}\nstatus:\n{status}\n")
(logs / f"{wfname}__{job}__DONE").write_text(f"failed {failed}\n")
print(f"{wfname} {job} done, failed {failed}", flush=True)
