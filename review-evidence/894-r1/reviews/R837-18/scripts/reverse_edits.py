#!/usr/bin/env python3
"""Undo the four R837-17 edits (F1's exact fix, S1's three SHAs) on the live PR body and print the result's sha256,
so it can be compared with the body R837-17 reviewed (sha256 prefix 4d54a675). usage: reverse_edits.py <live_body> <out>"""
import hashlib, sys
live = open(sys.argv[1], encoding='utf-8', newline='').read()
fix = ("and of the files it imports or reads outside that directory, later commits change `poll_grade.py` and "
       "`aecp_mbx.h` in comments only and `ctrl_loop.h` in comments and in `CTRL_LOOP_TX_MS`, which none of them "
       "reads, so its result carries to the head; run at `07ed787e` it prints the same 28 of 28 checks and 96 of 96 "
       "mutants (R837-17's `receipts/hooks_selftest_07ed787e.log`).")
old = "so its result carries by the identity of its inputs."
edits = [(fix, old),
         ("Three sweeps run at `26898c05`", "Three sweeps run at the head"),
         ("run again at `b6f5c638`", "run again at the head"),
         ("run again at `478ff78c`", "run again at the head")]
body = live
for new, prior in edits:
    n = body.count(new)
    print(f'{n} x {new[:60]!r}')
    body = body.replace(new, prior)
print('old F1 phrase in live:', live.count(old), '| "identity of its inputs" in live:', live.count('identity of its inputs'))
open(sys.argv[2], 'w', encoding='utf-8', newline='').write(body)
for name, text in (('live', live), ('reconstructed', body)):
    for variant, t in ((name, text), (name + '+LF', text + '\n'), (name + '-LF', text.rstrip('\n'))):
        print(variant, hashlib.sha256(t.encode()).hexdigest())
