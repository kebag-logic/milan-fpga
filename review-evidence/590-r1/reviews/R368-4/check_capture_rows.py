#!/usr/bin/env python3
"""Compare the merge-dev capture arms with the committed capture receipt.

Usage: check_capture_rows.py <author-mergedev dir> <repo at exact head> <out.json>
Each of the six arms' measurement JSON must equal, field for field, the
same fields of the receipt measurement with the same shape, CPU clock and traffic arm; the
receipt maxima must be the per-shape/clock maxima of those rows; each arm's
compiled source list must include the two RTL files the merge changed.
"""
import json, sys
from pathlib import Path

pk, repo, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
rec = json.loads((repo / 'tb/verilator/nvm_capture_cpu/measurements.json').read_text())
arms = [(s, c, t) for s, c in (('1x1', 50), ('8x8', 50), ('8x8', 100)) for t in ('on', 'off')]
SH = {'1x1': 'endstation_ax7101_1x1_tdm8', '8x8': 'endstation_ax7101_8x8'}
report, ok = {}, True
for s, c, t in arms:
    m = json.loads((pk / f'native-evidence/capture-{s}-{c}-{t}.json').read_text())
    r = [x for x in rec['measurements'] if x['shape'] == SH[s] and x['cpu_hz'] == c * 10**6 and x['traffic'] == t]
    # the receipt adds identity fields (netlist, firmware, BIOS, ROM, config, command)
    equal = len(r) == 1 and all(r[0].get(k) == v for k, v in m.items())
    extra = sorted(set(r[0]) - set(m)) if len(r) == 1 else []
    src = json.loads((pk / f'native-evidence/capture-{s}-{c}-{t}-sources.json').read_text())
    srcs = src.get('sources', src) if isinstance(src, dict) else src
    names = [str(x) for x in srcs]
    has = {f: any(n.endswith(f) for n in names) for f in ('hdl/milan/KL_pp_shadow.sv', 'hdl/milan/milan_datapath.sv')}
    rows_ok = all(x['ok'] == 1 and x['mismatches'] == 0 and x['open'] == 0 for x in m['rows']) and len(m['rows']) == 16
    report[f'{s}-{c}-{t}'] = dict(equal_receipt=equal, receipt_only_fields=extra, captures=len(m['rows']), rows_ok=rows_ok, max_ms=m['maximum_ms'],
                                   min_ms=m['minimum_ms'], n_sources=len(names), compiles_changed_rtl=has)
    ok &= equal and rows_ok and all(has.values())
    print(f'{s}-{c}-{t}: receipt-equal={equal} captures={len(m["rows"])} rows_ok={rows_ok} '
          f'min={m["minimum_ms"]} max={m["maximum_ms"]} sources={len(names)} changed-RTL={has}')
for mx in rec['maxima']:
    got = max(x['maximum_ms'] for x in rec['measurements'] if x['shape'] == mx['shape'] and x['cpu_hz'] == mx['cpu_hz'])
    good = abs(got - mx['maximum_ms']) < 1e-9 and abs(49 / got - mx['margin']) < 1e-9
    print('receipt maximum', mx['shape'], mx['cpu_hz'], mx['maximum_ms'], 'consistent' if good else 'INCONSISTENT')
    ok &= good
m8 = next(m for m in rec['maxima'] if m['shape'] == SH['8x8'] and m['cpu_hz'] == 50_000_000)['maximum_ms']
report['8x8_50_margin_to_24_5_ms'] = round(24.5 - m8, 5)
report['gain_over_24_30246_ms'] = round(24.30246 - m8, 5)
print('8x8@50 max', m8, 'margin to 24.5 ms', report['8x8_50_margin_to_24_5_ms'], 'gain', report['gain_over_24_30246_ms'])
json.dump(report, open(out, 'w'), indent=1)
print('RESULT', 'PASS' if ok else 'FAIL')
sys.exit(0 if ok else 1)
