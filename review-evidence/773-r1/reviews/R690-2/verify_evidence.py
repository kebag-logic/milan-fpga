#!/usr/bin/env python3
"""Verify public #773 evidence objects and aggregate receipts without executing banks.

Usage: python3 verify_evidence.py REPO OUTPUT_DIRECTORY
Requires the named evidence commit in REPO's object database.
"""
from collections import Counter
from pathlib import Path
import hashlib
import json
import os
import re
import subprocess
import sys

repo = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]).resolve()
ref = '1faf10a1331f93451a6aa4e43956a51de6ab4da3'
head = '1b47a3dcff0cb65cb5cebe1f86327429a76f775d'
tree = 'f608aefd73bbc007624782653182d0a6f85c8825'
base = 'review-evidence/773-r1/'
os.environ['GIT_NO_REPLACE_OBJECTS'] = '1'
def git(*args):
    return subprocess.check_output(['git', '-C', str(repo), *args])
def get(name):
    return git('show', ref + ':' + base + name)

manifest = json.loads(get('MANIFEST.json'))
selected = {}
for entry in manifest:
    name = entry['file']
    if name.startswith('author-r2/receipts/round2/') or name == 'author-r2/PR-BODY.md':
        data = get(name)
        assert hashlib.sha256(data).hexdigest() == entry['published_sha256'], name
        selected[name] = data
        target = out / 'public' / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
print('Published evidence commit:', ref)
print('Git signature status:', git('log', '-1', '--format=%G?', ref).decode().strip(), '(N means unsigned)')
print('Verified published SHA-256 hashes:', len(selected))
print('Hashes verify published bytes, including declared path redactions; no signer attestation is asserted.')
pre = 'author-r2/receipts/round2/'
def txt(name):
    return selected[pre + name].decode()

seen = []
total = 0
for shard in range(4):
    key = f'sweep/shard-{shard}/'
    result = json.loads(txt(key + 'results.json'))
    assert result['head'] == head
    assert len(result['results']) == 1
    run = result['results'][0]
    assert run['exit_code'] == 0 and run['command'][-2:] == ['--shard', f'{shard}/4']
    identity = txt(key + 'clone_identity.txt')
    assert head in identity and tree in identity
    runner = txt(key + 'runner.txt')
    suites = re.findall(r'^PASS\s+(\S+)$', runner, re.M)
    assert not re.search(r'^(FAIL|TIMEOUT|UNKNOWN)\s', runner, re.M)
    n, passed, failed, timed = map(int, re.search(r'suites:\s+(\d+)\s+passed:\s+(\d+)\s+failed:\s+(\d+)\s+timed out:\s+(\d+)', runner).groups())
    checks, failures = map(int, re.search(r'checks:\s+(\d+)\s+in-suite failures:\s+(\d+)', runner).groups())
    assert n == passed == len(suites) and failed == timed == failures == 0
    seen.extend(suites)
    total += checks
    print(f'Shard {shard}: head/tree bound, command --shard {shard}/4, rc 0, {n}/{n}, {checks} checks; '+re.search(r'tracked changes: \d+', identity).group())
listed = subprocess.check_output(['bash', 'scripts/run_all_suites.sh', '--list'], cwd=repo, text=True).split()
assert Counter(seen) == Counter(listed) and len(seen) == len(set(seen)) == 64
assert total == 2190887
print('PASS: 64/64 unique suites equal current --list; 2190887 checks, zero reported in-suite failures')
print('Shard 0 post-run count is 2. The driver documents regeneration of two TEST_RESULTS files; the receipt does not identify its changed paths. This is a provenance limit, not evidence of an RTL change.')
assert txt('gates/behave.rc').strip() == '0'
assert '406 scenarios passed, 0 failed, 0 skipped' in txt('gates/behave.log')
assert head in txt('gates/behave.log')
assert txt('gates/lint.rc').strip() == '0' and head in txt('gates/lint.log') and tree in txt('gates/lint.log')
print('PASS: behave 406/406 and lint rc 0 at the requested head')
docs = json.loads(txt('docs/all.receipts.json'))
assert docs['head'] == docs['head_after'] == head
counts = Counter(str(x.get('rc')) for x in docs['steps'])
print('Docs receipt rc distribution:', dict(counts))
bad = [x for x in docs['steps'] if x.get('rc') not in (0, None)]
assert len(bad) == 1 and bad[0]['id'] == 'gate_8'
print('Docs initial gate_8 rc 128 is explicitly superseded by the direct-base receipt:')
print(txt('docs/gate_8_em_dash_direct.txt'))
assert txt('gates/docs_named.log').count('rc=0') == 3
print('PASS: three named docs gates rc 0; GNU Make 4.3 recorded')
path = 'hdl/ieee1722/crf/KL_media_domain_event.sv'
old = git('show', '13d8f1e8:' + path).decode()
new = git('show', head + ':' + path).decode()
def strip(s):
    return re.sub(r'/\*.*?\*/|//[^\n]*', '', s, flags=re.S)
assert strip(old) == strip(new)
changes = git('diff', '--name-only', '13d8f1e8', head).decode().splitlines()
assert set(changes) == {path, 'docs/design/MEDIA_CLOCK_FOLLOWING.md', 'docs/reference/MILAN_COMPLIANCE_MATRIX.md'}
print('PASS: exact comment-stripped equality; only two documentation pages and that comment changed')
print('Non-comment SHA-256:', hashlib.sha256(strip(new).encode()).hexdigest())
