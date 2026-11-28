#!/usr/bin/env python3
"""Read-only review checks. Run from the candidate clone; outputs beside this script."""
import ast
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys

OUT = Path(__file__).resolve().parent
SCRATCH = OUT / 'scratch'
SCRATCH.mkdir(exist_ok=True)
HEAD = '4461d77ca34ec1203321821a3313071ff1923984'
EVIDENCE = '63ebbbacee3d6c366274d0b756f86433a7588a30'
PREFIX = 'review-evidence/977-r1/'
os.environ['GIT_NO_REPLACE_OBJECTS'] = '1'
sys.dont_write_bytecode = True

def git(*args):
    return subprocess.check_output(['git', *args])

def blob(path):
    return git('show', f'{EVIDENCE}:{PREFIX}{path}')

def save(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2) + '\n')

manifest = json.loads(blob('MANIFEST.json'))
selected = [r for r in manifest if r['file'].startswith('author-r13/') or
            r['file'] in ('author-r10/receipts/SUPERSESSION-NOTE.md',
                          'author-r11/receipts/SUPERSESSION-NOTE.md')]
verified = []
for entry in selected:
    data = blob(entry['file'])
    digest = hashlib.sha256(data).hexdigest()
    assert digest == entry['published_sha256'], entry['file']
    p = SCRATCH / entry['file']
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data)
    verified.append({'path': entry['file'], 'bytes': len(data), 'sha256': digest})
lookup = {r['file']: r for r in manifest}
note_paths = []
for version in ('r10', 'r11'):
    note = blob(f'author-{version}/receipts/SUPERSESSION-NOTE.md').decode()
    for relative in re.findall(r'^\| `[^`]+\.gz` \| `([^`]+)` \|$', note, re.M):
        path = f'author-{version}/receipts/{relative}'
        digest = hashlib.sha256(blob(path)).hexdigest()
        assert digest == lookup[path]['published_sha256']
        note_paths.append({'path': path, 'sha256': digest})
save('supersession-links.json', note_paths)
save('packet-integrity.json', {'commit': EVIDENCE, 'verified': verified,
    'commit_has_signature': b'\ngpgsig ' in git('cat-file', 'commit', EVIDENCE),
    'scope': 'Current author packet and both supersession notes; no reviewer reports read.'})

identity = blob('author-r13/receipts/elf-identity-4461d77c.txt').decode()
sections = {}
section = None
for line in identity.splitlines():
    if line.startswith('## '):
        section = line[3:]
        sections[section] = {}
    match = re.fullmatch(r'([0-9a-f]{64})  (.+)', line)
    if match:
        assert match[2] not in sections[section]
        sections[section][match[2]] = match[1]
assert len(sections['4461d77c']) == len(sections['25ff0632']) == 80
assert sections['4461d77c'] == sections['25ff0632']
save('elf-identity-audit.json', {'result': '80/80 matching path and SHA-256 pairs',
    'harness_paths': sum(not p.startswith('./ledger/') for p in sections['4461d77c']),
    'platform_paths': sum(p.startswith('./ledger/') for p in sections['4461d77c']),
    'pairs': sections['4461d77c'],
    'limit': 'Verified published build receipt, not a new build or direct comparison of unavailable ELF files.'})

measurement = {}
for point in ('1x1', '8x8-1if'):
    text = blob(f'author-r13/receipts/meas/deliv13-{point}-e59cf6ea.txt').decode()
    rows = re.findall(r'^(\S+) (\S+) commit (\d+): window (\d+) passes, (\d+) ordinary passes.*$', text, re.M)
    aliases = re.findall(r'^(\S+) (\S+): transmit-only alias of commit (\d+), excluded$', text, re.M)
    assert len(rows) == len({(r[0], r[2]) for r in rows}) == 44
    assert len(aliases) == 6 and all('srp.register_tx.' in r[1] for r in aliases)
    assert all(int(r[4]) > 0 for r in rows)
    assert len({r[0] for r in rows}) == 20
    old = blob(f'author-r12/receipts/meas/deliv-{point}-e59cf6ea.txt').decode()
    dearest = [s for s in text.splitlines() if s.startswith('DEAREST')]
    previous = [s for s in old.splitlines() if s.startswith('DEAREST')]
    assert dearest == previous
    for label in ('after', 'before 50 ms', 'before 500 ms'):
        shares = [int(v.replace(',', '')) for v in re.findall(
            re.escape(label) + r' [\d,]+: ([\d,]+) a sink', text)]
        expected = next(s for s in dearest if f'over the {label} base:' in s)
        maximum = int(re.search(r'base: ([\d,]+) cycles', expected)[1].replace(',', ''))
        assert len(shares) == 44 and max(shares) == maximum
    p = SCRATCH / f'deliv12-{point}.txt'
    p.write_text(old)
    measurement[point] = {'record_count': len(rows), 'distinct_group_commits': len({(r[0], r[2]) for r in rows}),
        'group_count': len({r[0] for r in rows}), 'aliases': aliases,
        'dearest': dearest, 'previous_dearest': previous,
        'per_record_printed_maxima': 'all three maxima recomputed from 44 rows and unchanged',
        'rows': rows}
