#!/usr/bin/env python3
"""[R632] round-3 independent scope probe.

Runs the three shipping scope-step bodies (taken verbatim from a reviewed
tree's workflows, with only the recursive `ci_scope.py --selftest` call
replaced by `:`) against real and synthetic histories in a disposable shared
clone, in hosted mode (synthetic merge, live base first parent) and replay
mode (ACT=true, head checkout, refs/remotes/origin/dev = live). Prints one
JSON line per case/workflow/mode.

Usage: probe_r632_3.py <source-clone> <shipping-tree> <scratch-dir> <cases.json>
cases.json: [{"label":..,"live":..,"head":..,"merge":<optional real merge>}]
"""
import json, os, pathlib, subprocess, sys, tempfile, textwrap

src, shipping, scratch, cases_file = map(pathlib.Path, sys.argv[1:5])
STEPS = (("rtl.yml", "full-ci-gate", "gate"), ("rtl-fast.yml", "changes", "scope"),
         ("elaborate.yml", "elaborate", "scope"))
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
ENV.update(HOME=str(scratch / "home"), GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull,
           GIT_AUTHOR_NAME="probe", GIT_AUTHOR_EMAIL="probe@example.invalid",
           GIT_COMMITTER_NAME="probe", GIT_COMMITTER_EMAIL="probe@example.invalid",
           GIT_AUTHOR_DATE="2001-01-01T00:00:00+0000", GIT_COMMITTER_DATE="2001-01-01T00:00:00+0000")
(scratch / "home").mkdir(parents=True, exist_ok=True)
repo = scratch / "clone"

def git(*a, cwd=None, check=True):
    r = subprocess.run(["git", "-C", str(cwd or repo), *a], env=ENV, text=True, capture_output=True)
    if check and r.returncode:
        raise RuntimeError(f"git {a}: {r.stderr}")
    return r.stdout.strip()

def body(workflow, job, step):
    text = (shipping / ".github/workflows" / workflow).read_text()
    tail = text.partition(f"  {job}:\n")[2].partition(f"        id: {step}\n")[2].partition("        run: |\n")[2]
    out = []
    for line in tail.splitlines():
        if line.strip() and not line.startswith("          "):
            break
        out.append(line)
    s = textwrap.dedent("\n".join(out))
    assert s.count("python3 scripts/ci_scope.py --selftest") == 1
    return s.replace("python3 scripts/ci_scope.py --selftest", ":")

def run(script, checkout, extra):
    git("checkout", "--quiet", "--force", "--detach", checkout)
    with tempfile.TemporaryDirectory(dir=scratch) as t:
        env = dict(ENV, EVENT_NAME="pull_request", PR_DRAFT="false", PR_BASE_REF="dev",
                   GITHUB_OUTPUT=f"{t}/out", RUNNER_TEMP=t, ACT="false")
        env.update(extra)
        r = subprocess.run(["bash", "-euo", "pipefail", "-c", script], cwd=repo, env=env,
                           text=True, capture_output=True)
        if r.returncode:
            return {"rc": r.returncode, "stderr": r.stderr.strip()[-300:]}
        changed = next(pathlib.Path(t).glob("changed*")).read_text().splitlines()
        out = dict(l.split("=", 1) for l in pathlib.Path(f"{t}/out").read_text().splitlines())
        return {"rc": 0, "n": len(changed), "rtl": out["rtl"],
                "paths": changed if len(changed) <= 12 else changed[:12] + ["..."]}

if not repo.exists():
    subprocess.run(["git", "clone", "--quiet", "--shared", "--no-checkout", str(src), str(repo)],
                   env=ENV, check=True)
for case in json.loads(cases_file.read_text()):
    live, head = git("rev-parse", case["live"]), git("rev-parse", case["head"])
    merge = case.get("merge")
    if not merge:
        r = subprocess.run(["git", "-C", str(repo), "merge-tree", "--write-tree", live, head],
                           env=ENV, text=True, capture_output=True)
        merge = None if r.returncode else git("commit-tree", r.stdout.split()[0], "-p", live, "-p", head,
                                             "-m", "probe merge")
    git("update-ref", "refs/remotes/origin/dev", live)
    for wf, job, step in STEPS:
        s = body(wf, job, step)
        hosted = run(s, merge, {"GITHUB_SHA": merge, "PR_HEAD_SHA": head}) if merge else {"rc": "conflict"}
        replay = run(s, head, {"ACT": "true", "PR_HEAD_SHA": head, "GITHUB_SHA": head})
        same = hosted.get("paths") == replay.get("paths") and hosted.get("rtl") == replay.get("rtl")
        print(json.dumps({"case": case["label"], "workflow": wf, "live": live[:12], "head": head[:12],
                          "merge": (merge or "")[:12], "hosted": hosted, "replay": replay,
                          "hosted_eq_replay": same}), flush=True)
