#!/usr/bin/env python3
"""Capture a public GitHub GET response without writing remote state."""
import argparse
import json
from pathlib import Path
import subprocess
p = argparse.ArgumentParser()
p.add_argument("endpoint")
p.add_argument("output", type=Path)
p.add_argument("--paginate", action="store_true")
a = p.parse_args()
cmd = ["gh", "api", a.endpoint]
if a.paginate:
    cmd += ["--paginate", "--slurp"]
r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
if r.returncode:
    raise SystemExit(r.stderr.decode())
data = json.loads(r.stdout)
a.output.parent.mkdir(parents=True, exist_ok=True)
a.output.write_text(json.dumps(data, indent=2) + "\n")
print(str(a.output) + ": captured")
