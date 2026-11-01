#!/usr/bin/env python3
"""Exact-text checks of the round 6 delta. Usage: check_delta_r6.py <page> <PR body>"""
import re
import subprocess
import sys

page = open(sys.argv[1], encoding='utf-8').read()
body = open(sys.argv[2], encoding='utf-8').read()
CHECKS = [
    ('SE placement condition', page, 'Under a valid head, conversion error never shifts a sample.'),
    ('SE margin line', page, 'A margin under 125 µs lapses the head every packet.'),
    ('SE interleave line', page, 'Interleaved copies can then land one sample apart.'),
    ('SE item 3 pointer', page, '[Open design item 3](#open-design-items) owns that case.'),
    ('SE Annex D.2 condition', page, 'Under a valid head, clean copies keep that external behaviour.'),
    ('RR9 rule 2', page, 'it anchors the head and restarts the map with only bit 0 set'),
    ('RR8 TU-4', page, 'A stream that starts with tu, unpaired or on both networks, still renders.'),
    ('RR8 PR Round 5 row', body, 'TU-4 requires that a stream starting with tu still renders, unpaired or on both networks, with the lane stating how.'),
    ('Item 3 setup', page, 'Simulation with clean copies on both networks 10 to 50 µs before their time, first arrival interleaved, at 48, 96 and 192 kHz, every grid phase.'),
    ('Item 3 test', page, 'The test fails on a shift beyond what the lane states.'),
    ('Item 3 size as probe result', page, "reports up to 766 shifts and 383 unwritten samples in 2,000 packets. That is the probe's result, not a design figure"),
    ('PR known limitation', body, '**Short margin on both networks:** a margin under 125 µs lapses the head every packet, so interleaved clean copies can land one sample apart; open design item 3 for the same lane sets the allowed shift, and this PR states none.'),
    ('PR Round 3 note', body, '(round 6 conditions this on a valid head)'),
]
for name, hay, needle in CHECKS:
    print(f"{'OK ' if needle in hay else 'MISSING'} {name}: {hay.count(needle)} hit(s)")
for name, hay, gone in (('old placement line', page, 'So conversion error never shifts a sample.'),
                        ('old map text', page, 'clears the map'),
                        ('old Annex D.2 line', page, 'The merge keeps that external behaviour')):
    print(f"{'OK ' if gone not in hay else 'PRESENT'} removed: {name}: {hay.count(gone)} hit(s)")
row = [l for l in body.splitlines() if '`07f8eb91`' in l]
print('RR10 row(s):', len(row), [r.rstrip(' |')[-40:] for r in row])
print('766 in page lines:', [i + 1 for i, l in enumerate(page.splitlines()) if re.search(r'\b766\b', l)])
print('383 in page lines:', [i + 1 for i, l in enumerate(page.splitlines()) if re.search(r'\b383\b', l)])
print('766 in body lines:', [i + 1 for i, l in enumerate(body.splitlines()) if re.search(r'\b766\b', l)])
print('never shifts in body:', [l[:70] for l in body.splitlines() if 'never shifts' in l])
