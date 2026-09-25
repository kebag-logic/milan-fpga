import datetime
import json
from pathlib import Path
import shlex
import subprocess
import sys
import time

out = Path(__file__).resolve().parent
label, *command = sys.argv[1:]
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
begin = time.monotonic()
log = out / (label + ".log")
with log.open("w") as stream:
    stream.write("$ " + shlex.join(command) + "\n")
    stream.flush()
    result = subprocess.run(["rtk", "proxy", "timeout", "3600", *command],
                            stdout=stream, stderr=subprocess.STDOUT)
record = {"gate": label, "command": shlex.join(command), "rc": result.returncode,
          "started": started, "elapsed_seconds": round(time.monotonic() - begin, 2),
          "log": log.name}
with (out / "gates.jsonl").open("a") as stream:
    stream.write(json.dumps(record) + "\n")
print(log.read_text())
print(json.dumps(record))
sys.exit(result.returncode)
