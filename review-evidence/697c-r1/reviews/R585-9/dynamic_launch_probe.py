#!/usr/bin/env python3
"""Prove a named dynamic-code attribute can launch outside the helper."""
import argparse
import os
import subprocess
import sys
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument('root', type=Path)
ap.add_argument('scratch', type=Path)
args = ap.parse_args()
sys.dont_write_bytecode = True
module_dir = args.root.resolve() / 'sw/firmware/ctrl/test'
sys.path.insert(0, str(module_dir))
import ctrl_pin as p

texts = {f.relative_to(p.ROOT).as_posix(): f.read_text() for f in p.PROOF}
key = next(k for k in texts if k.endswith('ctrl_pin.py'))
payload = "import subprocess; subprocess.run([" + repr(sys.executable) + ", '-c', 'print(\"OUTSIDE_HELPER_PROCESS_RAN\")'], check=True)"
plant = '\nimport inspect\ninspect.builtins.exec(' + repr(payload) + ')\n'
texts[key] += plant
found = p.census(texts, p.git_env())
print('Planted code:', plant, flush=True)
print('Census findings:', found, flush=True)
args.scratch.mkdir(parents=True, exist_ok=True)
candidate = args.scratch / 'ctrl_pin_probe.py'
candidate.write_text(texts[key])
env = dict(os.environ, PYTHONPATH=str(module_dir), PYTHONDONTWRITEBYTECODE='1')
result = subprocess.run([sys.executable, '-B', str(candidate)], env=env,
                        capture_output=True, text=True, check=False, timeout=30)
print('Execution return code:', result.returncode)
print(result.stdout, end='')
print(result.stderr, end='')
assert result.returncode == 0 and 'OUTSIDE_HELPER_PROCESS_RAN' in result.stdout
if not found:
    print('REPRODUCED: explicit builtins.exec outside helper accepted and child process ran')
    sys.exit(1)
print('REFUSED: the census rejects the executable specimen')
