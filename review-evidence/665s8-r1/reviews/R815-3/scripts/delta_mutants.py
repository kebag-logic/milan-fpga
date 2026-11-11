#!/usr/bin/env python3
"""Disposable mutants of the round's new grader and reuse-guard checks; each must make the self-test fail
with the named control(s). Every mutant is applied in place and restored byte-for-byte after its run.

usage: delta_mutants.py <checkout>
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
D = ROOT / 'tb/verilator/ctrl_wire_timing'
G, B = D / 'wire_grade.py', D / 'wire_build.py'

MUTANTS = [
    ('bind-status-check-gone', G, "        if resp[0].status != SUCCESS:\n", "        if False:\n", ['bind-refused']),
    ('pairing-by-any-later-probe', G,
     "        own = [p for p in probes if p.first > resp[0].last and (until is None or p.first < until)]\n",
     "        own = [p for p in probes if p.first > cmd.last]\n", ['bind-without-its-probe-tx']),
    ('probe-count-check-gone', G, "    if len(probe.cycles) != draws:\n", "    if False:\n",
     ['probe-tx-transactions-not-the-draws']),
    ('aecp-status-check-gone', G, "        if final[0].status != statuses[name]:\n", "        if False:\n",
     ['aem-refused', 'mvu-refused']),
    ('no-period-check-gone', G, "    if announces > 1 and not period.cycles:\n", "    if False:\n",
     ['no-advertise-period']),
    ('stopped-check-gone', G, "    if quiet >= high:\n", "    if False:\n", ['stopped-advertising']),
    ('skip-after-announce-gone', G, "            if skipped and interface in offer.announced:\n",
     "            if False:\n", ['echo-skipped-after-the-announce']),
    ('frame-equation-gone', G, "    if delivered + FRAMES_PER_DRAW * draws != received:\n", "    if False:\n",
     ['received-frame-unaccounted']),
    ('expiry-met-ignores-arm', G, "            t['expiries_met'] += whole and offer.at in fired[offer.trigger]\n",
     "            t['expiries_met'] += whole\n", ['clean-loaded']),
    ('split-sources-unrecorded', B, "*split_sources(out, spec),", "",
     ['reuse-after-an-edit-of-tb_split_top.sv', 'reuse-after-an-edit-of-milan_datapath.sv',
      'reuse-after-an-edit-of-KL_mbx.sv']),
    ('makefile-unrecorded', B, ", MILAN_DP / 'Makefile')", ")", ['reuse-after-an-edit-of-Makefile']),
    ('firmware-tree-unrecorded', B,
     "    found['tree:firmware'] = budget_build.tree_digest([ROOT / t for t in FIRMWARE_TREES])\n", "",
     ['reuse-after-an-edit-of-tree:firmware']),
    ('partial-offers-never-counted', G, "        t['partial_offers'] += 0 < got < offer.frames\n",
     "        t['partial_offers'] += 0\n", ['clean-loaded']),
    ('over-delivery-check-gone', G, "        if got > offer.frames:\n", "        if False:\n",
     ['load-offer-over-delivered']),
]


def main() -> int:
    bad = 0
    for name, path, old, new, controls in MUTANTS:
        original = path.read_bytes()
        text = original.decode()
        if text.count(old) != 1:
            print(f'mutant {name}: NOT APPLIED ({text.count(old)} matches)')
            bad += 1
            continue
        path.write_text(text.replace(old, new))
        try:
            run = subprocess.run([sys.executable, '-B', str(D / 'run.py'), '--self-test'], capture_output=True,
                                 text=True, cwd=ROOT)
        finally:
            path.write_bytes(original)
        failed = [ln.split()[1].rstrip(':') for ln in run.stdout.splitlines()
                  if ln.startswith('control ') and (' FAIL' in ln or ': ESCAPED' in ln)]
        killed = run.returncode != 0 and all(c in failed for c in controls)
        print(f'mutant {name}: {"KILLED" if killed else "SURVIVED"} rc={run.returncode} failing={failed}')
        bad += not killed
    print(f'delta_mutants: {len(MUTANTS)} mutants, {bad} survived or not applied')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
