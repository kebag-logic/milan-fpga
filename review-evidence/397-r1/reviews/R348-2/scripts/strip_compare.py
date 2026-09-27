#!/usr/bin/env python3
"""Strip round-2 passive observation events (ticks, aem_read) from a round-2 log and
compare with the round-1 raw log. usage: strip_compare.py <round2.log|json> <round1.json>"""
import hashlib, json, re, sys
a = sys.argv[1]
new = json.load(open(a))['raw_log'] if a.endswith('.json') else open(a, 'rb').read().decode()
old = json.load(open(sys.argv[2]))['raw_log']
stripped = re.sub(r'\nEVENT cycle=\d+ kind=(?:ticks|aem_read)[^\n]*\n', '', new)
print('round-1 sha256        ', hashlib.sha256(old.encode()).hexdigest())
print('stripped round-2 sha256', hashlib.sha256(stripped.encode()).hexdigest())
print('identical:', stripped == old)
sys.exit(0 if stripped == old else 1)
