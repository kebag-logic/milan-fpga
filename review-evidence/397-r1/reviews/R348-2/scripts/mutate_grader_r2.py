#!/usr/bin/env python3
"""Round-2 mutants of the new grader code (tick spans, bounds, liveness, waits).
usage: mutate_grader_r2.py <tree> <out.json>  (disposable export of the exact head)
Runs the unmutated self-test first as a control, then each single-line mutant."""
import json, subprocess, sys
from pathlib import Path
tree = Path(sys.argv[1]).resolve(); run = tree / 'tb/verilator/fw_service_budget/run.py'
orig = run.read_text()
M = {
 'bound-no-phase': ("row['period_bound_ms'] = 250 + row", "row['period_bound_ms'] = 0 + row"),
 'bound-2000-as-500': ("row['liveness_bound_margin_ms'] = 2000 -", "row['liveness_bound_margin_ms'] = 500 -"),
 'tx-baud-230400': ("tx_bytes * 10_000 / 115200", "tx_bytes * 10_000 / 230400"),
 'tx-owner-none': ("if a['cycle'] <= start and end <= b['cycle']]", "if False]"),
 'tick-drop-internal': ("            spans.append((event['gap_start'], event['gap_start'] + event['max_gap']))\n", "            pass\n"),
 'tick-drop-edge-tail': ("    spans.append((previous, end))\n", ""),
 'tick-drop-leading': ("        spans.append((previous, event['first']))\n", ""),
 'liveness-ppstat-bit5': ("(int(pp[1], 16) >> 6) & 1", "(int(pp[1], 16) >> 5) & 1"),
 'liveness-2000-as-1000': ("liveness_margin_ms=2000 - rows[-1]['ms']", "liveness_margin_ms=1000 - rows[-1]['ms']"),
 'censored-inverted': ("right_censored=gap_end == ends[-1]['cycle']", "right_censored=gap_end != ends[-1]['cycle']"),
 'aem-from-boot': ("interval('aem_copy_crc', aem['cycle']", "interval('aem_copy_crc', 64"),
 'boot-budget-none': ("enable['cycle'], 20000)", "enable['cycle'], None)"),
 'restore-budget-3500': ("walk_end['cycle'], 3000)", "walk_end['cycle'], 3500)"),
 'erase-max-30s': ("0 <= erase_us <= 3_000_000,", "0 <= erase_us <= 30_000_000,"),
 'program-max-50ms': ("0 <= program_us <= 5_000,", "0 <= program_us <= 50_000,"),
 'queued-8x8-twelve': ("(3 if shape == SHAPES[1] else 12)", "(12 if shape == SHAPES[1] else 12)"),
 'wait-sum-first-only': ("wait = sum(e['wait_cycles'] for e in active if e['kind'] == 'flash')", "wait = 0"),
}
def selftest():
    r = subprocess.run([sys.executable, '-B', str(run), '--self-test'], capture_output=True, text=True, cwd=tree)
    return r.returncode, ((r.stdout + r.stderr).strip().splitlines() or [''])[-1][:140]
res = {'control-unmutated': selftest()}
for name, (a, b) in M.items():
    n = orig.count(a)
    if n != 1:
        res[name] = ('PATTERN-COUNT', n); continue
    run.write_text(orig.replace(a, b))
    try: res[name] = selftest()
    finally: run.write_text(orig)
for k, v in res.items():
    tag = 'control' if k.startswith('control') else ('CAUGHT' if v[0] not in (0, 'PATTERN-COUNT') else ('ESCAPED' if v[0] == 0 else 'N/A'))
    print(f'{k:24s} rc={v[0]} {tag} | {v[1]}')
json.dump(res, open(sys.argv[2], 'w'), indent=2)
