#!/usr/bin/env python3
"""Summarize which AcmpWalk tests failed, by which message and at which step, for each plant of a campaign."""
import json, re, sys
r = json.load(open(sys.argv[1]))
for x in r:
    out = {}
    for t, msg in x.get('failures', {}).items():
        tags = [tag for tag, s in (('trace', "full walk's calls"), ('sink0', 'no sink marked'),
                                   ('if0', 'no interface marked'), ('reach', 'the random entries')) if s in msg]
        m = re.search(r'at step (\d+)', msg)
        out[t.split('.')[1].replace('MatchTheFullWalk', '').replace('MatchesTheFullWalk', '')] = (tags, m.group(1) if m else None)
    print(x['status'], x['name'], out, x.get('error', ''))
