#!/usr/bin/env python3
"""Record a foreground command; usage: run.py REPO LABEL COMMAND [ARG ...]."""
import json, os, subprocess, sys, time
from pathlib import Path
packet = Path(__file__).resolve().parents[1]
repo, label, *command = sys.argv[1:]
(packet / 'scratch/tmp').mkdir(parents=True, exist_ok=True)
env = dict(os.environ, TMPDIR=str(packet / 'scratch/tmp'), PYTHONDONTWRITEBYTECODE='1')
started = time.monotonic()
with (packet / 'receipts' / (label + '.log')).open('wb') as log:
    rc = subprocess.run(command, cwd=repo, env=env, stdout=log, stderr=subprocess.STDOUT, check=False).returncode
elapsed = time.monotonic() - started
(packet / 'receipts' / (label + '.rc')).write_text(str(rc) + '\n')
(packet / 'receipts' / (label + '.json')).write_text(json.dumps(dict(command=command, rc=rc, seconds=round(elapsed, 3)), indent=2) + '\n')
print(f'{label}: rc={rc} elapsed={elapsed:.3f}s', flush=True)
print((packet / 'receipts' / (label + '.log')).read_text(errors='replace')[-3500:])
sys.exit(rc)
