#!/usr/bin/env python3
"""Run every `run:` step of the head's .github/workflows/docs.yml as its jobs
run it, on a clean clone, one `bash -e` script per step, output to a file, never
piped. Steps the host cannot run as written (GitHub-only recording and apt or
sudo installs the scratch environment already provides) are listed with the
reason instead. Usage: run_docs_workflow.py <clone> <export> <logs> <job> [ids...]"""
import json, os, re, subprocess, sys, time
from pathlib import Path
import yaml
wt, export, logs, job = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4]
only = set(sys.argv[5:])
scratch = Path(os.environ["GATE_SCRATCH"])
NOT_RUN = (
    (r"Resolve exact package downloads|Install diagram gate dependencies", "apt install: the host has the tools"),
    (r"Install the pinned sv2v release", "sudo install: the host has sv2v"),
    (r"Record executed gate outcomes|Record actual job execution|Retain checkout identity", "GitHub run evidence only"),
)
flow = yaml.safe_load((wt / ".github/workflows/docs.yml").read_text())
spec = flow["jobs"][job]
logs.mkdir(parents=True, exist_ok=True)
runner_temp = scratch / "runner_temp" / job
(runner_temp / "gate-results").mkdir(parents=True, exist_ok=True)
tmpdir = scratch / "tmpdir"
tmpdir.mkdir(exist_ok=True)
env = dict(os.environ, RUNNER_TEMP=str(runner_temp), TMPDIR=str(tmpdir), GITHUB_WORKSPACE=str(wt), GITHUB_ACTIONS="",
           HOME=os.environ["GATE_HOME"], PATH=os.environ["GATE_VENV"] + "/bin:" + os.environ["PATH"],
           MAKEFLAGS="-j1 --no-print-directory", GITHUB_ENV=str(runner_temp / "github_env"), CI="true")
env.pop("GITHUB_ACTIONS")
env["GITHUB_STEP_SUMMARY"] = str(runner_temp / "summary")
SUBST = {"${{ github.workspace }}": str(wt), "${{ github.event_name }}": "pull_request",
         "${{ github.event.pull_request.base.ref }}": "dev", "${{ github.event.before }}": ""}
def without_pip(text):
    """The workflow's pip lines install into the hosted CPython 3.12 under its
    constraints file. The scratch venv already holds those tools."""
    out, skipping = [], False
    for line in text.splitlines():
        if skipping or re.match(r"\s*python3 -m pip install\b", line):
            skipping = line.rstrip().endswith("\\")
            continue
        out.append(line)
    return "\n".join(out) + "\n"
def expand(v):
    v = str(v)
    for a, b in SUBST.items():
        v = v.replace(a, b)
    return v
for k, v in (spec.get("env") or {}).items():
    if k != "PIP_CONSTRAINT":
        env[k] = expand(v)
cwd = export if job == "docs-check-no-git" else wt
rows = []
for i, st in enumerate(spec["steps"]):
    if "run" not in st:
        continue
    ident, name = st.get("id", f"step{i}"), st.get("name", "")
    if only and ident not in only:
        continue
    reason = next((r for pat, r in NOT_RUN if re.search(pat, name)), None)
    if reason:
        rows.append((job, ident, name, "not run", reason, 0))
        continue
    stem = f"{job}__{ident}"
    script = runner_temp / f"{ident}.sh"
    body = without_pip(expand(st["run"]))
    if not body.strip():
        rows.append((job, ident, name, "not run", "pip install only: the scratch venv holds these tools", 0))
        continue
    script.write_text(body)
    step_env = dict(env)
    for k, v in (st.get("env") or {}).items():
        step_env[k] = expand(v)
    t0 = time.time()
    with open(logs / f"{stem}.log", "w") as log:
        rc = subprocess.run(["bash", "-e", str(script)], stdout=log, stderr=subprocess.STDOUT, env=step_env,
                            cwd=cwd, timeout=7000).returncode
    (logs / f"{stem}.rc").write_text(f"{rc}\n")
    rows.append((job, ident, name, rc, "", round(time.time() - t0)))
    print(f"{stem}\trc={rc}\t{round(time.time()-t0)}s\t{name}", flush=True)
with open(logs / f"{job}.summary.json", "a") as f:
    for r in rows:
        f.write(json.dumps(r) + "\n")
print(f"JOB_DONE {job}", flush=True)
