"""Run one foreground command with a durable exit-code receipt."""
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import time

scratch = Path("$VALIDATION_STORAGE/400-403-a322")
packet = (Path.home() / "milan-fpga-management/2026-09-23/400-403-a322")
key, *command = sys.argv[1:]
env = dict(os.environ)
env["PATH"] = "$VALIDATION_TOOLS/verilator-v5.050/bin:" + env["PATH"]
env["VERILATOR_ROOT"] = "$VALIDATION_TOOLS/verilator-v5.050/share/verilator"
env["PYTHONUNBUFFERED"] = "1"
start = time.monotonic()
raw = scratch / (key + ".raw.log")
print("START", key, shlex.join(command), flush=True)
with raw.open("w") as stream:
    result = subprocess.run(command, env=env, stdout=stream,
                            stderr=subprocess.STDOUT, timeout=14400)
elapsed = round(time.monotonic() - start, 3)
def scrub(text):
    text = text.replace(str(Path.home()), "<home>")
    text = text.replace(str(scratch), "<scratch>")
    text = text.replace(str(packet), "<packet>")
    return text
content = scrub(raw.read_text(errors="replace"))
(packet / (key + ".log")).write_text(content)
receipt = dict(command=scrub(shlex.join(command)), returncode=result.returncode,
               seconds=elapsed, log=key + ".log")
(packet / (key + ".json")).write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt), flush=True)
print("\n".join(content.splitlines()[-14:]), flush=True)
sys.exit(result.returncode)
