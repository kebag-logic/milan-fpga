"""Record an exact author validation command, output and exit status."""
import datetime
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import time

root = Path(__file__).resolve().parent
label, *command = sys.argv[1:]
start = datetime.datetime.now(datetime.timezone.utc).isoformat()
tick = time.monotonic()
result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                        env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
(root / "logs").mkdir(exist_ok=True)
log = root / "logs" / (label + ".log")
log.write_bytes(result.stdout)
record = dict(label=label, command=command, shell=shlex.join(command), cwd=str(Path.cwd()),
              started=start, seconds=round(time.monotonic()-tick, 3), exit=result.returncode,
              log=str(log.relative_to(root)))
with (root / "commands.jsonl").open("a") as stream:
    stream.write(json.dumps(record) + "\n")
print(json.dumps(record))
print(result.stdout.decode("utf-8", errors="replace")[-5000:])
sys.exit(result.returncode)
