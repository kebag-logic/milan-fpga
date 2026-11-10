#!/usr/bin/env python3
# Usage: python3 -I check-f01.py <pr-body.txt>
# Checks R801-3-F01: required basis present (whitespace-normalised), replaced basis absent,
# and lists every line citing 10.7.5.2 for manual classification.
import sys, re, hashlib
b = open(sys.argv[1]).read()
req = ("LINK_DOWN leaves the Applicants as they are (Table 10-3 has no Flush! row); it signals no "
       "leavealltimer! to either LeaveAll state machine (GAP-19).")
old = "Flush! is a Registrar event, 10.7.5.2"
j = re.sub(r'\s*\n\s*', ' ', b)
print('sha256', hashlib.sha256(b.encode()).hexdigest())
print('required present:', req in j, 'old present:', old in j)
for i, l in enumerate(b.splitlines(), 1):
    if '10.7.5.2' in l:
        print('cite %d: %s' % (i, l))
sys.exit(0 if (req in j and old not in j) else 1)
