#!/usr/bin/env python3
"""Run focused read-only gates; invoke with the candidate checkout as cwd."""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys
import time

packet = Path(__file__).resolve().parent
scratch = packet / "scratch"
scratch.mkdir(exist_ok=True)
env = dict(os.environ, TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE="1", GIT_NO_REPLACE_OBJECTS="1")
commands = {
    "gen_toc": ["python3", "scripts/gen_toc.py", "--check"],
    "docs_check": ["python3", "scripts/docs_check.py"],
    "check_doc_style": ["python3", "scripts/check_doc_style.py"],
    "check_em_dash": ["python3", "scripts/check_em_dash.py", "--base", "e21c1ca024d37ea188ad15b5c8f9c2dae18628df"],
    "pp_baseline_selftest": ["python3", "syn/ooc/pp_baseline.py", "--selftest"],
}

def run(item):
    name, command = item
    start = time.monotonic()
    with (packet / (name + ".log")).open("wb") as log:
        result = subprocess.run([sys.executable, *command[1:]], env=env, stdout=log, stderr=subprocess.STDOUT, timeout=540)
    elapsed = round(time.monotonic() - start, 3)
    (packet / (name + ".rc")).write_text(str(result.returncode) + "\n")
    return dict(name=name, command=command, rc=result.returncode, seconds=elapsed)

if sys.argv[1:]:
    commands = {name: commands[name] for name in sys.argv[1:]}

# Each subprocess is awaited; the foreground driver waits for every result.
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
    results = list(pool.map(run, commands.items()))
prior = packet / "focused_results.json"
if prior.exists():
    results = [r for r in json.loads(prior.read_text()) if r["name"] not in commands] + results
(packet / "focused_results.json").write_text(json.dumps(results, indent=2) + "\n")
for result in results:
    print(result["name"], "rc=" + str(result["rc"]), "seconds=" + str(result["seconds"]))
sys.exit(int(any(result["rc"] for result in results)))
