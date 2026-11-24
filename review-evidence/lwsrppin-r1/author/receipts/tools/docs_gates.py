#!/usr/bin/env python3
"""Run docs.yml's gate steps on a checkout: docs_gates.py REPO OUT BASE_SHA.

Every step with a run script runs as the workflow writes it, in bash with -e and pipefail, from REPO, except the
steps that install, fetch, resolve packages, set budgets or record receipts (the hosted runner's, listed in
not_run.txt). The em-dash gate runs as a push from BASE_SHA. The no-git docs step runs on a copy of REPO, since it
removes .git. Each step's log and rc go to OUT; summary.txt lists them.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

SKIP = ("Install", "Record", "Set CPU", "Fetch", "Resolve", "Retain", "Require every gate")


def main():
    repo, out, base = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3]
    out.mkdir(parents=True, exist_ok=True)
    wf = yaml.safe_load((repo / ".github/workflows/docs.yml").read_text())
    summary, skipped = [], []
    temp = out / "runner_temp"
    temp.mkdir(exist_ok=True)
    env = dict(os.environ, RUNNER_TEMP=str(temp), CI_CAMPAIGN_JOBS="4", GITHUB_WORKSPACE=str(repo),
               EVENT_NAME="push", PUSH_BEFORE_SHA=base, PR_BASE_REF="")
    for job, spec in wf["jobs"].items():
        for i, step in enumerate(spec.get("steps", [])):
            run, name = step.get("run"), step.get("name", f"step {i}")
            if not run:
                continue
            if name.startswith(SKIP):
                skipped.append(f"{job}#{i}: {name}")
                continue
            cwd = repo
            if "rm -rf .git" in run:
                cwd = out / "no-git-copy"
                shutil.rmtree(cwd, ignore_errors=True)
                shutil.copytree(repo, cwd, symlinks=True)
            label = f"{job}__{i}"
            result = subprocess.run(["bash", "-e", "-o", "pipefail", "-c", run], cwd=cwd, env=env,
                                    capture_output=True, text=True, timeout=7200)
            (out / f"{label}.log").write_text(result.stdout + result.stderr)
            summary.append(f"{job}#{i}\trc={result.returncode}\t{name}")
            print(summary[-1], flush=True)
    (out / "summary.txt").write_text("\n".join(summary) + "\n")
    (out / "not_run.txt").write_text("\n".join(skipped) + "\n")
    return int(any("\trc=0\t" not in s for s in summary))


if __name__ == "__main__":
    sys.exit(main())
