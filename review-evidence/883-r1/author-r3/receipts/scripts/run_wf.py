#!/usr/bin/env python3
"""Run one job of a .github/workflows file, step by step, as a pull_request to dev runs it, on a fresh clean clone.

usage: run_wf.py <workflow> <job> <head sha> <base sha> <scratch root> [key=value ...]

The step list comes from the workflow in the clone, never from a list kept here. Each `run:` step's text and env
are taken from the file; `${{ }}` expressions are resolved from the pull_request event (base `dev`, the given head,
the merge base as base sha, a ready PR), the given matrix values, the outputs earlier steps wrote to GITHUB_OUTPUT,
and the needs outputs a dev PR yields (changes.rtl = true, full-ci-gate.run_full = true). An expression not in that
set refuses the step (rc 97), so nothing is guessed. Only NOT_RUN (not_run.json) may stand between a `run:` step and
its rc file, each with its reason; verify_wf.py fails on any step with neither rc 0 nor an entry.

Substitutions, each also recorded in the step log: `/opt/verilator/bin` (the hosted cache's Verilator 5.050 build)
is the host's pinned Verilator 5.050; GoogleTest 1.14.0 and the RV32 SDK come from the environment the hosted
install steps would have produced (the SDK through scripts/ci_rv32_sdk.py itself, a verified cache hit). In the
elaborate jobs the job-private LiteX environment, whose build needs sudo and sbt, is the host's LiteX environment
at the pinned revisions with the repository's patch series applied, first on PATH.
"""
import fnmatch
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import yaml

LANE = "<lane>"
ORIGIN = "https://github.com/kebag-logic/milan-fpga.git"
S = Path("<scratch>")
VENV = str(S / "venv-ci/bin")
HOME = str(S / "home-ci")
VERILATOR_DIR = "<tools>/pinned-verilator-5.050"
GT = "<tools>/gtest-1.14.0"
TOOLS = (f"{VERILATOR_DIR}:<tools>/sv2v-v0.0.12:<scratch-root>/a662/make43/bin:"
         "/usr/local/sbin:/usr/local/bin:/usr/bin:/bin")
LITEX_BIN = "<litex>/venv/bin"
NOT_RUN = json.loads((Path(__file__).with_name("not_run.json")).read_text())
EXPR = re.compile(r"\$\{\{\s*(.*?)\s*\}\}")


