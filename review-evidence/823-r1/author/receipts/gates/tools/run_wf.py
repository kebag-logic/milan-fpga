#!/usr/bin/env python3
"""Run one job of a workflow, step by step, on a fresh clean clone of a commit (a pull_request to dev-soft-core).

usage: run_wf.py <workflow> <head sha> <job> <scratch root> [--matrix k/n] [step id ...]

Adapted from the docs runner of the 829 lane (receipts/gates/tools there): the step list comes from the workflow in
the clone, never from a list kept here; a GitHub expression in a step's env is given its pull_request value; only
not_run.json may stand between a `run:` step and its rc file, each entry with its reason, and verify_wf.py fails on
any step with neither an rc of 0 nor an entry. With step ids, only those steps run, in the clone the first call made.
"""
import json, os, re, subprocess, sys
from pathlib import Path
import yaml

LANE = "$LANES/823-name-cap"
ORIGIN = "https://github.com/kebag-logic/milan-fpga.git"
SCR = Path("$VALIDATION_STORAGE/823-a753c/gates")
VENV = str(SCR / "venv/bin")
HOME = str(SCR / "home")
TOOLS = ("$VALIDATION_TOOLS/pinned-verilator-5.050:$VALIDATION_TOOLS/sv2v-v0.0.12:"
         "$VALIDATION_STORAGE/scratch/a662/make43/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin")
LITEX = "$HOME/litex-milan/venv/bin"
NOT_RUN = json.loads(Path(__file__).with_name("not_run.json").read_text())
#: jobs whose steps need the LiteX interpreter first on PATH (the hosted job pip-installs it)
LITEX_JOBS = {"rtl-fast/firmware-boundary", "elaborate/elaborate-gates-0", "elaborate/elaborate-gates-1",
              "rtl-fast/publication-census"}

args = sys.argv[1:]
matrix = None
if "--matrix" in args:
    i = args.index("--matrix"); matrix = args[i + 1].split("/"); del args[i:i + 2]
