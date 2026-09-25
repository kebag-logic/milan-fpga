import datetime
import json
from pathlib import Path
import subprocess
import sys
import time

out = Path(__file__).resolve().parent
name, *command = sys.argv[1:]
head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
dirty = subprocess.check_output(["git", "status", "--porcelain"], text=True)
start = time.monotonic()
log = out / (name + ".log")
print("START", name, command, flush=True)
with log.open("w") as stream:
    result = subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT, check=False)
record = dict(name=name, command=command, head=head, dirty=dirty, rc=result.returncode,
              seconds=round(time.monotonic()-start, 2), log=log.name,
              finished=datetime.datetime.now(datetime.timezone.utc).isoformat())
with (out / "gates.jsonl").open("a") as stream:
    stream.write(json.dumps(record) + "\n")
print(json.dumps(record), flush=True)
print("\n".join(log.read_text(errors="replace").splitlines()[-18:]), flush=True)
sys.exit(result.returncode)
