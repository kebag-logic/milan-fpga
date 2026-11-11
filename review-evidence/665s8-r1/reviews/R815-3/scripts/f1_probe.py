#!/usr/bin/env python3
"""Falsification probe for the round's new loaded-log controls.

Part A prints the loaded log's MAAP slot writes, its LOAD lines, and the clean loaded log's graded load table
and findings, so the counts LOADED expects can be read off the log itself.
Part B applies further disposable in-place mutants of the load accounting (beyond delta_mutants.py) and reports
which controls each one fails; every mutant is restored byte-for-byte after its run.

usage: f1_probe.py <checkout>
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
D = ROOT / 'tb/verilator/ctrl_wire_timing'
G = D / 'wire_grade.py'

PART_A = r'''
import sys
sys.path.insert(0, sys.argv[1])
import wire_selftest as s, wire_grade as g
log = s.loaded()
slot = g.MAAP_FIRST_SLOT_IFS
for ln in log.text():
    w = ln.split()
    if (w[0] == 'TMR' and (int(w[2], 16) & 0xFF) == slot) or w[0].startswith('LOAD') or 'load-aecp' in ln:
        print('LINE', ln)
for name, fn in (('clean-loaded', lambda: s.loaded().text()),
                 ('load-offer-over-delivered', lambda: s.loaded(over_delivered=True).text()),
                 ('received-frame-unaccounted', lambda: s.loaded(untagged=True).text())):
    print('CASE', name)
    print(' expected LOADED', s.LOADED)
'''

MUTANTS = [
    # a partly delivered offer counted as delivered whole
    ('delivered-counts-partial', "        t['delivered_offers'] += whole\n", "        t['delivered_offers'] += got > 0\n"),
    # delivered frames counted only for whole offers (the frame equation then misses the partial offer's frame)
    ('frames-only-whole', "        t['delivered_frames'] += got\n",
     "        t['delivered_frames'] += got if got == offer.frames else 0\n"),
    # armed counted only for offers that were delivered whole
    ('armed-only-delivered', "            t['armed'] += 1\n", "            t['armed'] += whole\n"),
    # an armed burst delivered in part counted as meeting its expiry
    ('met-counts-partial', "            t['expiries_met'] += whole and offer.at in fired[offer.trigger]\n",
     "            t['expiries_met'] += bool(got) and offer.at in fired[offer.trigger]\n"),
    # partial counted as any offer not delivered whole (includes undelivered)
    ('partial-includes-undelivered', "        t['partial_offers'] += 0 < got < offer.frames\n",
     "        t['partial_offers'] += got < offer.frames\n"),
    # over-delivery found only above twice the queued frames
    ('over-delivery-threshold-doubled', "        if got > offer.frames:\n", "        if got > 2 * offer.frames:\n"),
    # a cancel no longer stops an arm from expiring (expiries() ignores later writes)
    ('expiry-ignores-cancel', "        if n + 1 == len(writes) or writes[n + 1][0] >= due:\n", "        if True:\n"),
]


def selftest() -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, '-B', str(D / 'run.py'), '--self-test'], capture_output=True, text=True,
                          cwd=ROOT)


def main() -> int:
    a = subprocess.run([sys.executable, '-B', '-c', PART_A, str(D)], capture_output=True, text=True, cwd=ROOT)
    print(a.stdout, a.stderr, sep='')
    base = selftest()
    for ln in base.stdout.splitlines():
        if 'clean-loaded' in ln or 'over-delivered' in ln or 'unaccounted' in ln or 'controls,' in ln:
            print('BASE', ln)
    for name, old, new in MUTANTS:
        original = G.read_bytes()
        text = original.decode()
        if text.count(old) != 1:
            print(f'mutant {name}: NOT APPLIED ({text.count(old)} matches)')
            continue
        G.write_text(text.replace(old, new))
        try:
            run = selftest()
        finally:
            G.write_bytes(original)
        failed = [ln.split()[1].rstrip(':') for ln in run.stdout.splitlines()
                  if ln.startswith('control ') and (' FAIL' in ln or ': ESCAPED' in ln)]
        print(f'mutant {name}: {"KILLED" if run.returncode else "SURVIVED"} rc={run.returncode} failing={failed}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
