#!/usr/bin/env python3
"""Verify the published evidence bytes and enumerate the reviewed test sources."""
import collections
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
commit = 'e1ce9b2b0ebab8205440b0a99026fdb7d4aa6b2e'
prefix = 'review-evidence/p1save-r1/'

def blob(path):
    return subprocess.check_output(['git', '-C', str(root), 'show', commit + ':' + prefix + path])

manifest = json.loads(blob('MANIFEST.json'))
for item in manifest:
    actual = hashlib.sha256(blob(item['file'])).hexdigest()
    assert actual == item['published_sha256'], item['file']
    print('PUBLISHED_SHA256_PASS', actual, item['file'])
print('PUBLISHED_MANIFEST_PASS', len(manifest), 'files', commit)

sys.path.insert(0, str(root / 'sw/firmware/ctrl_nvm/test'))
import nvm_bench
import nvm_mutants
import test_ctrl_nvm
counts = collections.Counter()
for name in nvm_bench.SUITE.tests:
    text = (root / 'sw/firmware/ctrl_nvm/test' / name).read_text()
    for kind, group, test in re.findall(r'\b(TEST_P|TEST_F|TEST)\(\s*(\w+)\s*,\s*(\w+)\s*\)', text):
        counts[(kind, group)] += 1
for key, value in sorted(counts.items()):
    print('DECLARED_TESTS', *key, value)
print('PLANTED_DEFECTS', len(nvm_mutants.MUTANTS), 'COMPILE_CONTROLS', test_ctrl_nvm.CONTROLS,
      'TOTAL', len(nvm_mutants.MUTANTS) + test_ctrl_nvm.CONTROLS)
assert len(nvm_mutants.MUTANTS) + test_ctrl_nvm.CONTROLS == 189
