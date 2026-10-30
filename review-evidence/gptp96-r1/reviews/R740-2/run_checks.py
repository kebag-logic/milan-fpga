#!/usr/bin/env python3
"""Focused documentation review probes; usage: run_checks.py CHECKOUT [LINT_DIR]."""
import concurrent.futures
import io
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tarfile

PACKET = Path(__file__).resolve().parent
REPO = Path(sys.argv[1]).resolve()
HEAD = '806957b35c3c23a36505744d205f9692720d19e2'
assert subprocess.check_output(['git', '-C', str(REPO), 'rev-parse', 'HEAD'], text=True).strip() == HEAD
SCRATCH = PACKET / 'scratch'
SCRATCH.mkdir(exist_ok=True)
ENV = dict(os.environ, TMPDIR=str(SCRATCH), PYTHONDONTWRITEBYTECODE='1')
if len(sys.argv) > 2:
    ENV['PATH'] = sys.argv[2] + os.pathsep + ENV['PATH']

def run(name, cwd, command, expect=0, diagnostic=None):
    result = subprocess.run(command, cwd=cwd, env=ENV, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, text=True, timeout=300)
    (PACKET / (name + '.log')).write_text(result.stdout)
    (PACKET / (name + '.rc')).write_text(str(result.returncode) + '\n')
    ok = (result.returncode == expect if expect == 0 else result.returncode != 0)
    if diagnostic:
        ok = ok and diagnostic in result.stdout
    return dict(name=name, command=command, rc=result.returncode,
                expected='zero' if expect == 0 else 'nonzero', diagnostic=diagnostic, passed=ok)

archive = subprocess.check_output(['git', '-C', str(REPO), 'archive', HEAD])
def fresh(name):
    root = SCRATCH / name
    root.mkdir(exist_ok=False)
    with tarfile.open(fileobj=io.BytesIO(archive)) as tf:
        tf.extractall(root, filter='data')
    return root

def probe(name, rel, old, new, diagnostic):
    root = fresh(name)
    file = root / rel
    original = file.read_text()
    assert original.count(old) == 1, (name, old, original.count(old))
    file.write_text(original.replace(old, new))
    return run(name, root, ['make', '-j16', 'docs'], 1, diagnostic)

rows = [
    ('probe-stale', 'docs/INTEGRATION.md', '| `SYNC_RTO_MS_C` | 375 |',
     '| `SYNC_RTO_MS_C` | 376 |', 'SYNC_RTO_MS_C is 376'),
    ('probe-bold-stale', 'docs/INTEGRATION.md', '| `SYNC_RTO_MS_C` | 375 |',
     '| `SYNC_RTO_MS_C` | **376** |', "SYNC_RTO_MS_C value '**376**'"),
    ('probe-negative', 'docs/INTEGRATION.md', '| `SYNC_RTO_MS_C` | 375 |',
     '| `SYNC_RTO_MS_C` | -1 |', "SYNC_RTO_MS_C value '-1'"),
    ('probe-unit-copy', 'docs/HDL_DEVELOPER.md',
     'Every usable Sync pair restarts it, in either role.',
     'Every usable Sync pair restarts it, in either role.\n\nThat watch lasts 375 ms.',
     "'375 ms' restates SYNC_RTO_MS_C"),
    ('probe-converted-copy', 'docs/INTEGRATION.md',
     '| Link-up | [`STEP_LINKUP_NS_C`](#protocol-constants) |',
     '| Link-up | 20 us |', "'20 us' restates STEP_LINKUP_NS_C"),
    ('probe-broken-rom', 'docs/MANAGER.md', '| Shipping | 1,022 of 1,024 | 2 |',
     '| Shipping | **1,021** of 1,024 | 3 |', "Shipping row '**1,021** of 1,024'"),
    ('probe-duplicate-rom', 'docs/MANAGER.md', '| Shipping | 1,022 of 1,024 | 2 |',
     '| Shipping | 1,022 of 1,024 | 2 |\n| Shipping | 1,022 of 1,024 | 2 |',
     'duplicate ROM budget row: Shipping'),
]

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    futures = [pool.submit(run, name, REPO, command) for name, command in [
        ('docs', ['make', '-j16', 'docs']),
        ('contract', ['make', '-j16', 'contract']),
        ('lint', ['make', '-j16', 'lint']),
        ('diff-check', ['git', 'diff', '--check', '135afd04..' + HEAD]),
    ]]
    futures += [pool.submit(probe, *row) for row in rows]
    results = [future.result() for future in futures]

# Each of the seventeen canonical constants must independently be tied to source.
root = fresh('each-constant')
file = root / 'docs/INTEGRATION.md'
original = file.read_text()
section = original.split('## Protocol constants\n', 1)[1].split('\n## ', 1)[0]
matches = re.findall(r'^\| `([A-Z][A-Z0-9_]*)` \| ([0-9,]+) \|', section, re.M)
assert len(matches) == 17
for name, value in matches:
    old = f'| `{name}` | {value} |'
    new = f'| `{name}` | {int(value.replace(",", "")) + 1} |'
    file.write_text(original.replace(old, new, 1))
    results.append(run('constant-' + name, root, [sys.executable, '-B', 'scripts/check_docs.py'], 1, name + ' is '))
file.write_text(original)
results.append(run('restored-control', root, ['make', '-j16', 'docs']))
(PACKET / 'checks.json').write_text(json.dumps(results, indent=2) + '\n')
for result in results:
    print(result['name'], 'rc=' + str(result['rc']), 'PASS' if result['passed'] else 'FAIL')
sys.exit(0 if all(result['passed'] for result in results) else 1)
