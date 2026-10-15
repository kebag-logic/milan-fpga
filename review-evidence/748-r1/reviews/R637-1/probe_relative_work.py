#!/usr/bin/env python3
"""Exercise the real leg runner with a supported relative scratch path."""
import importlib
import json
import os
from pathlib import Path
import sys
import threading
import tempfile
repo, packet = (Path(x).resolve() for x in sys.argv[1:3])
sys.dont_write_bytecode = True
sys.path.insert(0, str(repo / "scripts"))
m = importlib.import_module("ci_toolcache_isolation")
work = Path(tempfile.mkdtemp(prefix="relative-path-", dir=packet / "scratch"))
os.chdir(work)
leg = m.Leg("relative", Path("run/leg"), "HEAD", Path(sys.prefix), None)
m.drive(leg, [{"name": "no-op step", "run": "true\n"}], threading.Barrier(1))
result = {"work_argument": "run", "step_results": leg.results, "log": leg.log.read_text()}
absolute = m.Leg("absolute", work / "absolute/leg", "HEAD", Path(sys.prefix), None)
m.drive(absolute, [{"name": "no-op step", "run": "true\n"}], threading.Barrier(1))
result["absolute_step_results"] = absolute.results
assert absolute.results[0]["rc"] == 0
print(json.dumps(result, indent=2))
assert leg.results[0]["rc"] != 0
assert "No such file or directory" in result["log"]
print("REPRODUCED: relative --work creates a step path relative to the caller, then opens it relative to the workspace")
