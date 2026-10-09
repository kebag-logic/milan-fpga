#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Ask the tree's needle audit about fragments of GoogleTest default failure lines.

argv[1] = tree root. For each required killer, every substring (3+ characters) of the
default failure templates is tried as that killer's needle. A fragment the audit accepts
matches default output of any failing assertion, so it does not identify an assertion.
"""
import collections
import copy
import json
import sys
sys.path.insert(0, sys.argv[1] + '/scripts')
from needle_audit import validate_needles, assertion_literals

TEMPLATES = ('Expected equality of these values:', 'Which is: ', 'Value of: ', 'Actual: false',
             'Actual: true', 'Expected: true', 'Expected: false', 'Expected: (', ') <= (', ') != (',
             'Failed', 'Google Test trace:')
table = json.load(open(sys.argv[1] + '/tests/mutations.json'))
messages = assertion_literals()
fragments = sorted({t[i:j] for t in TEMPLATES for i in range(len(t)) for j in range(i + 3, len(t) + 1)})
accepted = collections.Counter()
kills = 0
for p, plant in enumerate(table):
    for k, kill in enumerate(plant['kills']):
        kills += 1
        for value in fragments:
            if not value.strip():
                continue
            planted = [copy.deepcopy(plant)]
            planted[0]['kills'][k]['needle'] = value
            if not validate_needles(planted, messages):
                accepted[value] += 1
for value in ('e', 'a', 's', 'n'):
    planted = copy.deepcopy(table[:1])
    planted[0]['kills'][0]['needle'] = value
    print('single character', repr(value), 'refused' if validate_needles(planted, messages) else 'ACCEPTED')
print('kills', kills, 'fragments tried per kill', len(fragments))
for value, n in accepted.most_common():
    print(f'ACCEPTED default fragment {value!r} for {n} killers')
print('accepted default fragments:', len(accepted))
