from pathlib import Path
import json
import subprocess
import sys
import time
out = Path(__file__).resolve().parent
label, *argv = sys.argv[1:]
start = time.monotonic()
with (out / (label + ".log")).open("w") as log:
    result = subprocess.run(argv, stdout=log, stderr=subprocess.STDOUT, timeout=14400)
record = dict(label=label, command=argv, rc=result.returncode, seconds=round(time.monotonic()-start, 2))
(out / (label + ".json")).write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps(record), flush=True)
print("".join((out / (label + ".log")).read_text(errors="replace").splitlines(keepends=True)[-12:]))
sys.exit(result.returncode)
