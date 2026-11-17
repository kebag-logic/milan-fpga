#!/usr/bin/env python3
"""Replay one job of .github/workflows/docs.yml natively on a clean clone.

Every step with a `run:` body executes verbatim, in order, under
bash --noprofile --norc -eo pipefail (the GitHub default shell), with
GITHUB_ENV folded into the environment after each step.  Hosted-only
plumbing is not run and is listed in the summary with the reason:
evidence record/upload steps, apt package resolution, and the sudo
install of sv2v (replaced by the same pinned, sha256-checked archive
unpacked into a scratch bin directory on PATH).

usage: replay_docs.py <source-repo> <head-sha> <job> <workdir> <python-for-venv>
"""
import json, os, re, shutil, subprocess, sys, time
from pathlib import Path

import yaml

src, head, job, work, pybin = sys.argv[1:6]
work = Path(work)
if work.exists():
    shutil.rmtree(work)
work.mkdir(parents=True)
clone = work / "src"
home = work / "home"
temp = work / "runner_temp"
logs = work / "logs"
for d in (home, temp, logs):
    d.mkdir()

def sh(*a, **k):
    return subprocess.run(a, check=True, **k)

sh("git", "clone", "-q", "--no-local", src, str(clone))
sh("git", "-C", str(clone), "checkout", "-q", "--detach", head)
got = subprocess.run(["git", "-C", str(clone), "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
assert got == head, (got, head)
sh("git", "-C", str(clone), "remote", "set-url", "origin", "https://github.com/kebag-logic/milan-fpga.git")
status = subprocess.run(["git", "-C", str(clone), "status", "--porcelain"], capture_output=True, text=True, check=True).stdout
assert status == "", status

venv = work / "venv"
sh(pybin, "-m", "venv", str(venv))
bindir = work / "bin"
bindir.mkdir()

env = {
    "HOME": str(home),
    "PATH": f"{venv}/bin:{bindir}:{os.path.expanduser("~")}/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin",
    "LANG": "C.UTF-8",
    "CI": "true",
    "GITHUB_ACTIONS": "true",
    "GITHUB_WORKSPACE": str(clone),
    "GITHUB_SHA": head,
    "GITHUB_EVENT_NAME": "pull_request",
    "RUNNER_TEMP": str(temp),
    "RUNNER_OS": "Linux",
    "GIT_TERMINAL_PROMPT": "0",
}

wf = yaml.safe_load((clone / ".github/workflows/docs.yml").read_text())
jd = wf["jobs"][job]
EXPR = {
    "${{ github.workspace }}": str(clone),
    "${{ github.event_name }}": "pull_request",
    "${{ github.event.pull_request.base.ref }}": "dev",
    "${{ github.event.before }}": "",
}

def subst(v):
    v = str(v)
    for a, b in EXPR.items():
        v = v.replace(a, b)
    if "${{" in v:
        raise SystemExit(f"unhandled expression in {v!r}")
    return v

for k, v in (jd.get("env") or {}).items():
    env[k] = subst(v)

SV2V = """set -euo pipefail
ver=v0.0.12
sha256=ff8c9eea5bc029b372fb4953427625cddb7cf7e58c1240623ac9f260818d5a00
url="https://github.com/zachjs/sv2v/releases/download/${ver}/sv2v-Linux.zip"
mkdir -p "$RUNNER_TEMP/ci-sv2v-cache"
archive="$RUNNER_TEMP/ci-sv2v-cache/sv2v.zip"
if [ ! -f "$archive" ]; then curl -fsSL "$url" -o "$archive"; fi
echo "${sha256}  $archive" | sha256sum -c -
unzip -q -o "$archive" -d "$RUNNER_TEMP/sv2v"
install -m755 "$(find "$RUNNER_TEMP/sv2v" -name sv2v -type f | head -1)" "%s/sv2v"
sv2v --version
""" % bindir

rows = []
failed = False
for i, s in enumerate(jd["steps"]):
    sid, name = s.get("id", f"step{i}"), s.get("name", s.get("uses", ""))
    if "run" not in s:
        rows.append(dict(id=sid, name=name, action="not run", reason=f"hosted action {s.get('uses')}"))
        continue
    body = s["run"]
    if sid in ("ci_record",) or name.startswith("Record executed gate outcomes") or name.startswith("Retain checkout identity"):
        rows.append(dict(id=sid, name=name, action="not run", reason="hosted evidence plumbing"))
        continue
    if name.startswith("Resolve exact package downloads"):
        rows.append(dict(id=sid, name=name, action="not run", reason="apt package resolution; librsvg2-bin present on host"))
        continue
    if name == "Install diagram gate dependencies":
        body = "\n".join(l for l in body.splitlines() if "apt-get" not in l)
        note = "apt-get line dropped (librsvg2-bin present); pip line run"
    elif name == "Install the pinned sv2v release":
        body = SV2V
        note = "same pinned archive and sha256, installed into scratch bin instead of sudo /usr/local/bin"
    else:
        note = ""
    if failed:
        rows.append(dict(id=sid, name=name, action="skipped", reason="earlier step failed"))
        continue
    step_env = dict(env)
    for k, v in (s.get("env") or {}).items():
        step_env[k] = subst(v)
    genv = temp / "github_env"; genv.write_text("")
    gout = temp / "github_output"; gout.write_text("")
    step_env["GITHUB_ENV"] = str(genv)
    step_env["GITHUB_OUTPUT"] = str(gout)
    script = temp / f"step_{i:02d}.sh"
    script.write_text(subst(body) if "${{" in body else body)
    log = logs / f"{i:02d}_{sid}.log"
    t0 = time.time()
    with open(log, "w") as f:
        rc = subprocess.run(["bash", "--noprofile", "--norc", "-eo", "pipefail", str(script)],
                            cwd=clone, env=step_env, stdout=f, stderr=subprocess.STDOUT).returncode
    dt = round(time.time() - t0, 1)
    for line in genv.read_text().splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            env[k] = v
    rows.append(dict(id=sid, name=name, action="run", rc=rc, seconds=dt, note=note,
                     log=log.name, tail=log.read_text(errors="replace").splitlines()[-3:]))
    print(f"{job} {sid} rc={rc} {dt}s {name}", flush=True)
    if rc != 0:
        failed = True

summary = dict(job=job, head=head, rows=rows, result="failure" if failed else "success")
(work / "summary.json").write_text(json.dumps(summary, indent=1) + "\n")
print(f"{job} RESULT {summary['result']}")
sys.exit(1 if failed else 0)
