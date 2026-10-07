#!/usr/bin/env python3
"""Replay the focused review checks in foreground, with at most 16 build jobs."""
import argparse
from pathlib import Path
import subprocess
import sys

p = argparse.ArgumentParser()
p.add_argument('--repo', type=Path, required=True)
p.add_argument('--sim', required=True)
a = p.parse_args()
root = a.repo.resolve()
packet = Path(__file__).resolve().parents[1]
scripts = packet / 'scripts'
scratch = packet / 'scratch'
def record(name, argv):
    subprocess.run([sys.executable, str(scripts / 'record.py'), name, *argv],
                   cwd=root, check=True)

record('initial-integrity', [sys.executable, str(scripts / 'verify_tree.py')])
record('capture-build', ['make', '-j16', '-C', 'tb/verilator/chmap_capture', 'build',
                        f'VERILATOR={a.sim}', 'VERILATOR_JOBS=16', f'MDIR={scratch}/capture'])
record('capture-run', [str(scratch / 'capture/Vchmap_wrap')])
record('held-mutants', ['env', f'VERILATOR={a.sim}', 'PYTHONDONTWRITEBYTECODE=1',
                        sys.executable, 'tb/verilator/follow_ring/mutants.py', '--jobs', '1',
                        '--mdir', str(scratch / 'mutants'), '--select', 'HELD-DUP', 'STARVED-HELD-DUP'])
subprocess.run([sys.executable, str(scripts / 'hold_expiry_probe.py'), '--root', str(root),
                '--sim', a.sim], cwd=root, check=True)
record('controller', [sys.executable, '-B', 'tb/verilator/follow_ring/settle_control.py',
                      '--sim', a.sim, '--out', str(scratch / 'controller'), '--jobs', '1'])
record('traceability', [sys.executable, '-B', 'docs/traceability/gen_module_matrix.py', '--check'])
record('doc-style', [sys.executable, '-B', 'scripts/check_doc_style.py'])
record('public-audit', [sys.executable, str(scripts / 'audit_evidence.py'), '--repo', str(root), '--sim', a.sim])
record('final-integrity', [sys.executable, str(scripts / 'verify_tree.py')])
