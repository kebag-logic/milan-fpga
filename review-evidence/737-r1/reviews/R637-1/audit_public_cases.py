#!/usr/bin/env python3
"""Independently compare published case receipts against current driver inventories.

This verifies published digests, not the unpublished stdout bytes themselves.
"""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
evidence = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(root / 'scripts'))
from ci_case_receipts import verify
from ci_suite_pieces import inventory, PIECE_SECONDS

for suite in PIECE_SECONDS:
    directory = evidence / 'author' / 'case-evidence' / suite
    full = json.loads((directory / 'full.json').read_text())
    legs = [json.loads(path.read_text()) for path in sorted(directory.glob('leg-*.json'))]
    names = inventory(suite)
    assert names == json.loads((directory / 'inventory.json').read_text())
    left = verify(names, [full], suite, full['head'], full['tree'])
    right = verify(names, legs, suite, full['head'], full['tree'])
    assert left == right
    altered = copy.deepcopy(legs)
    dropped = altered[0]['results'].pop(0)['case']
    try:
        verify(names, altered, suite, full['head'], full['tree'])
    except ValueError as exc:
        refusal = str(exc)
    else:
        raise AssertionError('dropped case accepted')
    print(json.dumps(dict(suite=suite, cases=len(names), legs=len(legs),
                         head=full['head'], tree=full['tree'],
                         equal_per_case_verdicts_and_output_digests=True,
                         dropped_case=dropped, drop_refusal=refusal,
                         raw_stdout_rehashed=False), sort_keys=True))

document = json.loads((evidence / 'author' / 'source-correspondence.json').read_text())
for group in document['identical_source_groups']:
    command = ['git', 'diff', '--no-ext-diff', '--no-textconv', group['source_head'],
               document['candidate_head'], '--', *group['paths']]
    result = subprocess.run(command, cwd=root, capture_output=True)
    if result.returncode:
        print(json.dumps({'source_group': group['group'], 'independent_object_comparison':
                          'unavailable: source object absent from clone'}))
    else:
        assert not result.stdout
        print(json.dumps({'source_group': group['group'], 'independent_object_comparison': 'identical'}))
