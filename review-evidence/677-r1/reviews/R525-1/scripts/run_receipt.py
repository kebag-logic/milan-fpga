#!/usr/bin/env python3
"""Run one foreground command and retain its output, status and elapsed time.
Usage: run_receipt.py REPO PACKET NAME COMMAND [ARG ...]
Outputs only replace the two supplied roots and the invoking home path.
"""
import json, os, pathlib, subprocess, sys, time
repo, packet = map(lambda x: pathlib.Path(x).resolve(), sys.argv[1:3])
name, command = sys.argv[3], sys.argv[4:]
scratch = packet / "scratch" / name
scratch.mkdir(parents=True, exist_ok=True)
env = dict(os.environ, TMPDIR=str(scratch), PYTHONPYCACHEPREFIX=str(scratch / "pycache"), PYTHONUNBUFFERED="1")
start = time.monotonic()
raw = scratch / "raw.log"
with raw.open("w") as log:
    result = subprocess.run(command, cwd=repo, env=env, stdout=log, stderr=subprocess.STDOUT, check=False)
elapsed = time.monotonic() - start
replacements = [(str(packet), "<packet>"), (str(repo), "<source>"), (str(pathlib.Path.home()), "<home>")]
def redact(s):
    for old, new in replacements: s = s.replace(old,new)
    return s
receipts=packet / "receipts"
receipts.mkdir(exist_ok=True)
(receipts / f"{name}.log").write_text(redact(raw.read_text(errors="replace")))
(receipts / f"{name}.rc").write_text(str(result.returncode)+"\n")
(receipts / f"{name}.json").write_text(json.dumps({"command": [redact(x) for x in command], "rc": result.returncode, "elapsed_seconds": round(elapsed,3), "redactions": "source, packet and home roots only"},indent=2)+"\n")
print(name, "rc",result.returncode,"seconds",round(elapsed,1),flush=True)
print("\n".join(redact(raw.read_text(errors="replace")).splitlines()[-15:]),flush=True)
sys.exit(result.returncode)