def main() -> int:
    wfname, job, head, base, root = sys.argv[1:6]
    matrix = dict(a.split("=", 1) for a in sys.argv[6:])
    tag0 = f"{wfname}__{job}" + "".join(f"__{k}{v}" for k, v in sorted(matrix.items()))
    root = Path(root)
    work = root / "work" / tag0
    logs = root / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    wt = work / "wt"
    assert not wt.exists(), f"{wt} exists: a job runs on a fresh clone"
    wt.parent.mkdir(parents=True, exist_ok=True)

    def run(*a, cwd=None):
        return subprocess.run(a, cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()

    run("git", "clone", "-q", "--shared", "--no-checkout", LANE, str(wt))
    run("git", "fetch", "-q", LANE, head, cwd=wt)
    run("git", "-c", "advice.detachedHead=false", "checkout", "-q", "--detach", head, cwd=wt)
    assert run("git", "rev-parse", "HEAD", cwd=wt) == head
    assert run("git", "status", "--porcelain", cwd=wt) == ""
    run("git", "remote", "set-url", "origin", ORIGIN, cwd=wt)
    # the base branch as origin/dev, as the checkout of a pull_request has it
    run("git", "fetch", "-q", LANE, f"+refs/remotes/origin/dev:refs/remotes/origin/dev", cwd=wt)
    # actions/checkout of a pull_request checks out its merge commit: the merge tree of the base tip and the
    # head, parents (base tip, head). GITHUB_SHA names it; PR_HEAD_SHA names the head.
    tip = run("git", "rev-parse", "refs/remotes/origin/dev", cwd=wt)
    tree = run("git", "merge-tree", "--write-tree", tip, head, cwd=wt).splitlines()[0]
    ident = dict(os.environ, GIT_AUTHOR_NAME="pr-merge", GIT_AUTHOR_EMAIL="pr-merge@localhost",
                 GIT_COMMITTER_NAME="pr-merge", GIT_COMMITTER_EMAIL="pr-merge@localhost",
                 GIT_AUTHOR_DATE="2026-11-11T00:00:00Z", GIT_COMMITTER_DATE="2026-11-11T00:00:00Z")
    merge = subprocess.run(["git", "commit-tree", tree, "-p", tip, "-p", head, "-m", f"Merge {head} into {tip}"],
                           cwd=wt, env=ident, check=True, capture_output=True, text=True).stdout.strip()
    run("git", "-c", "advice.detachedHead=false", "checkout", "-q", "--detach", merge, cwd=wt)
    assert run("git", "status", "--porcelain", cwd=wt) == ""
    gm = run("git", "config", "--blob", f"{head}:.gitmodules", "--get-regexp", r"^submodule\..*\.path$", cwd=wt)
    for line in gm.splitlines():
        dep = line.split()[1]
        if (Path(LANE) / dep / ".git").exists():
            run("git", "config", f"submodule.{dep}.url", f"{LANE}/{dep}", cwd=wt)

    temp = work / "runner_temp"
    temp.mkdir(exist_ok=True)
    tmp = work / "tmp"
    tmp.mkdir(exist_ok=True)
    gh_env = work / "github_env"
    gh_env.touch()
    gh_path = work / "github_path"
    gh_path.touch()
    wf = yaml.safe_load((wt / ".github/workflows" / f"{wfname}.yml").read_text())
    # actions/download-artifact: rtl.yml's yosys-portability takes each shard's uploaded `yosys-results` (artifact
    # yosys-results-<shard>) under $RUNNER_TEMP/all-yosys-results/<artifact>; here each comes from that shard's own
    # run of this replay, at this head
    if wfname == "rtl" and job == "yosys-portability":
        import shutil
        for k in range(4):
            src = root / "work" / f"rtl__yosys-shards__shard{k}__total4" / "runner_temp" / "yosys-results"
            if src.is_dir():
                shutil.copytree(src, temp / "all-yosys-results" / f"yosys-results-{k}")
    jd = wf["jobs"][job]
    step_out: dict[str, dict[str, str]] = {}
    # full-ci-gate's `target` step writes target_sha=$GITHUB_SHA, the merge commit a pull_request checks out
    needs_out = {"changes": {"rtl": "true"},
                 "full-ci-gate": {"run_full": "true", "target_sha": merge}}

    def resolve(text: str) -> str:
        def one(m: re.Match) -> str:
            e = m.group(1)
            fixed = {
                "github.workspace": str(wt), "github.event_name": "pull_request",
                "github.event.pull_request.base.ref": "dev", "github.event.pull_request.base.sha": base,
                "github.event.pull_request.head.sha": head, "github.event.pull_request.draft": "false",
                "github.event.before": "", "github.token": "", "github.sha": merge,
                "toJSON(matrix)": json.dumps(matrix) if matrix else "null", "job.status": "success",
            }
            if e in fixed:
                return fixed[e]
            if e.startswith("matrix.") and e[7:] in matrix:
                return matrix[e[7:]]
            mo = re.fullmatch(r"steps\.([\w-]+)\.outputs\.([\w-]+)", e)
            if mo:
                return step_out.get(mo[1], {}).get(mo[2], "")
            mo = re.fullmatch(r"needs\.([\w-]+)\.outputs\.([\w-]+)", e)
            if mo and mo[1] in needs_out and mo[2] in needs_out[mo[1]]:
                return needs_out[mo[1]][mo[2]]
            if re.fullmatch(r"needs\.[\w-]+\.result", e):
                return "success"
            if e in ("toJSON(needs)", "toJSON(steps)"):
                return "{}"
            raise KeyError(e)
        return EXPR.sub(one, text)

    base_env = {k: v for k, v in os.environ.items() if k in ("LANG", "LC_ALL", "USER", "TERM")}
    base_env.update(
        PATH=f"{VENV}:{TOOLS}", HOME=HOME, RUNNER_TEMP=str(temp), TMPDIR=str(tmp), RUNNER_OS="Linux",
        GITHUB_WORKSPACE=str(wt), GITHUB_ENV=str(gh_env), GITHUB_PATH=str(gh_path), GITHUB_SHA=merge,
        GITHUB_EVENT_NAME="pull_request", GITHUB_BASE_REF="dev", GITHUB_RUN_ID="0", CI="true",
        # a pull_request's ref is refs/pull/<number>/merge; the PR has no number yet, so 0
        GITHUB_REF="refs/pull/0/merge", GITHUB_REPOSITORY="kebag-logic/milan-fpga",
        GIT_ALLOW_PROTOCOL="file:https", PYTHONHASHSEED="0",
        VERILATOR=f"{VERILATOR_DIR}/verilator",
        TSN_GEN_ROOT="<mgmt>/tools/tsn-gen-deca300c",
        PKG_CONFIG_PATH=f"{GT}/lib/pkgconfig", CMAKE_PREFIX_PATH=GT, LD_LIBRARY_PATH=f"{GT}/lib",
        CPLUS_INCLUDE_PATH=f"{GT}/include", C_INCLUDE_PATH=f"{GT}/include", LIBRARY_PATH=f"{GT}/lib")
    if wfname == "elaborate" and job.startswith("elaborate-gates-"):
        base_env["PATH"] = f"{LITEX_BIN}:" + base_env["PATH"]
    for scope in (wf.get("env") or {}, jd.get("env") or {}):
        for k, v in scope.items():
            base_env[k] = resolve(str(v))

    failed = 0
    for n, step in enumerate(jd.get("steps", [])):
        if "run" not in step:
            continue
        sid = step.get("id") or f"step{n}"
        tag = f"{tag0}__{sid}"
        key = f"{wfname}/{job}/{sid}"
        if any(fnmatch.fnmatchcase(key, pat) for pat in NOT_RUN):
            continue
        env = dict(base_env)
        for line in gh_env.read_text().splitlines():
            if "=" in line:
                k, v = line.split("=", 1)
                env[k] = v
        extra = [p for p in gh_path.read_text().splitlines() if p.strip()]
        extra = [VERILATOR_DIR if p == "/opt/verilator/bin" else p for p in extra]
        if extra:
            env["PATH"] = ":".join(reversed(extra)) + ":" + env["PATH"]
        log = logs / f"{tag}.log"
        try:
            for k, v in (step.get("env") or {}).items():
                env[k] = resolve(str(v))
            text = resolve(step["run"])
        except KeyError as unknown:
            log.write_text(f"# refused: unresolved expression {unknown}\n")
            (logs / f"{tag}.rc").write_text("97\n")
            print(f"{tag}\trc=97 (unresolved {unknown})", flush=True)
            failed += 1
            continue
        subs = []
        if "/opt/verilator/bin" in text:
            text = text.replace("/opt/verilator/bin", VERILATOR_DIR)
            subs.append(f"/opt/verilator/bin -> the pinned Verilator 5.050 ({VERILATOR_DIR})")
        out_file = work / f"{sid}.output"
        out_file.write_text("")
        env["GITHUB_OUTPUT"] = str(out_file)
        script = work / f"{sid}.sh"
        script.write_text(text)
        shell = step.get("shell") or (jd.get("defaults") or {}).get("run", {}).get("shell")
        # GitHub's Linux runner: no shell key is `bash -e {0}`; `shell: bash` adds --noprofile --norc -o pipefail
        if shell is None:
            argv = ["bash", "-e", str(script)]
        elif shell == "bash":
            argv = ["bash", "--noprofile", "--norc", "-e", "-o", "pipefail", str(script)]
        else:
            argv = shell.replace("{0}", str(script)).split()
        wd = wt / step["working-directory"] if "working-directory" in step else wt
        with open(log, "w") as out:
            out.write(f"# head {head} merge {merge} workflow {wfname} job {job} matrix {matrix} step {sid}: {step.get('name')}\n")
            for s in subs:
                out.write(f"# substitution: {s}\n")
            out.flush()
            rc = subprocess.run(argv, cwd=wd, env=env, stdout=out, stderr=subprocess.STDOUT,
                                stdin=subprocess.DEVNULL).returncode
        outs = {}
        for line in out_file.read_text().splitlines():
            if "=" in line:
                k, v = line.split("=", 1)
                outs[k] = v
        step_out[sid] = outs
        (logs / f"{tag}.rc").write_text(f"{rc}\n")
        print(f"{tag}\trc={rc}", flush=True)
        failed += rc != 0
    status = run("git", "status", "--porcelain", cwd=wt) if (wt / ".git").exists() else "(no .git: removed by the job)"
    (logs / f"{tag0}__tree-after.txt").write_text(f"head {head}\nmerge {merge} (tree {tree})\nstatus:\n{status}\n")
    (logs / f"{tag0}__DONE").write_text(f"failed {failed}\n")
    print(f"{tag0} done, failed {failed}", flush=True)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
