#!/usr/bin/env python3
"""Replay one job of a workflow, step by step, on a fresh clean clone of a commit.

usage: run_job.py <workflow file> <job> <head sha> <root> [--matrix k=v ...] [--gate-env] [--steps SID,...]

The step list comes from the workflow in the clone, never from a list kept here. Every `run:` step
either runs, its log and rc written under <root>/logs, or matches a rule of not_run.json (beside
this file), whose reason verify_jobs.py prints beside it; verify_jobs.py fails on any step with
neither an rc of 0 nor a reason.

The job gets its own clean clone (submodules at the commit's gitlinks, objects from the lane's own
clones, origin set to the public repository) and its own new Python 3.12 virtual environment, as a
fresh hosted runner does. All jobs share one CI HOME under the scratch root, as the hosted runs share
their caches, so the pinned RV32 SDK is installed once by its own installer and verified by each job.
With --gate-env the job uses the host's LiteX virtual environment and its sbt caches in place of a
job-private LiteX, for the elaboration jobs whose setup needs sudo; HOME stays the CI HOME.

Each run of the runner image's /opt tools is read as the host's pinned one (SUBST below), and each
`${{ }}` expression as the pull_request event to dev-soft-core it stands for (EXPR below). The job's
and each step's env are applied; GITHUB_ENV and GITHUB_PATH are honoured between steps. A failed step
is recorded and the job goes on, so one run shows every failure.
"""
import argparse
import json
import os
import re
import subprocess
from pathlib import Path

import yaml

LANE = "$LANES/665-s6-placement"
ORIGIN = "https://github.com/kebag-logic/milan-fpga.git"
PY312 = "$VALIDATION_TOOLS/uvpy/cpython-3.12.3-linux-x86_64-gnu/bin/python3.12"
TOOLS = ("$VALIDATION_TOOLS/verilator-v5.050/bin:$VALIDATION_TOOLS/sv2v-v0.0.12:"
         "$VALIDATION_STORAGE/scratch/a662/make43/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin")
GATE_LITEX = "$HOME/litex-milan/venv/bin:$VALIDATION_STORAGE/scratch/665s4-a698e/meson-bin"
SCRATCH = Path("$VALIDATION_STORAGE/scratch/665s6-a745b")
CI_HOME = SCRATCH / "ci-home"
BASE_REF = "dev-soft-core"
#: the runner image's tools, read as the host's pinned ones
SUBST = (("/opt/verilator/bin", "$VALIDATION_TOOLS/verilator-v5.050/bin"),)
RULES = json.loads(Path(__file__).with_name("not_run.json").read_text())


def sh(*a, cwd=None, env=None):
    return subprocess.run(a, cwd=cwd, env=env, check=True, capture_output=True, text=True).stdout.strip()


def not_run(wf: str, job: str, sid: str, name: str) -> dict | None:
    """The rule that keeps this step from running as written (its reason, and any command run instead)."""
    for rule in RULES["rules"]:
        if re.fullmatch(rule["workflow"], wf) and re.fullmatch(rule["job"], job) and (
                re.fullmatch(rule.get("id", "(?!)"), sid) or re.fullmatch(rule.get("name", "(?!)"), name)):
            return rule
    return None


def expr(text: str, ctx: dict) -> str:
    """Each ${{ }} expression of the pull_request event, or the text unchanged when it is not known."""
    def one(m):
        key = m.group(1).strip()
        return ctx.get(key, m.group(0))
    return re.sub(r"\$\{\{\s*(.*?)\s*\}\}", one, text)


def again(a, matrix, tag, work, logs) -> int:
    """Run named steps again on the job's existing clone and venv, in the environment of its first run."""
    env, ctx = environment(a, matrix, work)
    return steps(a, matrix, tag, work, logs, env, ctx)


