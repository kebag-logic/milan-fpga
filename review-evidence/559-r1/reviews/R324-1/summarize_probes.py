#!/usr/bin/env python3
"""Summarize R324-1 probe capture logs into probe_summary.json (stdlib only)."""
import json
import re
from pathlib import Path

PKT = Path(__file__).resolve().parent
ARMS = {
    'b8x8_100': '8x8, CPU/system 100/100 MHz, traffic ON (unmodified head; control)',
    'b8x8_100_nt': '8x8, CPU/system 100/100 MHz, traffic OFF (harness no-traffic arm)',
    'b8x8_50': '8x8, CPU/system 50/100 MHz, traffic ON',
    'b8x8_50_nt': '8x8, CPU/system 50/100 MHz, traffic OFF',
    'b8x8_50_phase': '8x8, CPU/system 50/100 MHz, traffic ON, CPU rising edges aligned to sys rising edges',
}
out = {}
for arm, text in ARMS.items():
    raw = (PKT / 'receipts/probes' / arm / 'capture.log').read_text(errors='replace')
    rows = [dict((k, int(v)) for k, v in re.findall(r'(\w+)=(\d+)', m))
            for m in re.findall(r'CAPTURE index=[^\n]*', raw)]
    spec = json.loads((PKT / 'receipts/probes' / arm / 'spec.json').read_text())
    ms = [r['sys_cycles'] / spec['sys_hz'] * 1000 for r in rows]
    out[arm] = dict(arm=text, cpu_hz=spec['cpu_hz'], sys_hz=spec['sys_hz'],
                    captures=len(rows), all_ok=all(r['ok'] == 1 and r['mismatches'] == 0
                                                   and r['open'] == 0 for r in rows),
                    sys_cycles=[r['sys_cycles'] for r in rows],
                    max_ms=max(ms), margin_vs_50ms=50 / max(ms),
                    fraction_of_25ms_bar=max(ms) / 25,
                    traffic=[(r['requests'], r['responses'], r['reads']) for r in rows])
(PKT / 'receipts/probe_summary.json').write_text(json.dumps(out, indent=2) + '\n')
for arm, row in out.items():
    print(f"{arm:14s} cpu={row['cpu_hz']//1000000:3d}MHz n={row['captures']} ok={row['all_ok']} "
          f"cycles={row['sys_cycles']} max={row['max_ms']:.5f} ms margin={row['margin_vs_50ms']:.4f}x "
          f"bar={row['fraction_of_25ms_bar']:.4f} traffic={row['traffic']}")
