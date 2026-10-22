#!/usr/bin/env python3
"""Verify the public author receipts directly from their immutable Git tree.
Usage: audit_evidence.py REPO
No checkout changes and no reviewer reports are read.
"""
import hashlib
import json
import subprocess
import sys

repo = sys.argv[1]
commit = 'b6d9eaa187cb2c43548e22e7adae21b35b539107'
prefix = 'review-evidence/771-r1/'
def show(path):
    return subprocess.check_output(['git', '-C', repo, 'show', commit + ':' + prefix + path])
manifest = json.loads(show('MANIFEST.json'))
counts = {}
for item in manifest:
    path = item['file']
    if not path.startswith(('author/', 'author-r2/')):
        continue
    data = show(path)
    digest = hashlib.sha256(data).hexdigest()
    assert digest == item['published_sha256'], path
    group = path.split('/')[0]
    counts[group] = counts.get(group, 0) + 1
print('Public archive:', commit)
print('Published SHA-256 receipts verified:', json.dumps(counts, sort_keys=True))
print('Original hashes are not substituted for hashes of redacted publication bytes.')
log = show('author-r2/round2/firmware-gates/text/ctrl_firmware.log')
print('Text firmware log:', len(log), 'bytes; sha256', hashlib.sha256(log).hexdigest())
import re
text = log.decode()
tallies = re.findall(r'^\s*== .*checks: (\d+)\s+failures: (\d+) ==$', text, re.M)
print('Firmware arm tallies:', len(tallies), 'checks:', sum(int(a) for a,b in tallies), 'failures:', sum(int(b) for a,b in tallies))
for line in text.splitlines():
    if any(x in line for x in ('mutants: ', 'acmp-kind-lost (', 'acmp-kind-not-notified (', 'test_ctrl_firmware:')):
        print(line)
assert len(tallies) == 66 and sum(int(a) for a,b in tallies) == 1593 and not any(int(b) for a,b in tallies)
assert 'mutants: 521 of 521 caught' in text and 'test_ctrl_firmware: PASS' in text
for name in ('fw_rv32_selftest','tally_selftest_mutants','ctrl_firmware','ctrl_firmware_shards','ctrl_nvm','fw_coverage_selftest','fw_coverage_check','ctrl_boundary_litex'):
    rc = show('author-r2/round2/firmware-gates/' + name + '.rc').decode().strip()
    print(name, 'rc=' + rc)
    assert rc == '0'
for name in ('ctrl_boundary','firmware_census'):
    print('Disclosed earlier/non-assigned run:', name, 'rc=' + show('author-r2/round2/firmware-gates/' + name + '.rc').decode().strip())
assert show('author-r2/round2/firmware-gates/firmware_census.log') == show('author-r2/round2/firmware-gates/firmware_census_dev_inputs.log')
print('Census head/base archived outputs byte-identical.')
commit_text = subprocess.check_output(['git', '-C', repo, 'cat-file', 'commit', commit]).decode()
print('Archive commit signature header present:', '\ngpgsig ' in commit_text)
