#!/usr/bin/env python3
"""Compare the trace wrapper's observable behavior with the existing gate."""
import json
import os
from pathlib import Path
import subprocess

packet = Path(__file__).resolve().parents[1]
bench = packet / "scratch/observed/tb/aecp_cmds"
results = []
for arg in ("obj_dir/observed.json", "obj_dir/no-such-observation.json"):
    pairs = []
    for argv in (["python3", "-B", "../../scripts/check_aecp_commands.py", "--observed", arg],
                 ["python3", "-B", "check_observed.py", arg]):
        env = dict(os.environ)
        env.pop("REQ_TAG_LOG", None)
        result = subprocess.run(argv, cwd=bench, env=env, capture_output=True, text=True)
        pairs.append(dict(command=argv, rc=result.returncode, stdout=result.stdout, stderr=result.stderr))
    assert all(pairs[0][key] == pairs[1][key] for key in ("rc", "stdout", "stderr"))
    results.append(dict(observation=arg, identical=True, runs=pairs))
(packet / "receipts/wrapper-parity.json").write_text(json.dumps(results, indent=2)+"\n")
print("PASS: wrapper preserves output and return status for valid and unreadable observations.")
