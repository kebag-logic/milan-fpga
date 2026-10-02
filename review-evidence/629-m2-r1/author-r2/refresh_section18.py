#!/usr/bin/env python3
"""Refresh the capture figures in the saved-state docs from the new receipt.

Usage: refresh_section18.py <repo>

Every figure written is read from tb/verilator/nvm_capture_cpu/measurements.json
(the receipt assemble_receipt.py wrote and the gate re-checked); every old
figure replaced is read from the receipt at HEAD, so a sentence that does not
match exactly once stops the script instead of being skipped.
"""
import json
import subprocess
import sys
from pathlib import Path

repo = Path(sys.argv[1])
REC = 'tb/verilator/nvm_capture_cpu/measurements.json'
new = json.loads((repo / REC).read_text())
old = json.loads(subprocess.run(['git', '-C', str(repo), 'show', f'HEAD:{REC}'],
                                check=True, capture_output=True, text=True).stdout)
LIMIT_MS = new['hold_floor_ms'] / 2
X8, X1 = 'endstation_ax7101_8x8', 'endstation_ax7101_1x1_tdm8'


def maxima(r: dict) -> dict:
    return {(m['shape'], m['cpu_hz']): m for m in r['maxima']}


def arm(r: dict, shape: str, mhz: int, traffic: str) -> dict:
    return next(m for m in r['measurements']
                if (m['shape'], m['cpu_hz'], m['traffic']) == (shape, mhz * 1_000_000, traffic))


def ms(v: float) -> str:
    return f'{v:.5f}'.rstrip('0').rstrip('.') if False else f'{v:.5f}'


def ratio(v: float) -> str:
    return f'{v:.4f}x'


def census(r: dict, shape: str) -> tuple[str, str]:
    c = r['measured_for'][shape]
    return f"{c['raw_bytes']:,}", f"{c['records']}"


mo, mn = maxima(old), maxima(new)
w8o, w8n = mo[(X8, 50_000_000)], mn[(X8, 50_000_000)]
w1o, w1n = mo[(X1, 50_000_000)], mn[(X1, 50_000_000)]
c8o, c8n = mo[(X8, 100_000_000)], mn[(X8, 100_000_000)]
HIST_MS = 24.30246   # the historical byte-copy maximum, stated on the page at the old census


def row(r: dict, shape: str, mhz: int, traffic: str, label: str, basis: str) -> str:
    a = arm(r, shape, mhz, traffic)
    return (f"| {label} | {mhz} / 100, {basis} | {traffic.upper()} | "
            f"{a['minimum_ms']:.5f} to {a['maximum_ms']:.5f} | {ratio(a['margin'])} |")


ROWS = [(X1, 50, 'on', '1x1', 'contract'), (X1, 50, 'off', '1x1', 'contract'),
        (X8, 50, 'on', '8x8', 'contract'), (X8, 50, 'off', '8x8', 'contract'),
        (X8, 100, 'on', '8x8', 'non-contract'), (X8, 100, 'off', '8x8', 'non-contract')]

b8o, r8o = census(old, X8)
b8n, r8n = census(new, X8)
b1o, r1o = census(old, X1)
b1n, r1n = census(new, X1)
assignment = new['remeasurement_assignment']