def environment(a, matrix, work) -> tuple[dict, dict]:
    """The job's environment and the ${{ }} context, its venv made if it has none."""
    wt, temp, tmp = work / "wt", work / "runner_temp", work / "tmp"
    gh_env, gh_out, gh_path = work / "github_env", work / "github_output", work / "github_path"
    CI_HOME.mkdir(parents=True, exist_ok=True)
    env = {k: v for k, v in os.environ.items() if k in ("LANG", "LC_ALL", "USER", "TERM", "YOSYS_RESULT_ROOTS")}
    if a.gate_env:
        # the host's LiteX venv and its sbt caches; HOME stays the CI HOME, where the pinned SDK is
        env.update(PATH=f"{GATE_LITEX}:{TOOLS}", HOME=str(CI_HOME), LITEX_ENV_CC_TRIPLE="riscv32-linux",
                   COURSIER_MODE="offline", COURSIER_CACHE="$HOME/.cache/coursier",
                   SBT_OPTS=("-Dsbt.offline=true -Dsbt.global.base=$HOME/.sbt "
                             "-Dsbt.boot.directory=$HOME/.sbt/boot -Dsbt.ivy.home=$HOME/.ivy2"))
    else:
        venv = work / ("venv" if a.python == PY312 else "venv-" + Path(a.python).name)
        if not venv.exists():
            sh(a.python, "-m", "venv", str(venv))
            # the ubuntu-24.04 runner image's python3 carries PyYAML; a fresh venv does not
            sh(str(venv / "bin/python3"), "-m", "pip", "install", "--quiet", "pyyaml")
        env.update(PATH=f"{venv}/bin:{TOOLS}", HOME=str(CI_HOME))
    env.update(RUNNER_TEMP=str(temp), TMPDIR=str(tmp), GITHUB_WORKSPACE=str(wt), GITHUB_ENV=str(gh_env),
               GITHUB_OUTPUT=str(gh_out), GITHUB_PATH=str(gh_path), GITHUB_SHA=a.head, GITHUB_EVENT_NAME="pull_request",
               GITHUB_REF="refs/pull/853/merge", GITHUB_REPOSITORY="kebag-logic/milan-fpga", CI="true", ACT="true",
               GIT_ALLOW_PROTOCOL="file:https", VERILATOR="$VALIDATION_TOOLS/verilator-v5.050/bin/verilator",
               TSN_GEN_ROOT="$HOME/milan-fpga-management/tools/tsn-gen-deca300c", PYTHONHASHSEED="0")
    ctx = {"github.event_name": "pull_request", "github.base_ref": BASE_REF,
           "github.event.pull_request.base.ref": BASE_REF, "github.event.pull_request.head.sha": a.head,
           "github.event.pull_request.draft": "false", "github.sha": a.head, "github.workspace": str(wt),
           "github.repository": "kebag-logic/milan-fpga", "runner.temp": str(temp)}
    ctx.update({f"matrix.{k}": v for k, v in matrix.items()})
    ctx.update(json.loads(os.environ.get("REPLAY_NEEDS", "{}")))
    return env, ctx


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("workflow")
    ap.add_argument("job")
    ap.add_argument("head")
    ap.add_argument("root", type=Path)
    ap.add_argument("--matrix", action="append", default=[])
    ap.add_argument("--gate-env", action="store_true")
    ap.add_argument("--steps", default="")
    ap.add_argument("--base-tip", required=True, help="the live dev-soft-core tip the PR's base names")
    ap.add_argument("--reuse", action="store_true", help="with --steps: run them again on the job's own clone")
    ap.add_argument("--python", default=PY312, help="the interpreter the job's venv is made from")
    a = ap.parse_args()
    assert not a.reuse or a.steps, "--reuse runs named --steps again, never a whole job"
    matrix = dict(kv.split("=", 1) for kv in a.matrix)
    tag = a.job + "".join(f"-{k}{v}" for k, v in sorted(matrix.items()))
    work = a.root / tag
    logs = a.root / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    wt = work / "wt"
    if a.reuse:
        return again(a, matrix, tag, work, logs)
    assert not wt.exists(), f"{wt} exists: a job runs on a fresh clone"
    work.mkdir(parents=True)
    sh("git", "clone", "-q", "--shared", "--no-checkout", LANE, str(wt))
    sh("git", "-c", "advice.detachedHead=false", "checkout", "-q", "--detach", a.head, cwd=wt)
    assert sh("git", "rev-parse", "HEAD", cwd=wt) == a.head
    assert sh("git", "status", "--porcelain", cwd=wt) == ""
    sh("git", "update-ref", f"refs/remotes/origin/{BASE_REF}", a.base_tip, cwd=wt)
    gm = sh("git", "config", "--blob", f"{a.head}:.gitmodules", "--get-regexp", r"^submodule\..*\.path$", cwd=wt)
    for line in gm.splitlines():
        dep = line.split()[1]
        if (Path(LANE) / dep / ".git").exists():
            sh("git", "config", f"submodule.{dep}.url", f"{LANE}/{dep}", cwd=wt)
    sh("git", "remote", "set-url", "origin", ORIGIN, cwd=wt)
    for d in ("runner_temp", "tmp"):
        (work / d).mkdir()
    for f in ("github_env", "github_output", "github_path"):
        (work / f).touch()
    env, ctx = environment(a, matrix, work)
    return steps(a, matrix, tag, work, logs, env, ctx)