save('extraction-receipt-audit.json', measurement)

script = blob('author-r13/receipts/deliv13.py.txt').decode()
module = type(sys)('extractor')
exec(compile(script, 'published-deliv13.py', 'exec'), module.__dict__)
assert module.selftest() == 0
names = ['srp.register_burst.t0.r%d.if0' % i for i in range(3)]
alias = 'srp.register_tx.t0.if0'
commits = [10000, 20000, 30000]
rxc = [(c, 4, n) for c, n in zip(commits, names)]
starts = dict(zip(names, commits)) | {alias: 30000}
records, aliases = module.records(names + [alias], rxc, starts, 4)
assert records == list(zip(names, commits)) and aliases == [alias]
bases = [(s, 600 if 32000 <= s <= 48000 else 100) for s in range(0, 1000000, 4000)]
shares = [module.measure(bases, c, 2)['share']['after'] for _, c in records]
assert shares == [0, 500, 1250]
old_records = [(n, 10000) for n in names]
old_shares = [module.measure(bases, c, 2)['share']['after'] for _, c in old_records]
assert old_shares == [0, 0, 0] and old_shares != shares
refusals = {}
for label, bad_rx, bad_starts in [
        ('missing', rxc[:2], starts),
        ('duplicate', rxc + [rxc[1]], starts),
        ('wrong channel', rxc[:2] + [(30000, 1, names[2])], starts),
        ('mismatched start', rxc, starts | {names[1]: 21000})]:
    try:
        module.records(names + [alias], bad_rx, bad_starts, 4)
    except module.Refused as e:
        refusals[label] = str(e)
    else:
        raise AssertionError(label)
assert module.measure(bases[:5], 10000, 2) is None
save('extractor-probe.json', {'commits': commits, 'shares': shares, 'old_rule_shares': old_shares,
    'refusals': refusals, 'truncated_window': 'unmeasured', 'result': 'PASS'})

sys.path.insert(0, str(Path('tb/verilator/ctrl_service_budget').resolve()))
import load_grade
import flip_grade
from unittest.mock import patch
loads = {p: sum(load_grade.load(load_grade.ROOT, p, flip_grade.COLUMN).values()) for p in ('1x1/1if', '8x8/1if')}
assert abs(loads['8x8/1if'] - 0.78214) < 0.000005
refused = flip_grade.findings(load_grade.ROOT, ceiling={'8x8/1if': 0.77})
assert refused and not flip_grade.findings(load_grade.ROOT, ceiling={'8x8/1if': 0.79})
floors = {}
for point, cost in [('1x1/1if', 195), ('8x8/1if', 155)]:
    with patch.dict(load_grade.DELIVERY_US, {point: cost}):
        floors[point] = load_grade.delivery_findings(load_grade.ROOT)
        assert any('under its measurement' in x for x in floors[point])
assert not flip_grade.over(.790, .79) and flip_grade.over(.791, .79)
save('model-probe.json', {'loads': loads, 'at_authorized_ceiling': refused, 'lowered_floors': floors,
    'edge_0790': 'within 0.79', 'edge_0791': 'over 0.79', 'result': 'PASS; owner decision still open'})

paths = git('diff', '--name-only', '3256d1d2', HEAD).decode().splitlines()
asts = {}
for path in paths:
    if path.endswith('.py'):
        old = ast.dump(ast.parse(git('show', '3256d1d2:' + path).decode()))
        new = ast.dump(ast.parse(Path(path).read_text()))
        # Docstrings are intentionally changed; compare after removing all standalone strings.
        def executable(data):
            tree = ast.parse(data)
            class Strip(ast.NodeTransformer):
                def visit_Expr(self, node):
                    return None if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str) else node
            return ast.dump(Strip().visit(tree))
        asts[path] = executable(git('show', '3256d1d2:' + path).decode()) == executable(Path(path).read_text())
        assert asts[path]
assert not git('diff', '--name-only', '3256d1d2', HEAD, '--', 'sw/firmware', 'hdl', 'third_party', 'protocol-processor', 'gptp-processor')
patch_bytes = git('diff', HEAD + '^', HEAD)
check = subprocess.run(['git', 'apply', '-R', '--check'], input=patch_bytes, capture_output=True)
assert check.returncode == 0
save('delta-audit.json', {'head': HEAD, 'tree': git('rev-parse', HEAD + '^{tree}').decode().strip(),
    'source_base': git('rev-parse', 'origin/dev-soft-core').decode().strip(),
    'changed_paths': paths, 'unchanged_executable_python': asts,
    'firmware_rtl_submodules_delta': 'empty', 'last_commit_reverse_apply_check': check.returncode,
    'last_commit_parent': git('rev-parse', HEAD + '^').decode().strip()})
print('Packet, ELF receipt, extraction, synthetic fault, model, delta and reverse-apply checks PASS')
