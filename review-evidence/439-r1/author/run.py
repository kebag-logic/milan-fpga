#!/usr/bin/env python3
"""Record exact argv, raw stdout/stderr and exit without filtering."""
import datetime
import json
import os
from pathlib import Path
import subprocess
import sys
import time
root = Path(__file__).resolve().parent
label, *argv = sys.argv[1:]
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", VERILATOR_JOBS="8", MAKEFLAGS="-j8")
tick = time.monotonic()
result = subprocess.run(argv, capture_output=True, env=env, check=False)
for name, data in (("stdout", result.stdout), ("stderr", result.stderr)):
    (root / "logs" / f"{label}.{name}").write_bytes(data)
record = dict(label=label, argv=argv, cwd=os.getcwd(), started=started,
              seconds=time.monotonic()-tick, exit=result.returncode,
              env_overrides={key: env[key] for key in ("PYTHONDONTWRITEBYTECODE", "VERILATOR_JOBS", "MAKEFLAGS")})
with (root / "commands.jsonl").open("a") as stream:
    stream.write(json.dumps(record)+"\n")
print(json.dumps(record), flush=True)
sys.stdout.buffer.write(result.stdout)
sys.stderr.buffer.write(result.stderr)
sys.exit(result.returncode)
