#!/usr/bin/env python3
"""Focused documentation and interface gates; excludes delegated full banks."""
import argparse
import json
import subprocess
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('--repo', type=Path, required=True)
p.add_argument('--packet', type=Path, required=True)
a = p.parse_args()
commands = [
    ['python3', '-B', 'docs/diagrams/submodule_boundaries.gen.py', '--check'],
    ['python3', '-B', 'docs/diagrams/submodule_boundaries.gen.py', '--selftest'],
    ['python3', '-B', 'scripts/check_submodule_docs.py'],
    ['python3', '-B', 'scripts/check_submodule_docs.py', '--selftest'],
    ['python3', '-B', 'scripts/docs_check.py'],
    ['python3', '-B', 'scripts/check_diagram_pngs.py'],
    ['python3', '-B', 'sw/mailbox/gen_mailbox.py', '--check'],
    ['python3', '-B', 'scripts/ci_events.py', '--check'],
    ['python3', '-B', 'scripts/check_em_dash.py', '--base', 'db9aa8c9b135b34ff3d070a979dee70440b37cc6'],
]
out = a.packet.resolve() / 'docs'
out.mkdir(exist_ok=True)
rows = []
for i, cmd in enumerate(commands):
    r = subprocess.run(cmd, cwd=a.repo, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    (out / f'{i:02d}.log').write_text(r.stdout)
    (out / f'{i:02d}.rc').write_text(str(r.returncode) + '\n')
    rows.append({'command': cmd, 'rc': r.returncode, 'log': f'docs/{i:02d}.log'})
    print(' '.join(cmd), 'rc=', r.returncode, flush=True)
(out / 'results.json').write_text(json.dumps(rows, indent=2) + '\n')
raise SystemExit(int(any(r['rc'] for r in rows)))
