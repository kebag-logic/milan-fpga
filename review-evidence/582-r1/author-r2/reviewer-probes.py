"""Run the assigned packet substitutions against this lane and restore bytes.

Packet scripts stay read-only. Only their data definitions are loaded; their
copy/checkout loops are replaced by a finally-restored single-file edit.
The ROM substitutions run the new bank test, as the assignment requires.
"""
import ast
import hashlib
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
from unittest.mock import patch

ROOT = Path.cwd().resolve()
OUT = Path(__file__).resolve().parent
PACKETS = Path('$REVIEWS')
PY = sys.executable
results = []


def definitions(path, argv, stop=None):
    with patch.object(sys, 'argv', argv):
        if stop is None:
            return runpy.run_path(str(path))
        tree = ast.parse(path.read_text(), filename=str(path))
        body = []
        for node in tree.body:
            if isinstance(node, ast.Assign) and any(
                    isinstance(target, ast.Name) and target.id == stop for target in node.targets):
                break
            body.append(node)
        tree.body = body
        namespace = {'__file__': str(path), '__name__': 'packet_definitions'}
        exec(compile(tree, str(path), 'exec'), namespace)
        return namespace


def check_case(mid, rel, old, new, command, cwd, reason, control=False):
    path = ROOT / rel
    before = path.read_bytes()
    source = before.decode()
    assert source.count(old) == 1, (mid, source.count(old))
    with tempfile.TemporaryDirectory(prefix='582-mutation-cache-') as cache:
        try:
            path.write_text(source.replace(old, new))
            proc = subprocess.run(command, cwd=ROOT / cwd, text=True, capture_output=True,
                                  env=dict(os.environ, PYTHONPYCACHEPREFIX=cache), timeout=1800)
        finally:
            path.write_bytes(before)
    assert path.read_bytes() == before
    output = proc.stdout + proc.stderr
    passed = proc.returncode == 0 if control else proc.returncode != 0 and reason in output
    status = ('CONTROL-PASS' if control else 'KILLED') if passed else 'FAILED'
    print(f'{status} {mid}: rc {proc.returncode}; {output.strip().splitlines()[-1:]}', flush=True)
    log = OUT / 'probes' / f'{mid}.log'
    log.parent.mkdir(exist_ok=True)
    encoded = output.encode()
    assert len(encoded) <= 200_000, 'keep oversized evidence outside the packet'
    log.write_bytes(encoded)
    results.append(dict(probe=mid, status=status, returncode=proc.returncode,
                        command=command, cwd=str(ROOT / cwd), log=str(log.relative_to(OUT)),
                        sha256=hashlib.sha256(encoded).hexdigest(), size=len(encoded)))
    (OUT / 'probe-results.json').write_text(json.dumps(results, indent=2) + '\n')
    assert passed, (mid, output[-4000:])


r355 = definitions(PACKETS / '582-r355-1-packet/scripts/30_mutants.py',
                   ['30_mutants.py', str(ROOT), str(ROOT), PY], stop='results')
selected = {'C0', 'C1', 'C2', 'C3', 'B3', 'S1', 'S2', 'S3', 'S4'}
for mid, rel, old, new, command, cwd in r355['MUTANTS']:
    code = mid.split()[0]
    if code in selected:
        reason = 'accepted invalid input' if code == 'B3' else 'clock accepted before platform'
        check_case('R355-' + code, rel, old, new, command, cwd, reason, code.startswith('C'))

r354 = definitions(PACKETS / '582-r354-1-packet/scripts/mutants.py',
                   ['mutants.py', str(ROOT), PY])
rom_command = [PY, '-c', 'import test_clock_contract as t; t.test_gptp_rom_clock()']
for mid, rel, old, new, (command, cwd) in r354['MUTANTS']:
    if mid == 'M21-rom-clock-not-forwarded':
        check_case('R354-M21-control', rel, old, old, rom_command, cwd, '', True)
        check_case('R354-M21', rel, old, new, rom_command, cwd, 'gPTP ROM does not use configured Milan clock')
    elif mid.startswith(('M16-', 'M17-', 'M18-')):
        check_case('R354-' + mid.split('-')[0], rel, old, new, command, cwd,
                   'configuration clock pairs not preserved')

probe36 = ast.parse((PACKETS / '582-r355-1-packet/scripts/36_rom_clock_replay.py').read_text())
constants = {}
for node in probe36.body:
    if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
        if node.targets[0].id in ('REL', 'OLD', 'NEW'):
            constants[node.targets[0].id] = ast.literal_eval(node.value)
check_case('R355-probe36', constants['REL'], constants['OLD'], constants['NEW'],
           rom_command, 'sw/builder', 'gPTP ROM does not use configured Milan clock')
print('PASS: assigned reviewer mutations killed, controls passed, edited sources restored')
