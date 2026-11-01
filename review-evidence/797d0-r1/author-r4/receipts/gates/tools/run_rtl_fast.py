#!/usr/bin/env python3
"""Run the steps of .github/workflows/rtl-fast.yml that read scripts/ or docs/ on a fresh clean clone of a commit.

usage: run_rtl_fast.py <head sha> <job> <scratch root> [step id ...]

The steps run are the workflow's own text. With no step ids a job runs whatever its
selection (select_rtl_fast.py) names. A job's budget and dependency steps run first,
each with its own log and rc, because the selected steps need them.
"""
import json, os, subprocess, sys
from pathlib import Path
import yaml

LANE = "$LANES/797-d0-audit"
ORIGIN = "https://github.com/kebag-logic/milan-fpga.git"
SCRATCH = "$VALIDATION_STORAGE/797-a706d/gates"
VENV = f"{SCRATCH}/venv/bin"
HOME = f"{SCRATCH}/home"
PINNED = "$VALIDATION_TOOLS/pinned-verilator-5.050"
TOOLS = f"{PINNED}:$VALIDATION_TOOLS/sv2v-v0.0.12:$VALIDATION_STORAGE/scratch/a662/make43/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin"
HERE = Path(__file__).parent

head, job, root = sys.argv[1:4]
root = Path(root)
logs = root / "logs"
logs.mkdir(parents=True, exist_ok=True)
work = root / job
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
run("git", "fetch", "-q", LANE, "+refs/remotes/origin/dev:refs/remotes/origin/dev", cwd=wt)
for line in run("git", "config", "--blob", f"{head}:.gitmodules", "--get-regexp", r"^submodule\..*\.path$", cwd=wt).splitlines():
    dep = line.split()[1]
    if (Path(LANE) / dep / ".git").exists():
        run("git", "config", f"submodule.{dep}.url", f"{LANE}/{dep}", cwd=wt)

temp = work / "runner_temp"; temp.mkdir(exist_ok=True)
tmp = work / "tmp"; tmp.mkdir(exist_ok=True)
gh_env = work / "github_env"; gh_env.touch()
gh_out = work / "github_output"; gh_out.touch()
gh_path = work / "github_path"; gh_path.touch()
wf = yaml.safe_load((wt / ".github/workflows/rtl-fast.yml").read_text())
body = wf["jobs"][job]
env = {k: v for k, v in os.environ.items() if k in ("LANG", "LC_ALL", "USER", "TERM")}
env.update(wf.get("env") or {})
# LITEX_BIN names the interpreter a job's LiteX builders need; a job without it keeps the scratch venv.
env.update(PATH=f"{os.environ['LITEX_BIN']}:{VENV}:{TOOLS}" if os.environ.get("LITEX_BIN") else f"{VENV}:{TOOLS}", HOME=HOME, RUNNER_TEMP=str(temp), TMPDIR=str(tmp), GITHUB_WORKSPACE=str(wt),
           GITHUB_ENV=str(gh_env), GITHUB_OUTPUT=str(gh_out), GITHUB_PATH=str(gh_path), GITHUB_SHA=head, CI="true",
           GIT_ALLOW_PROTOCOL="file:https", VERILATOR=f"{PINNED}/verilator",
           TSN_GEN_ROOT="$MANAGEMENT/tools/tsn-gen-deca300c")
for key, value in (body.get("env") or {}).items():
    env[key] = str(value).replace("${{ github.workspace }}", str(wt))
# The hosted pull_request event's replay form: the base is the live dev fetched above.
STEP_ENV = {"scope": dict(EVENT_NAME="pull_request", ACT="true", PR_BASE_REF="dev", PR_HEAD_SHA=head, PUSH_BEFORE_SHA="")}
chosen = sys.argv[4:] or json.loads((HERE / "rtl_fast_selection.json").read_text())[job]
failed = 0
for n, step in enumerate(body["steps"]):
    if "run" not in step:
        continue
    sid = step.get("id") or f"step{n}"
    needed = step.get("name", "").startswith(("Set CPU-derived", "Fetch ")) or sid in chosen
    if not needed:
        continue
    for line in gh_env.read_text().splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            env[k] = v
    # This host has the pinned Verilator at another path; the step text is otherwise as the workflow writes it.
    script = work / f"{sid}.sh"
    script.write_text(step["run"].replace("/opt/verilator/bin", PINNED))
    tag = f"{job}__{sid}"
    log = logs / f"{tag}.log"
    e = dict(env); e.update(STEP_ENV.get(sid, {}))
    with open(log, "w") as out:
        out.write(f"# head {head} job {job} step {sid}: {step.get('name')}\n")
        out.flush()
        rc = subprocess.run(["bash", "-e", str(script)], cwd=wt, env=e, stdout=out, stderr=subprocess.STDOUT,
                            stdin=subprocess.DEVNULL).returncode
    (logs / f"{tag}.rc").write_text(f"{rc}\n")
    print(f"{tag}\trc={rc}", flush=True)
    failed += rc != 0
(logs / f"{job}__tree-after.txt").write_text(f"head {run('git', 'rev-parse', 'HEAD', cwd=wt)}\nstatus:\n{run('git', 'status', '--porcelain', cwd=wt)}\n")
(logs / f"{job}__DONE").write_text(f"failed {failed}\n")
print(f"{job} done, failed {failed}", flush=True)
