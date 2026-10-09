#!/usr/bin/env python3
# Probes of needle_audit.validate_needles with gtest default-message fragments; argv[1] = tree root.
import copy, json, sys
sys.path.insert(0, sys.argv[1] + '/scripts')
from needle_audit import validate_needles
table = json.load(open(sys.argv[1] + '/tests/mutations.json'))
for value in ('    Which is: 5', 'Expected equality of these values:', 'Actual: 4', 'Which is:',
              'Expected equality', 'equality of these values', 'r.frames.size()', '5u', 'Which is', 'is: 5',
              'both owed frames and ANNOUNCE leave once room returns'):
    t = copy.deepcopy(table); t[0]['kills'][0]['needle'] = value
    print(('refused ' if validate_needles(t) else 'accepted') + ' ' + repr(value))
