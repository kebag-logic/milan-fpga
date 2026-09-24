import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import time

out = Path(__file__).resolve().parent
label, *command = sys.argv[1:]
start = time.monotonic()
with (out / (label + ".log")).open("w") as log:
    result = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, timeout=7200)
elapsed = time.monotonic() - start
receipt = {"command": shlex.join(command), "rc": result.returncode,
           "seconds": round(elapsed, 3)}
(out / (label + ".json")).write_text(json.dumps(receipt, indent=2) + "\n")
print(f"{label}: rc {result.returncode}, {elapsed:.1f}s", flush=True)
text = (out / (label + ".log")).read_text(errors="replace")
print(text[-4500:] if len(text) > 4500 else text, end="", flush=True)
sys.exit(result.returncode)
