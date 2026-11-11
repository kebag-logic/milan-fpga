#!/usr/bin/env python3
"""Run one job of a workflow, step by step, on a fresh clean clone of a commit (from run_docs_yml.py, generalised).

usage: run_wf.py <workflow file name> <head sha> <job> <scratch root> [matrix key=value ...]

The step list comes from the workflow in the clone, never from a list kept here. Only not_run.json beside this file
may stand between a `run:` step and its rc file, each with its reason (keys: "<workflow>/<job>/<step>",
"<workflow>/<step>" or "<step>"); verify_wf.py fails on any step with neither an rc of 0 nor a reason. A step's
`${{ matrix.* }}` and `${{ github.workspace }}` are the values given here; GITHUB_ENV and GITHUB_PATH are honoured
between steps, as a runner honours them.
"""
import json, os, re, subprocess, sys
from pathlib import Path
import yaml

LANE = "<lane>"
ORIGIN = "https://github.com/kebag-logic/milan-fpga.git"
VENV = "<scratch>/gates/venv/bin"
HOME = "<scratch>/gates/home"
TOOLS = ("<rv32-sdk>/host/bin:<tools>/pinned-verilator-5.050:<tools>/sv2v-v0.0.12:"
         "<tools-scratch>/a662/make43/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin")
NOT_RUN = json.loads(Path(__file__).with_name("not_run.json").read_text())

