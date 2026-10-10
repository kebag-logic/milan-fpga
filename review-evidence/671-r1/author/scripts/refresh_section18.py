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
HIST_MS = 24.30246   # the historical byte-copy maximum, stated on the page
PREV_CENSUS_MS = 13.23352   # the 8x8 maximum before #629 grew the census, stated on the page


def maxima(r: dict) -> dict:
    return {(m['shape'], m['cpu_hz']): m for m in r['maxima']}


def arm(r: dict, shape: str, mhz: int, traffic: str) -> dict:
    return next(m for m in r['measurements']
                if (m['shape'], m['cpu_hz'], m['traffic']) == (shape, mhz * 1_000_000, traffic))


def ms(v: float) -> str:
    return f'{v:.5f}'


def ratio(v: float) -> str:
    return f'{v:.4f}x'


def row(r: dict, shape: str, mhz: int, traffic: str, label: str, basis: str) -> str:
    a = arm(r, shape, mhz, traffic)
    return (f"| {label} | {mhz} / 100, {basis} | {traffic.upper()} | "
            f"{a['minimum_ms']:.5f} to {a['maximum_ms']:.5f} | {ratio(a['margin'])} |")


assert new['measured_for'] == old['measured_for'], 'the census moved; this script assumes it did not'
mo, mn = maxima(old), maxima(new)
w8o, w8n = mo[(X8, 50_000_000)], mn[(X8, 50_000_000)]
w1o, w1n = mo[(X1, 50_000_000)], mn[(X1, 50_000_000)]
c8o, c8n = mo[(X8, 100_000_000)], mn[(X8, 100_000_000)]
ROWS = [(X1, 50, 'on', '1x1', 'contract'), (X1, 50, 'off', '1x1', 'contract'),
        (X8, 50, 'on', '8x8', 'contract'), (X8, 50, 'off', '8x8', 'contract'),
        (X8, 100, 'on', '8x8', 'non-contract'), (X8, 100, 'off', '8x8', 'non-contract')]
pp_old, pp_new = old['processor_pins']['protocol-processor'], new['processor_pins']['protocol-processor']

EDITS = {
    'docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md': [
        (f"Timing. MEASURED on {old['date']} in the",
         f"Timing. MEASURED on {new['date']} in the"),
        (f"The [#629 round-2 assignment]({old['remeasurement_assignment']}) requires this remeasurement.\n"
         "The CLOCK_SOURCE NAME records #629 adds grow the census.\n",
         f"The [#671 assignment]({new['remeasurement_assignment']}) requires this remeasurement.\n"
         "The #671 boot read-fault rule changes the product firmware.\n"
         f"The [#629 round-2 assignment]({old['remeasurement_assignment']}) required the previous one.\n"
         "The CLOCK_SOURCE NAME records #629 adds grew the census.\n"),
        ("The [#70 AEM-first ruling](https://github.com/kebag-logic/milan-fpga/issues/70#issuecomment-5894183475) required the previous one.\n",
         "The [#70 AEM-first ruling](https://github.com/kebag-logic/milan-fpga/issues/70#issuecomment-5894183475) required the one before.\n"),
        (f"Measured commit: `{old['base']}`.", f"Measured commit: `{new['base']}`."),
        (f"Measured tree: `{old['tree']}`.", f"Measured tree: `{new['tree']}`."),
        (f"Firmware SHA-256: `{old['product_firmware_sha256']}`.",
         f"Firmware SHA-256: `{new['product_firmware_sha256']}`."),
        (f"Protocol-processor pin: `{pp_old}`.", f"Protocol-processor pin: `{pp_new}`."),
        (f"**The worst 8x8 measurement is {ms(w8o['maximum_ms'])} ms.**\n"
         f"Its floor ratio is {ratio(w8o['margin'])}.\n"
         f"The margin to 24.5 ms is {LIMIT_MS - w8o['maximum_ms']:.5f} ms.\n"
         f"The previous census measured {ms(PREV_CENSUS_MS)} ms.\n"
         f"The historical pre-word-copy maximum was {HIST_MS:.5f} ms, at that census.\n"
         f"The word-copy remedy gained {HIST_MS - PREV_CENSUS_MS:.5f} ms of margin there.\n"
         "Firmware, hold behavior and the measured paths are unchanged.\n"
         "The record census grows: 8x8 from 156 to 164 records, 12,634 to 13,210 bytes.\n"
         "At 1x1 it grows from 53 to 54 records, 3,218 to 3,290 bytes.\n"
         "The receipt binds the same firmware and the new census.\n",
         f"**The worst 8x8 measurement is {ms(w8n['maximum_ms'])} ms.**\n"
         f"Its floor ratio is {ratio(w8n['margin'])}.\n"
         f"The margin to 24.5 ms is {LIMIT_MS - w8n['maximum_ms']:.5f} ms.\n"
         f"The previous receipt measured {ms(w8o['maximum_ms'])} ms, at the same census.\n"
         f"The census before #629 measured {ms(PREV_CENSUS_MS)} ms.\n"
         f"The historical pre-word-copy maximum was {HIST_MS:.5f} ms, at that census.\n"
         f"The word-copy remedy gained {HIST_MS - PREV_CENSUS_MS:.5f} ms of margin there.\n"
         "The firmware changed in its boot path only; `nvm_capture()`, the hold and the census are unchanged.\n"
         "The census is 164 records and 13,210 bytes at 8x8, 54 and 3,290 at 1x1.\n"
         "The receipt binds the new firmware and the unchanged census.\n"),
        (f"The 1x1 maximum is {ms(w1o['maximum_ms'])} ms ({ratio(w1o['margin'])[:-1]}x floor ratio).\n\n"
         "| Shape |",
         f"The 1x1 maximum is {ms(w1n['maximum_ms'])} ms ({ratio(w1n['margin'])[:-1]}x floor ratio).\n\n"
         "| Shape |"),
    ] + [(row(old, *r), row(new, *r)) for r in ROWS] + [
        (f"   The worst 8x8 copy is {ms(w8o['maximum_ms'])} ms across both arms.\n",
         f"   The worst 8x8 copy is {ms(w8n['maximum_ms'])} ms across both arms.\n"),
        (f"   Its ratio to the guaranteed 49 ms floor is {ratio(w8o['margin'])}.\n"
         f"   The 24.5 ms margin is {LIMIT_MS - w8o['maximum_ms']:.5f} ms.\n",
         f"   Its ratio to the guaranteed 49 ms floor is {ratio(w8n['margin'])}.\n"
         f"   The 24.5 ms margin is {LIMIT_MS - w8n['maximum_ms']:.5f} ms.\n"),
        (f"   The 1x1 maximum is {ms(w1o['maximum_ms'])} ms ({ratio(w1o['margin'])[:-1]}x floor ratio).\n",
         f"   The 1x1 maximum is {ms(w1n['maximum_ms'])} ms ({ratio(w1n['margin'])[:-1]}x floor ratio).\n"),
        (f"   The 100 MHz 8x8 comparison is non-contract: {ms(c8o['maximum_ms'])} ms maximum.\n",
         f"   The 100 MHz 8x8 comparison is non-contract: {ms(c8n['maximum_ms'])} ms maximum.\n"),
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
for key, m in sorted(mn.items()):
    print('MAXIMUM', key, ms(m['maximum_ms']), ratio(m['margin']), 'margin to limit',
          f"{LIMIT_MS - m['maximum_ms']:.5f} ms")
