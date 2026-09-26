import datetime
import json
from pathlib import Path
import subprocess
import sys
import time

out = Path("$MANAGEMENT/2026-09-23/502-a338")
name, *cmd = sys.argv[1:]
start = time.monotonic()
with (out / (name + ".log")).open("w") as log:
    result = subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT, timeout=21600)
record = dict(name=name, command=cmd, cwd=str(Path.cwd()), exit_code=result.returncode, seconds=round(time.monotonic()-start, 2), timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat())
with (out / "gates.jsonl").open("a") as log:
    log.write(json.dumps(record) + "\n")
print(json.dumps(record), flush=True)
print("".join((out / (name + ".log")).read_text(errors="replace").splitlines(keepends=True)[-12:]), flush=True)
sys.exit(result.returncode)
