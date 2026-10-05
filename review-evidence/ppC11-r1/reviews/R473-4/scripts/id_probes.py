#!/usr/bin/env python3
"""Independent ID fixtures and three deliberately weakened scanner controls."""
import argparse
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile

p = argparse.ArgumentParser()
p.add_argument('--source', type=Path, required=True)
p.add_argument('--scratch', type=Path, required=True)
a = p.parse_args()
script = a.source / 'scripts/check-ids.py'
params = '''## 7. Parameter master table (F01.5)

| P-ID | Default |
|---|---|
| P-RX-SLOTS | 4 |
| P-TEST-ALPHA / P-TEST-BETA | 1 |
'''
timing = '''<a id="fig-08-constants"></a>**F08.1**

| T-ID | Value |
|---|---|
| T-ADP-DELAY | 0 |
| T-ADP-DELAY-START | 0 |
| T-NVM-RS-DEADLINE | 0 |
| T-NVM-RS-AGGREGATE | 0 |
| T-MRP-JOIN | 0 |
'''
cases = [
    ('T-ADP-DELAY(-START)', None),
    ('T-ADP-DELAY(-STRT)', 'T-ADP-DELAY-STRT'),
    ('P-RX-SLOTS-1', None),
    ('P-NO-BASE-1', 'P-NO-BASE-1'),
    ('P-RX-SLOTS-2', 'P-RX-SLOTS-2'),
    ('T-NVM-{RS-DEADLINE, RS-AGGREGATE}', None),
    ('T-NVM-{RS-DEADLINE, RS-AGGREGAT}', 'T-NVM-RS-AGGREGAT'),
    ('T-MRP-*', None),
    ('T-NOTHING-*', 'T-NOTHING-*'),
    ('P-TEST-ALPHA / -BETA', None),
    ('P-TEST-ALPHA / -BET', 'P-TEST-BET'),
    ('T-MRP-JOIN-driven', None),
    ('T-ADP-DELAY(-start)', 'T-ADP-DELAY(-...)'),
]
for leader in ['', '// ', '# ', '-- ', '* ', '; ', '> ']:
    for newline in ['\n', '\r\n']:
        gap = newline + leader
        cases.extend([
            ('T-ADP-' + gap + 'DELAY(-START)', None),
            ('T-ADP-' + gap + 'DELAY(-STRT)', 'T-ADP-DELAY-STRT'),
            ('T-ADP-DELAY(-' + gap + 'START)', None),
            ('T-ADP-DELAY(-' + gap + 'STRT)', 'T-ADP-DELAY-STRT'),
            ('T-ADP-' + gap + 'DELAY(-' + gap + 'START)', None),
            ('T-ADP-' + gap + 'DELAY(-' + gap + 'STRT)', 'T-ADP-DELAY-STRT'),
            ('T-ADP-' + gap + 'DELAY-' + gap + 'START', None),
        ])
failures = 0
with tempfile.TemporaryDirectory(dir=a.scratch, prefix='ids-') as temp:
    root = Path(temp)
    subprocess.run(['git', 'init', '-q', str(root)], check=True)
    for name, body in [('01_overview.md', params), ('08_timing.md', timing)]:
        path = root / 'docs/architecture' / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body)
    for number, (body, token) in enumerate(cases):
        rel = ['docs/probe.md', 'hdl/probe.sv', 'tb/probe.txt'][number % 3]
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body)
        r = subprocess.run([sys.executable, str(script), '--root', str(root)], text=True, capture_output=True)
        good = r.returncode == (1 if token else 0) and (token is None or token in r.stdout)
        print(json.dumps({'case': number + 1, 'file': rel, 'body': body, 'expected': token,
                          'rc': r.returncode, 'pass': good, 'stdout': r.stdout}))
        failures += not good
        path.unlink()
    # The root is a fixture only. The reviewed checkout is never edited.
    source = script.read_text()
    old = subprocess.check_output(['git', '-C', str(a.source), 'show',
                                  '80588cdc43ca5605a1d3748d13dd8ed7f22f7000:scripts/check-ids.py'], text=True)
    old_uses = old[old.index('def uses('):old.index('\ndef resolves(')]
    new_uses = source[source.index('def uses('):source.index('\ndef resolves(')]
    mutations = {
        'any-minus-one': source.replace('token.endswith("-1") and token[:-2] in rows', 'token.endswith("-1")'),
        'skip-broken-optional': source.replace('optional = OPTIONAL.match(text, end)',
            'optional = OPTIONAL.match(text, end)\n            if optional and "\\n" in optional.group(0):\n                continue'),
        'old-parser-new-selftest': source.replace(new_uses, old_uses),
    }
    for name, body in mutations.items():
        assert body != source
        mutant = root / (name + '.py')
        mutant.write_text(body)
        r = subprocess.run([sys.executable, str(mutant), '--selftest'], text=True, capture_output=True)
        good = r.returncode == 1 and 'SELFTEST FAIL:' in r.stdout
        print(json.dumps({'mutation': name, 'rc': r.returncode, 'killed': good, 'stdout': r.stdout}))
        failures += not good
print(f'Independent fixtures: {len(cases)}; scanner mutations: {len(mutations)}; failures: {failures}')
raise SystemExit(bool(failures))
