#!/usr/bin/env python3
"""Disposable mutation probe: replace one unique text span, run a target, restore exact bytes.

Usage: mutate_probe.py <file> <before> <after> -- <command...>
Prints the command's exit code; exits 0 only when the mutant was DETECTED (command nonzero)
and the original bytes and mode were restored (blob id equals HEAD's).
"""
import os
import subprocess
import sys
from pathlib import Path

path, before, after = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
cmd = sys.argv[sys.argv.index('--') + 1:]
original = path.read_bytes()
mode = path.stat().st_mode
text = original.decode()
if text.count(before) != 1:
    raise SystemExit(f'anchor not unique in {path}: {before!r} x{text.count(before)}')
try:
    path.write_bytes(text.replace(before, after).encode())
    print(f'mutant applied to {path}: {before!r} -> {after!r}', flush=True)
    rc = subprocess.run(cmd).returncode
finally:
    path.write_bytes(original)
    os.chmod(path, mode)
blob = subprocess.run(['git', 'hash-object', str(path)], capture_output=True, text=True).stdout.strip()
head = subprocess.run(['git', 'rev-parse', f'HEAD:{path}'], capture_output=True, text=True).stdout.strip()
print(f'command exit={rc}; restored blob {blob} HEAD blob {head} match={blob == head}')
sys.exit(0 if (rc != 0 and blob == head) else 1)
