#!/usr/bin/env python3
"""Disposable probe: add a group 'aecp-fanout-full' to a sandbox copy of scenario.py.

Usage: fanout_full.py SANDBOX_HARNESS_DIR
The group registers the firmware's whole registration table (AECP_REGISTRATIONS = 16 controllers,
on every interface) for unsolicited notifications, then a 17th, unregistered controller sends a
SET_NAME. The probe's required recipients are all 16 x interfaces registrations; the grader's own
fan-out rule (last required recipient's commit) ends it. Nothing else in the copy changes.
"""
import sys
from pathlib import Path

path = Path(sys.argv[1]) / 'scenario.py'
text = path.read_text()
group = '''

def fanout_full_groups(p: Point, build: dict) -> list[Group]:
    """Reviewer probe: SET_NAME's notification fan-out with every registration slot used."""
    aecp = CH['aecp']
    g = Group('aecp-fanout-full', sim_ms=2500)
    ready(g, p)
    ctls = [0x0A0B0C0D0E0F1000 + n for n in range(16)]
    seq = 0x5000
    for i in range(p.interfaces):
        for ctl in ctls:
            frame = f.aem_command(f.Aem(p.entity_id, ctl, CTL_MAC, p.mac, seq), 0x0024, bytes(4))
            g.add(f'frame {i} {frame.hex()}', f'wait tx {aecp} 1 within {50 * MS}', 'wait quiet 3 within 2000000')
            seq += 1
    recipients = tuple((ctl, k) for k in range(p.interfaces) for ctl in ctls)
    name = b'fanout full'.ljust(64, b'\\0')
    frame = f.aem_command(f.Aem(p.entity_id, CTL2, CTL_MAC, p.mac, seq), 0x0010,
                          f.be(0, 2) + f.be(0, 2) + f.be(0, 2) + f.be(0, 2) + name)
    g.probe(Probe(f'aecp.set_name_full.if0', 'SET_NAME, every registration slot', 'notify', f'rxc:{aecp}',
                  [f'resp:{aecp}:{seq:x}', f'notify:{aecp}:0010:0:0'], expect='aecp_response',
                  recipients=recipients),
            f'frame 0 {frame.hex()}', wait=f'tx {aecp} {1 + len(recipients)} within {200 * MS}')
    return [g]
'''
anchor = '\n\ndef all_groups('
assert text.count(anchor) == 1
text = text.replace(anchor, group + anchor)
old = '*backlog_groups(p), *control_groups(p)]'
assert text.count(old) == 1
text = text.replace(old, '*backlog_groups(p), *control_groups(p), *fanout_full_groups(p, build)]')
path.write_text(text)
print('added aecp-fanout-full')
