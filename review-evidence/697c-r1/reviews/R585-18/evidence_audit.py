#!/usr/bin/env python3
"""Check public receipt populations against source and publication digests."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

packet = Path(__file__).resolve().parent
root = Path.cwd()
sys.path.insert(0, str(root / 'sw/firmware/ctrl/test'))
import ctrl_mutants
import aecp_mutants
import srp_mutants
import srp_pub_mutants

pub = packet / 'public'
manifest = {x['file']: x for x in json.loads((packet / 'published-manifest-selected.json').read_text())}
sources = json.loads((packet / 'public-sources.json').read_text())
for x in sources:
    data = (pub / x['path']).read_bytes()
    assert hashlib.sha256(data).hexdigest() == manifest['author-r19/' + x['path']]['published_sha256']
    assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == x['git_blob']
print('publication SHA-256 and Git blob verification:', len(sources), 'files')

dev = (pub / 'round19/images-dev.json').read_bytes()
head = (pub / 'round19/images-head.json').read_bytes()
assert dev == head
images = json.loads(head)
assert len(images) == 65 and len({r['path'] for r in images}) == 65
assert hashlib.sha256(head).hexdigest() == '96f55deba3b69b224fb838b746f559b3c944b552c694cef3211470d8b11db584'
print('public image manifests: 65/65 identical, five standalone plus 30 flat and 30 split')

cont = pub / 'round19-continuation'
lines = (cont / 'firmware-verdicts.txt').read_text().splitlines()
assert len(lines) == 915 and all(line.startswith('[ok] ') for line in lines)
names = Counter()
for line in lines:
    m = re.match(r'\[ok\] mutant ([^ ]+) ', line) or re.match(r'\[ok\] ([^ :]+):', line)
    if m:
        names[m[1]] += 1
one_if = tuple(d for d in srp_mutants.DEFECTS if d.name.startswith((
    'four-way-', 'binding-', 'feedback-', 'r10-', 'p11-', 'srp-bound-', 'srp-term-',
    'srp-poll-extra', 'srp-send-extra', *srp_pub_mutants.ROUND5)))
expected = Counter(d.name for table in (ctrl_mutants.MUTANTS, aecp_mutants.DEFECTS,
                                       srp_mutants.DEFECTS, one_if) for d in table)
assert names == expected, (expected - names, names - expected)
assert sum(line.startswith('[ok] arm ') for line in lines) == 60
assert sum(line.startswith('[ok] lwSRP pin,') for line in lines) == 2
print('firmware public verdict multiset matches source:', len(ctrl_mutants.MUTANTS),
      len(aecp_mutants.DEFECTS), len(srp_mutants.DEFECTS), len(one_if), '+ 60 arms + 2 pin controls = 915')

def coverage(name):
    text = (cont / 'logs' / name).read_text()
    rows = [l for l in text.splitlines() if re.match(r'(sw/|third_party/)', l)]
    assert len(rows) == 30 and all('lines 100.00 %  branches 100.00 %' in l for l in rows)
    moves = {'sw/firmware/ctrl/' + core + '/' + core + '.c':
             'third_party/tsn-c-stack/src/' + core + '.c' for core in ('adp', 'acmp', 'maap')}
    moves['sw/firmware/ctrl/wire/wire.h'] = 'third_party/tsn-c-stack/include/wire.h'
    # The task moves exactly these four covered files. Preserve every numerator,
    # denominator and percentage; normalize only their reviewed path relocation.
    normalized = []
    for row in rows:
        fields = row.split()
        fields[0] = moves.get(fields[0], fields[0])
        normalized.append(tuple(fields))
    return sorted(normalized)
assert coverage('coverage.log') == coverage('coverage-dev.log')
print('coverage tables: 30 identical rows, 100% after unchanged exclusions')
for name in ('ctrl_build.py', 'ctrl_pin.py', 'ctrl_pin_env.py', 'ctrl_pin_store.py'):
    path = 'sw/firmware/ctrl/test/' + name
    assert subprocess.check_output(['git', 'show', '27ee16b5:' + path]) == (root / path).read_bytes()
print('pin proof and all pin-control modules: byte-identical to reviewed baseline')
for name in ('hook312.log', 'hook314.log'):
    text = (cont / 'logs' / name).read_text()
    caught = re.findall(r'^CAUGHT\s+H(\d+) ', text, re.M)
    assert sorted(map(int, caught)) == list(range(1, 25)), caught
    print(name, 'H1-H24 caught once each')
print('public receipt audit: PASS')