wfname, head, job, root = args[:4]
only = set(args[4:])
root = Path(root)
tag_job = f"{wfname}.{job}" + (f".{matrix[0]}of{matrix[1]}" if matrix else "")
work = root / tag_job
logs = root / "logs"
logs.mkdir(parents=True, exist_ok=True)
wt = work / "wt"
fresh = not wt.exists()
assert fresh or only, f"{wt} exists: a job runs on a fresh clone"
wt.parent.mkdir(parents=True, exist_ok=True)
run = lambda *a, cwd=None: subprocess.run(a, cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()
if fresh:
    run("git", "clone", "-q", "--shared", "--no-checkout", LANE, str(wt))
    run("git", "fetch", "-q", LANE, head, cwd=wt)
    run("git", "-c", "advice.detachedHead=false", "checkout", "-q", "--detach", head, cwd=wt)
    assert run("git", "rev-parse", "HEAD", cwd=wt) == head
    assert run("git", "status", "--porcelain", cwd=wt) == ""
    run("git", "remote", "set-url", "origin", ORIGIN, cwd=wt)
    # the base the PR targets, as the hosted checkout carries it for scope and diff gates
    run("git", "fetch", "-q", LANE, "refs/remotes/origin/dev-soft-core:refs/remotes/origin/dev-soft-core", cwd=wt)
gm = run("git", "config", "--blob", f"{head}:.gitmodules", "--get-regexp", r"^submodule\..*\.path$", cwd=wt)
for line in gm.splitlines():
    dep = line.split()[1]
    if (Path(LANE) / dep / ".git").exists():
        run("git", "config", f"submodule.{dep}.url", f"{LANE}/{dep}", cwd=wt)

temp = work / "runner_temp"; temp.mkdir(exist_ok=True)
tmp = work / "tmp"; tmp.mkdir(exist_ok=True)
gh_env = work / "github_env"; gh_env.touch()
gh_out = work / "github_output"; gh_out.touch()
gh_path = work / "github_path"; gh_path.touch()
env = {k: v for k, v in os.environ.items() if k in ("LANG", "LC_ALL", "USER", "TERM")}
path = f"{VENV}:{TOOLS}"
if f"{wfname}/{job}" in LITEX_JOBS:
    path = f"{LITEX}:{path}"
env.update(PATH=path, HOME=HOME, RUNNER_TEMP=str(temp), TMPDIR=str(tmp),
           GITHUB_WORKSPACE=str(wt), GITHUB_ENV=str(gh_env), GITHUB_OUTPUT=str(gh_out), GITHUB_PATH=str(gh_path),
           GITHUB_SHA=head, GITHUB_EVENT_NAME="pull_request", GITHUB_BASE_REF="dev-soft-core", CI="true",
           GIT_ALLOW_PROTOCOL="file:https", VERILATOR="$VALIDATION_TOOLS/pinned-verilator-5.050/verilator",
           TSN_GEN_ROOT="$HOME/milan-fpga-management/tools/tsn-gen-deca300c",
           GIT_CONFIG_COUNT="1", GIT_CONFIG_KEY_0="protocol.file.allow", GIT_CONFIG_VALUE_0="always",
           # The checkout is the head, not GitHub's merge commit, so the scope selectors take their replay path
           # (the live base and `git merge-tree`); no PR exists, so the ref the target step prints is the branch.
           ACT="true", GITHUB_REF="refs/heads/823-nvm-format")
# PIP_CONSTRAINT is not set: ci/constraints-ci.txt pins CPython 3.12 wheels by URL, and this host runs another CPython
CONTEXT = {"github.event_name": "pull_request", "github.event.pull_request.base.ref": "dev-soft-core",
           "github.event.pull_request.head.sha": head, "github.event.before": "",
           "github.event.pull_request.draft": "false", "github.workspace": str(wt), "github.sha": head,
           "needs.full-ci-gate.outputs.target_sha": head}
#: The hosted Verilator is built into /opt; this host's pinned build of the same version stands in its place.
SUBST = {"/opt/verilator/bin": "$VALIDATION_TOOLS/pinned-verilator-5.050"}
if matrix:
    CONTEXT.update({"matrix.shard": matrix[0], "matrix.total": matrix[1]})


def value(text):
    """A step env value with each known expression given its pull_request value; None when one is unknown."""
    out, unknown = text, False
    for m in re.findall(r"\$\{\{\s*([^}]*?)\s*\}\}", text):
        if m in CONTEXT:
            out = out.replace("${{ " + m + " }}", CONTEXT[m]).replace("${{" + m + "}}", CONTEXT[m])
        else:
            unknown = True
    return None if unknown else out


wf = yaml.safe_load((wt / f".github/workflows/{wfname}.yml").read_text())
for k, v in (wf.get("env") or {}).items():
    if value(str(v)) is not None:
        env[k] = value(str(v))
body = wf["jobs"][job]
for k, v in (body.get("env") or {}).items():
    if k != "PIP_CONSTRAINT" and value(str(v)) is not None:
        env[k] = value(str(v))
failed = 0
for n, step in enumerate(body["steps"]):
    if "run" not in step:
        continue
    sid = step.get("id") or f"step{n}"
    tag = f"{tag_job}__{sid}"
    if any(key in NOT_RUN for key in (f"{wfname}/{job}/{sid}", f"{wfname}/{sid}", f"{wfname}/{job}/*")):
        continue
    if only and sid not in only:
        continue
    for line in gh_env.read_text().splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            env[k] = v
    e = dict(env)
    # as the runner does: every line a step wrote to GITHUB_PATH leads PATH for the steps after it
    added = [ln for ln in reversed(gh_path.read_text().splitlines()) if ln.strip()]
    if added:
        e["PATH"] = ":".join(added + [env["PATH"]])
    for k, v in (step.get("env") or {}).items():
        if value(str(v)) is not None:
            e[k] = value(str(v))
    script = work / f"{sid}.sh"
    text = step["run"]
    for k, v in CONTEXT.items():
        text = text.replace("${{ " + k + " }}", v)
    subst = [f"{a} -> {b}" for a, b in SUBST.items() if a in text]
    for a, b in SUBST.items():
        text = text.replace(a, b)
    script.write_text(text)
    log = logs / f"{tag}.log"
    with open(log, "w") as out:
        out.write(f"# head {head} workflow {wfname} job {job} step {sid}: {step.get('name')}\n")
        if subst:
            out.write(f"# substituted: {'; '.join(subst)}\n")
        out.flush()
        rc = subprocess.run(["bash", "-e", str(script)], cwd=wt / step.get("working-directory", "."), env=e, stdout=out,
                            stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL).returncode
    (logs / f"{tag}.rc").write_text(f"{rc}\n")
    print(f"{tag}\trc={rc}", flush=True)
    failed += rc != 0
if (wt / ".git").exists():
    status = run("git", "status", "--porcelain", cwd=wt)
    (logs / f"{tag_job}__tree-after.txt").write_text(f"head {run('git','rev-parse','HEAD',cwd=wt)}\nstatus:\n{status}\n")
else:
    (logs / f"{tag_job}__tree-after.txt").write_text("no .git: the job strips the checkout's git metadata by design\n")
(logs / f"{tag_job}__DONE").write_text(f"failed {failed}\n")
print(f"{tag_job} done, failed {failed}", flush=True)
