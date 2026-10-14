#!/usr/bin/env python3
"""Execute the exact sweep preflight functions without executing any suite."""
import os, subprocess, sys
from pathlib import Path
repo = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parents[1]
text = (repo / 'scripts/run_all_suites.sh').read_text()
start = text.index('preflight() {')
end = text.index('\n#! the sweep itself:', start)
body = text[start:end]
assert 'act_ci.py' not in body
out = packet / 'receipts/serial-preflight'
out.mkdir(exist_ok=True)
program = 'set -u\nROOT="$1"\nOUT="$2"\n' + body + '\nprepare_logs\nrun_preflight_gates\necho "serial preflight: PASS; suites not invoked"\n'
script = packet / 'scratch/preflight-only.sh'
script.write_text(program)
print('Executing exact preflight(), prepare_logs(), run_preflight_gates() definitions from scripts/run_all_suites.sh', flush=True)
sys.exit(subprocess.run(['bash', str(script), str(repo), str(out)], cwd=repo).returncode)
