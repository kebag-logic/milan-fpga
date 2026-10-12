#!/usr/bin/env python3
"""Run review campaigns concurrently, awaiting every foreground command."""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys
import time

source = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parents[1]
head = "4bee75b2e647507a71ece50359fceb135c334757"
scratch = packet / "scratch"
receipts = packet / "receipts"
(scratch / "tmp").mkdir(parents=True, exist_ok=True)
env = dict(os.environ, TMPDIR=str(scratch / "tmp"), PYTHONDONTWRITEBYTECODE="1")
pinned = os.environ.get("REVIEW_VERILATOR", "$VALIDATION_TOOLS/pinned-verilator-5.050/verilator")
identity = subprocess.run([pinned, "--version"], capture_output=True, text=True, check=True).stdout
assert "Verilator 5.050" in identity, identity
(receipts / "compiler-identity.txt").write_text(identity)
wrapper = scratch / "limited-compiler.py"
wrapper.write_text("#!/usr/bin/env python3\nimport os,sys\na=sys.argv[1:]\nfor i in range(len(a)-1):\n if a[i] == '-j' and a[i+1] == '0': a[i+1]='2'\nos.execv(" + repr(pinned) + ", [" + repr(pinned) + "]+a)\n")
wrapper.chmod(0o755)
for name in ("gates", "observed", "controls"):
    tree = scratch / name
    if not tree.exists():
        subprocess.run(["git", "clone", "--quiet", "--shared", "--no-checkout", str(source), str(tree)], check=True)
        subprocess.run(["git", "-C", str(tree), "checkout", "--quiet", "--detach", head], check=True)

campaigns = [
    ("make-check", ["make", "-j16", "check"], scratch / "gates", {}),
    ("guards", ["python3", "-B", "tb/elab_guards/guards.py", "--frontend", "verilator", "--verilator", str(wrapper), "--jobs", "4"], source, {}),
    ("observed", ["make", "-j16", "run", "VERILATOR=" + str(wrapper)], scratch / "observed/tb/aecp_cmds", {"REQ_TAG_LOG": str(receipts / "observed-tags.txt")}),
    ("controls", ["python3", "-B", "tb/aecp_cmds/mutants.py", "--jobs", "2", "--verilator", str(wrapper), "--output", str(receipts / "controls")], scratch / "controls", {}),
]

def run(item):
    name, command, cwd, extra = item
    start = time.monotonic()
    print("START " + name, flush=True)
    with (receipts / (name + ".log")).open("w") as out:
        out.write("command: " + repr(command) + "\ncwd: " + str(cwd) + "\n")
        out.flush()
        result = subprocess.run(command, cwd=cwd, env=dict(env, **extra), stdout=out, stderr=subprocess.STDOUT)
    (receipts / (name + ".rc")).write_text(str(result.returncode) + "\n")
    record = dict(campaign=name, returncode=result.returncode, elapsed_seconds=round(time.monotonic()-start, 2))
    print(json.dumps(record), flush=True)
    return record

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(run, campaigns))
(receipts / "campaigns.json").write_text(json.dumps(results, indent=2) + "\n")
raise SystemExit(any(r["returncode"] for r in results))