workflow, head, job, root = sys.argv[1:5]
matrix = dict(a.split("=", 1) for a in sys.argv[5:])
mtag = "".join(f"-{v}" for _, v in sorted(matrix.items()))
root = Path(root)
work = root / f"{workflow.removesuffix('.yml')}__{job}{mtag}"
logs = root / "logs"
logs.mkdir(parents=True, exist_ok=True)
Path(HOME).mkdir(parents=True, exist_ok=True)
wt = work / "wt"
assert not wt.exists(), f"{wt} exists: a job runs on a fresh clone"
wt.parent.mkdir(parents=True, exist_ok=True)
run = lambda *a, cwd=None: subprocess.run(a, cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()
run("git", "clone", "-q", "--shared", "--no-checkout", LANE, str(wt))
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
gh_env = work / "github_env"; gh_env.touch()
gh_out = work / "github_output"; gh_out.touch()
gh_path = work / "github_path"; gh_path.touch()
env = {k: v for k, v in os.environ.items() if k in ("LANG", "LC_ALL", "USER", "TERM")}
VENV = os.environ.get("WF_VENV", VENV)
env.update(PATH=f"{VENV}:{TOOLS}", HOME=HOME, RUNNER_TEMP=str(temp), TMPDIR=str(tmp),
           GITHUB_WORKSPACE=str(wt), GITHUB_ENV=str(gh_env), GITHUB_OUTPUT=str(gh_out), GITHUB_PATH=str(gh_path),
           GITHUB_SHA=head, GITHUB_EVENT_NAME="pull_request", GITHUB_BASE_REF="dev-soft-core", CI="true",
           GITHUB_REF="refs/heads/tsn-c-stack-pin-715589c", GITHUB_HEAD_REF="tsn-c-stack-pin-715589c",
           GITHUB_REPOSITORY="kebag-logic/milan-fpga",
           GIT_ALLOW_PROTOCOL="file:https", VERILATOR="<tools>/pinned-verilator-5.050/verilator",
           TSN_GEN_ROOT="<mgmt>/tools/tsn-gen-deca300c",
           LITEX_ENV_CC_TRIPLE="riscv32-buildroot-linux-gnu", PYTHONHASHSEED="0", COURSIER_MODE="offline",
           SBT_OPTS="-Dsbt.offline=true")


#: The event a pull request to dev-soft-core makes, ready for review (the exhaustive gates' case), as the hosted
#: runner fills its expressions; an expression not here stays, and its step is in not_run.json.
EVENT = {"github.workspace": str(wt), "github.event_name": "pull_request",
         "github.event.pull_request.base.ref": "dev-soft-core", "github.event.pull_request.head.sha": head,
         "github.event.before": "", "github.event.pull_request.draft": "false",
         "needs.full-ci-gate.outputs.target_sha": head, "steps.scope.outputs.rtl": "true"}
#: Paths the hosted runner installs its pinned tools at, and where the same pinned tool is on this host; each
#: rewrite is named at the top of the step's log.
PATH_MAP = (("/opt/verilator/bin", "<tools>/pinned-verilator-5.050"),)


def expand(text: str) -> str:
    """A step's matrix, workspace and event expressions, as the runner fills them."""
    text = re.sub(r"\$\{\{\s*matrix\.(\w+)\s*\}\}", lambda m: matrix[m[1]], text)
    return re.sub(r"\$\{\{\s*([\w.-]+)\s*\}\}", lambda m: EVENT.get(m[1], m[0]), text)


wf = yaml.safe_load((wt / ".github/workflows" / workflow).read_text())
body = wf["jobs"][job]
#: Job env a hosted runner applies and this host cannot, each with its reason, named at the top of every step's log.
ENV_NOT_APPLIED = {"PIP_CONSTRAINT": "its pins are CPython 3.12 x86_64 wheel downloads; this host runs CPython 3.14, "
                                     "the venv carrying the same releases"}
for k, v in {**(wf.get("env") or {}), **(body.get("env") or {})}.items():
    if k not in ENV_NOT_APPLIED:
        env[k] = expand(str(v))
failed = 0
for n, step in enumerate(body["steps"]):
    if "run" not in step:
        continue
    sid = step.get("id") or f"step{n}"
    tag = f"{workflow.removesuffix('.yml')}__{job}{mtag}__{sid}"
    if any(k in NOT_RUN for k in (f"{workflow}/{job}/{sid}", f"{workflow}/{sid}", sid)):
        continue
    for line in gh_env.read_text().splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            env[k] = v
    extra = [p for p in gh_path.read_text().splitlines() if p]
    e = dict(env)
    if extra:
        e["PATH"] = ":".join(extra[::-1]) + ":" + env["PATH"]
    for k, v in (step.get("env") or {}).items():
        e[k] = expand(str(v))
    script = work / f"{sid}.sh"
    text = expand(step["run"])
    mapped = [(a, b) for a, b in PATH_MAP if a in text]
    for a, b in mapped:
        text = text.replace(a, b)
    script.write_text(text)
    log = logs / f"{tag}.log"
    with open(log, "w") as out:
        out.write(f"# head {head} workflow {workflow} job {job}{mtag} step {sid}: {step.get('name')}\n# clone {wt}\n"
                  f"# venv {VENV}\n" + "".join(f"# path rewritten: {a} -> {b}\n" for a, b in mapped) +
                  "".join(f"# env not applied: {k}: {why}\n" for k, why in ENV_NOT_APPLIED.items()
                          if k in {**(wf.get("env") or {}), **(body.get("env") or {})}))
        out.flush()
        rc = subprocess.run(["bash", "-e", str(script)], cwd=wt / step.get("working-directory", "."), env=e,
                            stdout=out, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL).returncode
    (logs / f"{tag}.rc").write_text(f"{rc}\n")
    print(f"{tag}\trc={rc}", flush=True)
    failed += rc != 0
status = run("git", "status", "--porcelain", cwd=wt)
(logs / f"{workflow.removesuffix('.yml')}__{job}{mtag}__tree-after.txt").write_text(
    f"head {run('git', 'rev-parse', 'HEAD', cwd=wt)}\nstatus:\n{status}\n")
(logs / f"{workflow.removesuffix('.yml')}__{job}{mtag}__DONE").write_text(f"failed {failed}\n")
print(f"{workflow} {job}{mtag} done, failed {failed}", flush=True)