EDITS = {
    'docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md': [
        ("  (MILAN_NVM_STAGE_BASE): 3264 bytes at 1x1 and 12680 at 8x8,",
         "  (MILAN_NVM_STAGE_BASE): 3336 bytes at 1x1 and 13256 at 8x8,"),
        ("derives 3264 bytes at 1x1 and 12680 at 8x8.",
         "derives 3336 bytes at 1x1 and 13256 at 8x8."),
        (f"Timing. MEASURED on {old['date']} in the",
         f"Timing. MEASURED on {new['date']} in the"),
        (f"The [#70 AEM-first ruling]({old['remeasurement_assignment']}) requires this firmware remeasurement.",
         f"The [#629 round-2 assignment]({assignment}) requires this remeasurement.\n"
         f"The CLOCK_SOURCE NAME records #629 adds grow the census.\n"
         f"The [#70 AEM-first ruling]({old['remeasurement_assignment']}) required the previous one."),
        (f"Measured commit: `{old['base']}`.", f"Measured commit: `{new['base']}`."),
        (f"Measured tree: `{old['tree']}`.", f"Measured tree: `{new['tree']}`."),
        (f"**The worst 8x8 measurement is {ms(w8o['maximum_ms'])} ms.**\n"
         f"Its floor ratio is {ratio(w8o['margin'])}.\n"
         f"The margin to 24.5 ms is {LIMIT_MS - w8o['maximum_ms']:.5f} ms.\n"
         f"The historical pre-word-copy maximum was {HIST_MS:.5f} ms.\n"
         f"The word-copy remedy gains {HIST_MS - w8o['maximum_ms']:.5f} ms of margin.\n"
         "Firmware changed; hold behavior and the record census remain unchanged.\n"
         "The receipt binds the new firmware, including its startup guard.\n",
         f"**The worst 8x8 measurement is {ms(w8n['maximum_ms'])} ms.**\n"
         f"Its floor ratio is {ratio(w8n['margin'])}.\n"
         f"The margin to 24.5 ms is {LIMIT_MS - w8n['maximum_ms']:.5f} ms.\n"
         f"The previous census measured {ms(w8o['maximum_ms'])} ms.\n"
         f"The historical pre-word-copy maximum was {HIST_MS:.5f} ms, at that census.\n"
         f"The word-copy remedy gained {HIST_MS - w8o['maximum_ms']:.5f} ms of margin there.\n"
         "Firmware, hold behavior and the measured paths are unchanged.\n"
         f"The record census grows: 8x8 from {r8o} to {r8n} records, {b8o} to {b8n} bytes.\n"
         f"At 1x1 it grows from {r1o} to {r1n} records, {b1o} to {b1n} bytes.\n"
         "The receipt binds the same firmware and the new census.\n"),
        (f"The 1x1 maximum is {ms(w1o['maximum_ms'])} ms ({ratio(w1o['margin'])[:-1]}x floor ratio).\n\n"
         "| Shape |",
         f"The 1x1 maximum is {ms(w1n['maximum_ms'])} ms ({ratio(w1n['margin'])[:-1]}x floor ratio).\n\n"
         "| Shape |"),
    ] + [(row(old, *r), row(new, *r)) for r in ROWS] + [
        (f"The full closed-record census is {b1o} bytes / {r1o} records at 1x1.\n"
         f"At 8x8 it is {b8o} bytes / {r8o} records.",
         f"The full closed-record census is {b1n} bytes / {r1n} records at 1x1.\n"
         f"At 8x8 it is {b8n} bytes / {r8n} records."),
        (f"   The worst 8x8 copy is {ms(w8o['maximum_ms'])} ms across both arms.\n"
         f"   It covers {b8o} bytes and {r8o} records, including output maps.\n"
         f"   Its ratio to the guaranteed 49 ms floor is {ratio(w8o['margin'])}.\n"
         f"   The 24.5 ms margin is {LIMIT_MS - w8o['maximum_ms']:.5f} ms.\n"
         f"   The word-copy remedy gains {HIST_MS - w8o['maximum_ms']:.5f} ms over historical byte copying.\n",
         f"   The worst 8x8 copy is {ms(w8n['maximum_ms'])} ms across both arms.\n"
         f"   It covers {b8n} bytes and {r8n} records, including output maps.\n"
         f"   Its ratio to the guaranteed 49 ms floor is {ratio(w8n['margin'])}.\n"
         f"   The 24.5 ms margin is {LIMIT_MS - w8n['maximum_ms']:.5f} ms.\n"
         f"   At the previous census the word-copy remedy gained {HIST_MS - w8o['maximum_ms']:.5f} ms over historical byte copying.\n"),
        (f"   The 1x1 maximum is {ms(w1o['maximum_ms'])} ms ({ratio(w1o['margin'])[:-1]}x floor ratio).\n",
         f"   The 1x1 maximum is {ms(w1n['maximum_ms'])} ms ({ratio(w1n['margin'])[:-1]}x floor ratio).\n"),
        (f"   The 100 MHz 8x8 comparison is non-contract: {ms(c8o['maximum_ms'])} ms maximum.\n",
         f"   The 100 MHz 8x8 comparison is non-contract: {ms(c8n['maximum_ms'])} ms maximum.\n"),
    ],
    'tb/verilator/nvm_capture_cpu/README.md': [
        (f"The full 8x8 copy covers {b8o} bytes and {r8o} records.",
         f"The full 8x8 copy covers {b8n} bytes and {r8n} records."),
        (f"The 1x1 copy covers {b1o} bytes and {r1o} records.",
         f"The 1x1 copy covers {b1n} bytes and {r1n} records."),
    ],
}

for path, edits in EDITS.items():
    p = repo / path
    s = p.read_text()
    for a, b in edits:
        n = s.count(a)
        if n != 1:
            sys.exit(f'{path}: expected one occurrence, found {n}:\n{a}')
        s = s.replace(a, b)
    p.write_text(s)
    print(f'{path}: {len(edits)} edits')
print('8x8 maximum', w8n['maximum_ms'], 'limit', LIMIT_MS, 'margin', LIMIT_MS - w8n['maximum_ms'])
