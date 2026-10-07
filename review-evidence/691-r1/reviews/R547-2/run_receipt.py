#!/usr/bin/env python3
"""Run one foreground command, retain raw output in scratch and path-neutral receipts.
Usage: python3 run_receipt.py PACKET LABEL CWD COMMAND [ARG...]
"""
import os, pathlib, shlex, subprocess, sys, time
packet = pathlib.Path(sys.argv[1]).resolve()
label, cwd, command = sys.argv[2], sys.argv[3], sys.argv[4:]
raw = packet / "scratch" / (label + ".raw.log")
start = time.monotonic()
with raw.open("w") as stream:
    result = subprocess.run(command, cwd=cwd, stdout=stream, stderr=subprocess.STDOUT, env={**os.environ, "PYTHONDONTWRITEBYTECODE":"1", "PYTHONHASHSEED":"0", "TMPDIR":str(packet/"scratch")})
text = raw.read_text(errors="replace")
for before, after in ((str(packet), "$PACKET"), (str(pathlib.Path(cwd).resolve()), "$WORKDIR"), (os.path.expanduser("~"), "$HOME")):
    text = text.replace(before, after)
(packet / (label + ".log")).write_text(text)
(packet / (label + ".rc")).write_text(str(result.returncode) + "\n")
receipt = {"command":command,"cwd":cwd,"exit":result.returncode,"elapsed_s":round(time.monotonic()-start,3)}
import json
s = json.dumps(receipt,indent=2)
for before, after in ((str(packet), "$PACKET"), (str(pathlib.Path(cwd).resolve()), "$WORKDIR"), (os.path.expanduser("~"), "$HOME")):
    s=s.replace(before,after)
(packet/(label+".command.json")).write_text(s+"\n")
print(label, "rc",result.returncode, "seconds",receipt["elapsed_s"],flush=True)
print("\n".join(text.splitlines()[-14:]),flush=True)
sys.exit(result.returncode)