def steps(a, matrix, tag, work, logs, env, ctx) -> int:
    """Run the job's run: steps (or the named ones) in order, each logged with its rc."""
    wt = work / "wt"
    gh_env, gh_path = work / "github_env", work / "github_path"
    wf = yaml.safe_load((wt / ".github/workflows" / a.workflow).read_text())
    for k, v in (wf.get("env") or {}).items():
        env[k] = expr(str(v), ctx)
    body = wf["jobs"][a.job]
    for k, v in (body.get("env") or {}).items():
        env[k] = expr(str(v), ctx)
    only = set(filter(None, a.steps.split(",")))
    failed = 0
    for n, step in enumerate(body["steps"]):
        if "run" not in step:
            continue
        sid = step.get("id") or f"step{n}"
        name = step.get("name") or ""
        if only and sid not in only:
            continue
        rule = not_run(a.workflow, a.job, sid, name)
        if rule and rule.get("drop"):
            kept = [ln for ln in step["run"].splitlines() if not re.match(rule["drop"], ln)]
            rule = dict(rule, instead=rule["prepend"] + "\n" + "\n".join(kept))
        if rule and not rule.get("instead"):
            print(f"{tag}__{sid}\tNOT RUN\t{rule['reason']}", flush=True)
            continue
        for line in gh_env.read_text().splitlines():
            if "=" in line:
                k, v = line.split("=", 1)
                env[k] = v
        e = dict(env)
        extra = [p for p in gh_path.read_text().splitlines() if p.strip()]
        for old, new in SUBST:
            extra = [p.replace(old, new) for p in extra]
        if extra:
            e["PATH"] = ":".join(reversed(extra)) + ":" + env["PATH"]
        e.update({k: expr(str(v), ctx) for k, v in (step.get("env") or {}).items()})
        script = expr(rule["instead"] if rule else step["run"], ctx)
        for old, new in SUBST:
            script = script.replace(old, new)
        (work / f"{sid}.sh").write_text(script)
        log = logs / f"{tag}__{sid}.log"
        with open(log, "w") as out:
            out.write(f"# head {a.head} workflow {a.workflow} job {tag} step {sid}: {name}\n")
            if rule:
                out.write(f"# INSTEAD of the step as written ({rule['reason']}):\n# {rule['instead']}\n")
            out.flush()
            where = wt / expr(str(step.get("working-directory") or (body.get("defaults") or {}).get("run", {})
                                     .get("working-directory") or "."), ctx)
            rc = subprocess.run(["bash", "-e", str(work / f"{sid}.sh")], cwd=where, env=e, stdout=out,
                                stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL).returncode
        (logs / f"{tag}__{sid}.rc").write_text(f"{rc}\n")
        print(f"{tag}__{sid}\trc={rc}\t{name}", flush=True)
        failed += rc != 0
    status = sh("git", "status", "--porcelain", "--untracked-files=no", cwd=wt) if (wt / ".git").exists() else "(no .git)"
    (logs / f"{tag}__tree-after.txt").write_text(f"head {a.head}\ntracked changes:\n{status}\n")
    if not a.reuse:
        (logs / f"{tag}__DONE").write_text(f"failed {failed}\n")
    print(f"{tag} done, failed {failed}", flush=True)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
