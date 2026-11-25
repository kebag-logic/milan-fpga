#!/usr/bin/env python3
"""Run selected docs.yml steps on a checkout: docs_gates_r2.py REPO OUT BASE_SHA STEP[,STEP...] [--md VENV].

Round 1's docs_gates.py with a step selection: each STEP is `job#index` as docs.yml orders its steps, run as the
workflow writes it, in bash with -e and pipefail, from REPO. The em-dash gate runs as a push from BASE_SHA. The
no-git docs step runs on a copy of REPO without its ignored build trees (obj_*, __pycache__), since it removes
.git. --md VENV puts the pinned Markdown renderer's venv first on PATH (the renderer steps). Each step's log and rc
go to OUT; summary.txt lists them, appended across invocations.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

import yaml


def main():
    args = sys.argv[1:]
    venv = None
    if "--md" in args:
        at = args.index("--md")
        venv = Path(args[at + 1]).resolve()
        del args[at:at + 2]
    repo, out, base, wanted = Path(args[0]).resolve(), Path(args[1]).resolve(), args[2], args[3].split(",")
    out.mkdir(parents=True, exist_ok=True)
    wf = yaml.safe_load((repo / ".github/workflows/docs.yml").read_text())
    temp = out / "runner_temp"
    temp.mkdir(exist_ok=True)
    env = dict(os.environ, RUNNER_TEMP=str(temp), CI_CAMPAIGN_JOBS="4", GITHUB_WORKSPACE=str(repo),
               EVENT_NAME="push", PUSH_BEFORE_SHA=base, PR_BASE_REF="")
    if venv is not None:
        env["PATH"] = f"{venv / 'bin'}:{env['PATH']}"
        env["VIRTUAL_ENV"] = str(venv)
    steps = {f"{job}#{i}": step for job, spec in wf["jobs"].items() for i, step in enumerate(spec.get("steps", []))}
    failed = 0
    with (out / "summary.txt").open("a", encoding="utf-8") as summary:
        for key in wanted:
            step = steps[key]
            run, name = step["run"], step.get("name", key)
            cwd = repo
            if "rm -rf .git" in run:
                cwd = out / "no-git-copy"
                shutil.rmtree(cwd, ignore_errors=True)
                shutil.copytree(repo, cwd, symlinks=True, ignore=shutil.ignore_patterns("obj_*", "__pycache__"))
            result = subprocess.run(["bash", "-e", "-o", "pipefail", "-c", run], cwd=cwd, env=env,
                                    capture_output=True, text=True, timeout=3600, check=False)
            label = key.replace("#", "__") + ("-md" if venv else "")
            (out / f"{label}.log").write_text(result.stdout + result.stderr, encoding="utf-8")
            line = f"{key}\trc={result.returncode}\t{name}{' (pinned renderer)' if venv else ''}"
            summary.write(line + "\n")
            print(line, flush=True)
            failed += result.returncode != 0
            if cwd != repo:
                shutil.rmtree(cwd, ignore_errors=True)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
