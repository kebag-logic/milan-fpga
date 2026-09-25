import datetime
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import time

OUT = Path(__file__).resolve().parent
ROOT = Path("$LANES/545-crf-servo-slew")
env = dict(os.environ)
env["PATH"] = "/tmp/milan-a320-python/bin:" + env["PATH"]

def run(name, command, cwd=ROOT):
    log = OUT / (name + ".log")
    started = time.monotonic()
    print("START", name, shlex.join(command)[:180], flush=True)
    with log.open("w") as stream:
        stream.write("cwd: " + str(cwd) + "\ncommand: " + shlex.join(command) + "\n")
        stream.flush()
        try:
            result = subprocess.run(command, cwd=cwd, env=env, stdout=stream,
                                    stderr=subprocess.STDOUT, timeout=21600)
            rc = result.returncode
        except subprocess.TimeoutExpired:
            rc = 124
    seconds = time.monotonic() - started
    row = dict(name=name, command=command, cwd=str(cwd), rc=rc,
               seconds=round(seconds, 3), utc=datetime.datetime.now(datetime.UTC).isoformat())
    with (OUT / "gates.jsonl").open("a") as stream:
        stream.write(json.dumps(row) + "\n")
    with (OUT / "HANDOFF.md").open("a") as stream:
        stream.write("\n| " + name + " | `" + shlex.join(command).replace("|", "\\|") +
                     "` | " + str(rc) + " | " + log.name + "; " + f"{seconds:.3f} s" + " |\n")
    print("END", name, "rc", rc, "seconds", round(seconds, 3), flush=True)
    print("\n".join(log.read_text(errors="replace").splitlines()[-5:]), flush=True)
    return rc

if __name__ == "__main__":
    sys.exit(run(sys.argv[1], sys.argv[2:]))
