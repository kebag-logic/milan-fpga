#!/usr/bin/env python3
import json
import os
import subprocess
import sys
import time
from pathlib import Path
out=Path(__file__).resolve().parent
command=sys.argv[-1]
chunk=command.startswith(("verilator ", "./obj_", "python3 render_mutants.py", "python3 gmstep_mutants.py"))
if not chunk:
    os.execv("/bin/bash", ["bash", *sys.argv[1:]])
name=f"sweep-chunk-{time.time_ns()}"
start=time.monotonic()
with (out/(name+".log")).open("w") as log:
    log.write(command+"\n"); log.flush()
    result=subprocess.run(["/bin/bash", *sys.argv[1:]], stdout=log, stderr=subprocess.STDOUT, timeout=14400)
record=dict(name=name, command=command, cwd=os.getcwd(), rc=result.returncode, seconds=round(time.monotonic()-start, 2))
with (out/"sweep-chunks.jsonl").open("a") as ledger:
    ledger.write(json.dumps(record)+"\n")
print(json.dumps(record), file=sys.stderr, flush=True)
sys.exit(result.returncode)
