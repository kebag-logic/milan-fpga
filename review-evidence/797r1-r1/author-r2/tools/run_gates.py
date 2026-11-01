#!/usr/bin/env python3
"""Run the docs workflow's gate steps on the committed head, one bash -e
script per step, recording each exit status and output as a receipt.

Usage: run_gates.py <lane> <receipt dir> <first> <last>
Install, cache and submodule-fetch steps are not rerun (the scratch venv and
host tools provide them); the em-dash base is the merge base with dev; the
git-free job runs in a git-archive export under /tmp."""
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

LANE, OUT = Path(sys.argv[1]), Path(sys.argv[2])
FIRST, LAST = int(sys.argv[3]), int(sys.argv[4])
VENV = "/tmp/797-a711-wd"
RUNNER_TEMP = "/tmp/797-a711-runner"
BASE = "1e80128f0a467b58bf884b7d9bf62e013a2fb141"
SKIP = {"Install the python gate dependencies", "Install the pinned Markdown renderer",
        "Install diagram gate dependencies", "Install the pinned sv2v release",
        "Fetch the builder source dependencies", "Fetch the engine authority the builder derives from"}
steps = json.loads(Path("/tmp/797-a711-tools/steps.json").read_text())
OUT.mkdir(parents=True, exist_ok=True)
subprocess.run(["rm", "-rf", RUNNER_TEMP], check=True)
Path(RUNNER_TEMP).mkdir(parents=True, exist_ok=True)
env = dict(os.environ, HOME="/tmp/797-a711-home", PATH=f"{VENV}/bin:" + os.environ["PATH"], RUNNER_TEMP=RUNNER_TEMP,
           GITHUB_WORKSPACE=str(LANE), EVENT_NAME="pull_request", PR_BASE_REF="dev")


def mask(text: str) -> str:
    """Host paths out of a receipt."""
    text = text.replace(str(LANE), "<lane>").replace(VENV, "<venv>").replace(RUNNER_TEMP, "<runner-temp>")
    return text.replace("/tmp/797-a711-home", "$HOME").replace(os.environ["HOME"], "$HOME")


summary = OUT / "summary.tsv"
for idx in range(FIRST, LAST + 1):
    step = steps[idx]
    name = step["name"]
    if name in SKIP:
        line = f"{idx}\t{step['job']}\t{name}\tnot rerun (setup step)\t-\n"
        with summary.open("a") as fh:
            fh.write(line)
        continue
    run = step["run"]
    cwd = LANE
    if name == "Build the validated HDL reference":
        run = "\n".join(ln for ln in run.splitlines() if "pip install" not in ln and "requirements.txt" not in ln)
    if name == "Added-line em-dash gate":
        run = f"python3 scripts/check_em_dash.py --base {BASE}\npython3 scripts/check_em_dash.py --selftest"
    if name == "End-station builder gates":
        run = "\n".join(ln for ln in run.splitlines() if "pip install" not in ln)
    if name == "Strip git metadata, then run the docs gate":
        export = Path("/tmp/797-a711-nogit")
        subprocess.run(["rm", "-rf", str(export)], check=True)
        export.mkdir()
        archive = subprocess.run(["git", "-C", str(LANE), "archive", "--format=tar", "HEAD"],
                                 check=True, capture_output=True).stdout
        subprocess.run(["tar", "-x", "-C", str(export)], input=archive, check=True)
        cwd = export
        run = run.replace("rm -rf .git\n", "test ! -e .git\n")
    script = Path(RUNNER_TEMP) / f"step{idx}.sh"
    script.write_text(run + "\n")
    t0 = time.time()
    proc = subprocess.run(["bash", "-e", str(script)], cwd=cwd, env=env, capture_output=True, text=True)
    dt = time.time() - t0
    body = mask(f"$ {run}\n--- rc={proc.returncode} seconds={dt:.1f}\n{proc.stdout}{proc.stderr}")
    slug = re.sub(r"[^A-Za-z0-9]+", "-", name).strip("-").lower()[:60]
    dest = OUT / f"{idx:02d}-{slug}.txt"
    data = body.encode()
    if len(data) > 200_000:
        keep = Path("/tmp/797-a711-receipts-large") / dest.name
        keep.parent.mkdir(exist_ok=True)
        keep.write_bytes(data)
        tail = "\n".join(body.splitlines()[-40:])
        dest.write_text(f"output too large for the receipt directory: {len(data)} bytes, "
                        f"sha256 {hashlib.sha256(data).hexdigest()}\nlast 40 lines:\n{tail}\n")
    else:
        dest.write_bytes(data)
    with summary.open("a") as fh:
        fh.write(f"{idx}\t{step['job']}\t{name}\trc={proc.returncode}\t{dt:.0f}s\n")
    print(f"{idx:02d} rc={proc.returncode} {dt:6.1f}s {name}", flush=True)
