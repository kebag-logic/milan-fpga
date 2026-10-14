"""Recompute section 18's per-arm table, maxima, margins and binding lines from the receipt.

Usage: python3 -I section18_vs_receipt.py <receipt.json> <SAVED_STATE_SNAPSHOT_OWNERSHIP.md>
"""
import json
import sys

r = json.load(open(sys.argv[1]))
doc = open(sys.argv[2]).read()
need = []
for a in r['measurements']:
    ms = [row['sys_cycles'] / a['sys_hz'] * 1000 for row in a['rows']]
    shape = '8x8' if '8x8' in a['shape'] else '1x1'
    basis = 'contract' if a['cpu_hz'] == 50_000_000 else 'non-contract'
    need.append(f"| {shape} | {a['cpu_hz'] // 1_000_000} / {a['sys_hz'] // 1_000_000}, {basis} | "
                f"{a['traffic'].upper()} | {min(ms):.5f} to {max(ms):.5f} | {49 / max(ms):.4f}x |")
worst = max(m['maximum_ms'] for m in r['maxima'] if m['shape'].endswith('8x8') and m['cpu_hz'] == 50_000_000)
need += [f'**The worst 8x8 measurement is {worst:.5f} ms.**',
         f'Its floor ratio is {49 / worst:.4f}x.',
         f'The margin to 24.5 ms is {24.5 - worst:.5f} ms.',
         f"Measured commit: `{r['base']}`.", f"Measured tree: `{r['tree']}`.",
         f"Firmware SHA-256: `{r['product_firmware_sha256']}`.",
         f"Protocol-processor pin: `{r['processor_pins']['protocol-processor']}`.",
         f"gPTP-processor pin: `{r['processor_pins']['gptp-processor']}`.",
         f"Timing. MEASURED on {r['date']} in the",
         f"({r['remeasurement_assignment']})"]
bad = [n for n in need if n not in doc]
for n in need:
    print('OK ' if n not in bad else 'MISSING', n)
print('SECTION18_MATCHES_RECEIPT' if not bad else 'SECTION18_DIFFERS')
