#!/usr/bin/env python3
"""Reproduce summary/cycles.md with the packet's summ_b19.py on a disposable
copy, then plant a late recovery to show the 5 s grade can fail.
Usage: probe_summ_b19.py <copy-of-author-dir> <published-author-dir>"""
import json, subprocess, sys
from pathlib import Path
root, pub = Path(sys.argv[1]), Path(sys.argv[2])
tool = root / 'tools' / 'summ_b19.py'
def run():
    subprocess.run([sys.executable, '-I', str(tool)], capture_output=True, check=True)
    return (root / 'summary' / 'cycles.md').read_text()
base = run()
print('cycles.md reproduced byte-identical:', base == (pub / 'summary' / 'cycles.md').read_text())
print('correlation.json reproduced equal:', json.loads((root / 'summary' / 'correlation.json').read_text()) == json.loads((pub / 'summary' / 'correlation.json').read_text()))
p = root / 'bench' / 'cycle05' / 'correlation.json'
orig = p.read_text(); c = json.loads(orig)
for e in c['edges']['tu']:
    if str(e['to']) == '0': e['last_before'] += 5.0; e['first_after'] += 5.0
p.write_text(json.dumps(c))
mut = run()
print('mutant (cycle 5 tu clear +5 s):', [l for l in mut.splitlines() if l.startswith('| 5 |')][0])
p.write_text(orig)
print('restored equal:', run() == base)
