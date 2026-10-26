#!/usr/bin/env python3
"""The owed row from the raw log only: every ACMP frame the entity sent on the wire after the
composed mark, in order, as (message_type, sequence_id), and which GET_RX_STATE commands of
the window got no response by the run's end.
Usage: owed_check.py LOG"""
import sys
lines = open(sys.argv[1]).read().splitlines()
marks = {l.split()[2]: int(l.split()[1]) for l in lines if l.startswith('MARK')}
t0 = marks['composed']
sent = []
for l in lines:
    f = l.split()
    if f and f[0] == 'WIRE' and int(f[1]) > t0:
        fr = bytes.fromhex(f[4])
        if fr[12:14] == b'\x22\xf0' and fr[14] == 0xFC:   # AVTP ACMP
            sent.append((int(f[1]), fr[15] & 0x0F, int.from_bytes(fr[62:64], 'big')))
print('ACMP frames on the wire after the composed mark (cycle, message_type, sequence_id):')
for cyc, mt, seq in sent:
    print(f'  {cyc} type {mt} seq {seq:04x}')
seqs = [s for _, _, s in sent]
probe = 0x7387
k = seqs.index(probe) if probe in seqs else None
print('ahead of the probe response 7387 after the mark:', [f'{s:x}' for s in seqs[:k]] if k is not None else 'probe response absent')
cmds = [0x7380 + n for n in range(8)] + [0x7390 + n for n in range(4)]
print('commands of the window with no response:', [f'{s:x}' for s in cmds if s not in seqs])
