#!/usr/bin/env python3
"""R368-3 probe: the per-line dispatch oracle on real kept native logs.

Usage: python3 -B per_line_oracle_probe.py <repo-root> <author-r3 packet dir>
For the kept positive queued-builtins and queued-short raw logs (both shapes),
regrade with head code, then plant tick_calls=0 on exactly one console row
(first, middle, last): service_findings must name exactly that row and nothing
else, and report_verdict('none') must refuse. Also a queued-input run (plan
outside the per-line scope) is shown for contrast.
"""
from pathlib import Path
import contextlib, copy, io, json, sys

root = Path(sys.argv[1]).resolve(); pkt = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(root / 'tb/verilator/fw_service_budget'))
import run  # noqa: E402

def load(stem):
    d = pkt / 'native-evidence-raw'
    p = d / (stem + '-raw.log')
    if not p.exists():
        p = pkt / 'native-evidence' / (stem + '-raw.log')
    rec_p = d / (stem + '-receipt.json')
    if not rec_p.exists():
        rec_p = pkt / 'native-evidence' / (stem + '-receipt.json')
    return p.read_text(), json.loads(rec_p.read_text())

for stem in ('service-1x1-queued-builtins', 'service-8x8-queued-builtins',
             'service-1x1-queued-short', 'service-8x8-queued-short', 'service-8x8-queued-input'):
    raw, rec = load(stem)
    base = dict(media=rec['media'], shape=rec['shape'])
    base.update(run.grade(raw, rec['media']))
    clean = run.service_findings(base, raw)
    lines = [i for i, r in enumerate(base['rows']) if 'command_index' in r]
    print(f'{stem}: console rows={len(lines)} clean findings={len(clean)}')
    for pick in (lines[0], lines[len(lines) // 2], lines[-1]):
        res = copy.deepcopy(base)
        res['rows'][pick]['tick_calls'] = 0
        got = run.service_findings(res, raw)
        want = 'console line lacks a dispatch opportunity: ' + res['rows'][pick]['duty']
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                run.report_verdict('none', got, False)
            verdict = 'ACCEPTED'
        except Exception:  # noqa: BLE001
            verdict = 'refused'
        print(f'   plant row {pick} ({res["rows"][pick]["duty"]!r}): findings={got} exact={got == [want]} verdict_none={verdict}')
