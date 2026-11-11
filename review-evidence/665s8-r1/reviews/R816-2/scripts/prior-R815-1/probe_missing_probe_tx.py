#!/usr/bin/env python3
"""Probe: a published unloaded wire log with one draw's PROBE_TX transaction removed, as if that BIND_RX caused
no PROBE_TX (its commit, KL_mbx egress, MAC frame, the talker's answer and the ACMP slot's arms in that
transaction all gone). The head's grader is asked to grade it; a pass (no finding) means the grade does not
require one PROBE_TX per draw.

usage: probe_missing_probe_tx.py <checkout> <wire.log> <draws> <interfaces> <announces> <k>
"""
import sys
from pathlib import Path
checkout, logp = Path(sys.argv[1]), Path(sys.argv[2])
draws, n_if, announces, k = map(int, sys.argv[3:7])
sys.path.insert(0, str(checkout / 'tb/verilator/ctrl_wire_timing'))
import wire_grade as g
lines = logp.read_text().splitlines()
ACMP_CH = g.CHANNELS.index('acmp')
txc = [n for n, ln in enumerate(lines) if ln.startswith('TXC ') and int(ln.split()[2]) == ACMP_CH]
mtx = [n for n, ln in enumerate(lines) if ln.startswith('MTX ') and int(ln.split()[3]) == ACMP_CH]
txw = [n for n, ln in enumerate(lines) if ln.startswith('TXW ') and bytes.fromhex(ln.split()[4])[12:15] == b'\x22\xf0\xfc']
assert all(int(lines[m].split()[2]) == 0 for m in mtx), 'this probe handles interface-0-only ACMP egress'
assert len(txc) == len(mtx) == len(txw), (len(txc), len(mtx), len(txw))
probes = [i for i, n in enumerate(txw) if (bytes.fromhex(lines[n].split()[4])[15] & 0x0F) == g.PROBE_TX]
i = probes[k]
frame = bytes.fromhex(lines[txw[i]].split()[4])
seq = int.from_bytes(frame[62:64], 'big')
start = int(lines[txc[i]].split()[1])
nxt = int(lines[txc[probes[k + 1]]].split()[1])
slot = g.ACMP_FIRST_SLOT_IFS * n_if
drop = {txc[i], mtx[i], txw[i]}
for n, ln in enumerate(lines):
    w = ln.split()
    if w and w[0] == 'RXW' and bytes.fromhex(w[5])[12:15] == b'\x22\xf0\xfc' and \
            (bytes.fromhex(w[5])[15] & 0x0F) == g.PROBE_TX_RESPONSE and int.from_bytes(bytes.fromhex(w[5])[62:64], 'big') == seq:
        drop.add(n)
    if w and w[0] == 'TMR' and (int(w[2], 16) & 0xFF) == slot and start <= int(w[1]) < nxt:
        drop.add(n)
mutant = '\n'.join(ln for n, ln in enumerate(lines) if n not in drop) + '\n'
original = g.grade(logp.read_text(), 100_000_000, draws, n_if, announces)
result, findings = g.grade(mutant, 100_000_000, draws, n_if, announces)
row = lambda r, p: next(x for x in r['rows'] if x['path'] == p)
print(f'removed PROBE_TX #{k} (sequence_id {seq:#06x}), {len(drop)} lines')
print(f"original: findings={len(original[1])} probe_tx_n={row(original[0], 'acmp.probe_tx')['n']} "
      f"bind_rx_n={row(original[0], 'acmp.bind_rx')['n']}")
print(f"mutant:   findings={len(findings)} probe_tx_n={row(result, 'acmp.probe_tx')['n']} "
      f"bind_rx_n={row(result, 'acmp.bind_rx')['n']} bind_to_probe_tx_max_ms={row(result, 'acmp.bind_to_probe_tx')['max_ms']}")
for f in findings:
    print('FINDING', f)
print('VERDICT:', 'ESCAPED (graded as a pass)' if not findings else 'caught')
