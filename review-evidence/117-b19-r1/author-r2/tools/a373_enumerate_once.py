"""Run one bounded enumeration on the controller host; caller holds bench lock."""
from pathlib import Path
from datetime import datetime, timezone
import subprocess
import sys
iface, number = sys.argv[1:]
assert number in {"1", "2", "3"}
p = Path("/tmp/117-a373")
out = p / ("run-" + number)
out.mkdir(exist_ok=False)
print("START " + datetime.now(timezone.utc).isoformat(), flush=True)
r = subprocess.run(["sudo", "-n", "timeout", "20s", str(p / "enum_probe"), iface, "12", str(out)], timeout=23)
print("END " + datetime.now(timezone.utc).isoformat() + " rc=" + str(r.returncode), flush=True)
raise SystemExit(r.returncode)
