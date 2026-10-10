#!/usr/bin/env python3
"""Make the published (masked) tone_points_b15.py runnable for its synthetic controls.

usage: unmask_synthetic_ids.py <tools-dir>

The packet's tone_points_b15.py has its synthetic control stream ID and synthetic source address masked
as placeholders. This writes tone_points_b15_unmasked.py beside it with those two placeholders replaced
by synthetic values (stream ID 020000fffe0000aa, address 020000fffeaa); nothing else changes.
"""
import os
import sys

src = os.path.join(sys.argv[1], "tone_points_b15.py")
s = open(src).read()
a = s.replace('"<peer-eid>"', '"020000fffe0000aa"').replace('bytes.fromhex("<peer-id>")', 'bytes.fromhex("020000fffeaa")')
assert a.count("<peer-") == 0 and a != s
open(os.path.join(sys.argv[1], "tone_points_b15_unmasked.py"), "w").write(a)
print("written", os.path.join(sys.argv[1], "tone_points_b15_unmasked.py"))
