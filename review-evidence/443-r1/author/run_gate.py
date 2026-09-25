import json
import os
import subprocess
import sys
import time
from pathlib import Path
out = Path(__file__).resolve().parent
name, *command = sys.argv[1:]
start = time.monotonic()
with (out / (name + ".log")).open("w") as log:
    print("COMMAND:", " ".join(command), flush=True)
    log.write("COMMAND: " + " ".join(command) + "\n")
    log.flush()
    result = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, timeout=14400)
record = dict(name=name, command=command, cwd=os.getcwd(), rc=result.returncode, seconds=round(time.monotonic()-start, 2))
with (out / "gates.jsonl").open("a") as ledger:
    ledger.write(json.dumps(record) + "\n")
print(json.dumps(record), flush=True)
lines=(out/(name+".log")).read_text(errors="replace").splitlines()
print("\n".join(lines[-25:]))
sys.exit(result.returncode)
