#!/usr/bin/env python3
"""Cross-checks of review round R968-1 (PR #1026, head 12ab4b18): the figures the tree states at the arty-4x4 point,
recomputed from the author's published receipts and from the rules the tree cites. Read-only.

usage: python3 -I crosscheck.py CLONE EVIDENCE_AUTHOR_DIR
  CLONE                the reviewed checkout
  EVIDENCE_AUTHOR_DIR  review-evidence/arty4x4-r1/author of evidence commit 1994a795
"""
from __future__ import annotations

import json
import math
import os
import re
import sys
from decimal import ROUND_CEILING, Decimal
from pathlib import Path

OUT: list[tuple[bool, str]] = []


def check(ok: bool, text: str) -> None:
    OUT.append((bool(ok), text))


def main(argv: list[str]) -> int:
    clone, ev = Path(argv[0]), Path(argv[1])
    d = clone / 'tb/verilator/ctrl_service_budget'
    sys.path.insert(0, str(d))
    import edit_rows
    import egress_ledger
    import egress_mii
    import load_grade
    import poll_grade
    import rows_grade
    import rows_tiers
    import shape_costs

    # 1. The held-egress ledger: 60 ms hold + 1.05 x service, up to 0.01 ms, from the qualification receipt's rows.
    qual = json.loads((ev / 'round3/receipts/qualification.json').read_text())
    rows = qual['held_egress']['rows']
    rule = {n: float(60 + ((Decimal(str(ms)) - 60) * Decimal('1.05')).quantize(Decimal('0.01'), ROUND_CEILING))
            for n, ms in rows.items()}
    check(rows == egress_ledger.ARTY_4X4, f'ARTY_4X4 is the qualification receipt\'s seven held-egress rows: {rows}')
    check(rule == egress_ledger.LEDGER['arty-4x4'], f'LEDGER[arty-4x4] is the rule applied to them: {rule}')
    check(max(rule.values()) == 63.50 and min(rule.values()) == 61.65, 'the ledger spans 61.65 to 63.50 ms')
    doc = (clone / 'docs/design/SPLIT_CONTROL_MEMORY.md').read_text()
    figures, measured = egress_ledger.arty_doc(doc, 'arty-4x4')
    check(figures == rule and measured == rows, "section 15's 4x4 table states the same measurements and figures")

    # 2. The qualification receipt against the tree's model and section 15's table.
    model = qual['model']
    check(qual['status'] == 'PASS' and qual['groups'] == 159 and not qual['findings']
          and len(qual['regrade_returncodes']) == 8 and not any(qual['regrade_returncodes'].values()),
          'qualification receipt: PASS, 159 groups, no finding, eight variant regrades rc 0')
    check((round(model['load'], 4), model['rows_ms']['ACMP'], model['rows_ms']['txL'], model['rows_ms']['last'])
          == (0.4689, 28.52, 48.72, 117.68), 'receipt model: load 0.4689, ACMP 28.52, txL 48.72, last 117.68 ms')
    check(model['load'] <= 0.70 and model['rows_ms']['ACMP'] <= 30 and model['rows_ms']['txL'] <= 49
          and model['rows_ms']['last'] <= 140, 'each is within its owner bound (0.70, 30, 49, 140 ms)')
    check(qual['worst_pass']['cycles'] == 173322 and qual['worst_pass']['cycles'] / qual['cpu_hz'] * 1e3 < 2,
          'longest whole pass 173,322 cycles at 100 MHz = 1.733 ms, under THE SHARE 2 ms')
    for cell in ('| Long-window load | 0.4689 | 0.70 |', '| ACMP | 28.52 ms | 30 ms |', '| txL | 48.72 ms | 49 ms |',
                 '| Last queued notice | 117.68 ms | 140 ms |', '| Longest whole pass | 173322 cycles, 1.733 ms | 2 ms |',
                 '| 100 Mb/s egress, wait with gPTP x 1.05 + fixed path | 527.04 us | 1000 us |'):
        check(cell in doc, f'section 15 states {cell}')
    census = json.loads((ev / 'round3/receipts/census4-completed.json').read_text())
    check(len(census) == 159 and all(c['native_status'] == 0 and not (c['refusals'] or c['share'] or c['late'])
                                     for c in census),
          'census-4 receipt: 159 cases, native status 0, no refusal, share or late finding')
    missed = {(c['variant'], c['group']): c['misses'] for c in census if c['misses']}
    check(list(missed) == [('none', 'backlog-owed')] and
          sorted(m.split(':')[0] for m in missed['none', 'backlog-owed']) == sorted(rows),
          'census-4 receipt: the only budget misses are backlog-owed\'s seven ledger rows')
    cycles = {o['probe']: o['sys_cycles'] for c in census if c['group'] == 'backlog-owed' for o in c['over_budget']}
    check({n: c / 100_000 for n, c in cycles.items()} == rows,
          'census-4 receipt: each row\'s bus cycles at 100 MHz are the ledger\'s measurement, e.g. 6,264,658 = 62.64658 ms')
    owed = sorted({c['group'] for c in census if c['stated']})
    check(owed == ['srp-bound', 'srp-kept'], f'census-4 receipt: lines over their statements only in {owed} (#969, #1022)')
    check(max(c['worst_pass_cycles'] for c in census) == 173322, 'census-4 receipt: the worst pass is 173,322 cycles')

    # 3. The stated costs against the merged census receipt (measurement + 5 %, up to 5 us).
    merged = json.loads((ev / 'round3/receipts/merged234-969.json').read_text())['costs']
    by_rule = {k: v['rule_us'] for k, v in merged.items()}
    recomputed = {k: int(math.ceil(v['cycles'] / 100 * 1.05 / 5 - 1e-9) * 5) for k, v in merged.items()}
    check(recomputed == by_rule, 'merged receipt: every rule_us is cycles/100 x 1.05 rounded up to 5 us')
    stated = load_grade.STATED_US['arty-4x4']
    pairs = {'record.srp': 'record.srp', 'record.aecp': 'record.aecp.other', 'record.acmp': 'record.acmp',
             'record.adp': 'record.adp', 'record.maap': 'record.maap', 'event.ADP': 'event.TIMER#0',
             'event.ACMP': 'event.TIMER#1', 'event.MAAP': 'event.TIMER#2', 'event.AECP': 'event.TIMER#3',
             'event.TICK': 'event.TICK', 'event.GM': 'event.GM', 'centisecond': 'centisecond',
             'events_none': 'events_none', 'item.retained': 'item.record', 'item.aecp.notice': 'tx.aecp.notice',
             'item.aecp.response': 'tx.aecp.response'}
    bad = {k: (stated[k], by_rule[v]) for k, v in pairs.items() if stated[k] != by_rule[v]}
    check(not bad, f'load_grade.STATED_US[arty-4x4] equals the receipt for {len(pairs)} terms {bad or ""}')
    check(load_grade.STATED_US_DONOR['arty-4x4'] == stated, 'STATED_US_DONOR[arty-4x4] is the same table')
    polls = poll_grade.STATED_US[shape_costs.Shape(1, 5, 5)]
    pp = {'base': 'base', 'withdraw': 'item.withdraw', 'rebuild': 'item.rebuild', 'walk': 'item.walk',
          'reclaim': 'item.reclaim', 'retained': 'item.record', 'mrpdu': 'item.mrpdu', 'acmp': 'item.acmp',
          'aecp': 'item.aecp', 'aecp_long': 'item.aecp_long', 'acmp_declined': 'item.acmp_declined'}
    bad = {k: (polls[k], by_rule[v]) for k, v in pp.items() if polls[k] != by_rule[v]}
    check(not bad, f'poll_grade.STATED_US[(1,5,5)] equals the receipt for {len(pp)} terms {bad or ""}')
    dp = rows_tiers.DATAPATH_US['arty-4x4']
    check(dp == {k: by_rule[f'event.{k}'] for k in dp}, f'rows_tiers.DATAPATH_US[arty-4x4] equals the receipt: {dp}')
    check(rows_tiers.LONG_RECORD_US['arty-4x4'] == by_rule['record.aecp.long'] == 890, 'LONG_RECORD_US is 890 us')
    check(rows_grade.ROW_COSTS['arty-4x4']['event.LINK'] == by_rule['event.LINK'] == 200, 'event.LINK is 200 us')
    check(edit_rows.PACED['arty-4x4'] == {'a one-row edit': by_rule['paced.45'],
                                         'an accepted SET_CONFIGURATION': by_rule['paced.6']},
          f"edit_rows.PACED[arty-4x4] equals the receipt: {edit_rows.PACED['arty-4x4']}")
    listed = shape_costs.at(shape_costs.Shape(1, 5, 5), clone)
    hh = {'CTRL_LOOP_BUILD_PASS_US': 'build', 'CTRL_LOOP_BUILD_ONE_PASS_US': 'build_one',
          'CTRL_LOOP_SRP_UNIT_US': 'record.srp', 'CTRL_LOOP_STEP_PASS_US': 'step', 'CTRL_LOOP_TICK_US': 'centisecond'}
    bad = {k: (listed[k], by_rule[v]) for k, v in hh.items() if listed[k] != by_rule[v]}
    check(not bad, f'ctrl_loop.h (1,5,5) equals the receipt for {len(hh)} statements {bad or ""}')
    check(by_rule['share'] == 1820 and merged['share']['cycles'] == 173322, 'the pass by the rule is 1,820 us, under 2,000')

    # 4. The transmit bound is read through an integer division: 28 and 29 ms give the same hold-off term.
    src = (clone / 'sw/firmware/ctrl/srp/srp_mbx.c').read_text()
    check('(CTRL_LOOP_TX_MS + 9u) / 10u' in src and (28 + 9) // 10 == (29 + 9) // 10 == 3,
          'SRP_REDECLARE_CS reads CTRL_LOOP_TX_MS as (TX + 9) / 10: 3 cs at 28 and at 29 ms')
    check(listed['CTRL_LOOP_TX_MS'] == 29 <= 240 - 10 * 19 - 1, 'CTRL_LOOP_TX_MS 29 <= CTRL_LOOP_TX_BOUND_MS 49')

    # 5. The 100 Mb/s egress row and its stream load.
    p = egress_mii.params(dict(shape='endstation_arty_split_4x4', sys_hz=100_000_000, milan_hz=50_000_000))
    check(p.sr_bytes == (90, 90, 90, 90, 46), f'the 4x4 SR load is four 90-octet frames and the 46-octet CRF: {p.sr_bytes}')
    gptp_us = egress_mii.gptp_wire_ps(p) / 1e6
    row = (446.76 + gptp_us) * 1.05 + egress_mii.MII_FIXED_NS / 1000
    check(abs(gptp_us - 54.88) < 1e-9, f'one gPTP burst is {gptp_us:.2f} us on the wire')
    check(f'{row:.2f}' == '527.04', f'(446.76 + {gptp_us:.2f}) x 1.05 + {egress_mii.MII_FIXED_NS / 1000} = {row:.3f} us')
    check(f'{(446.76 + gptp_us) * 1.05 + 0.300:.2f}' == '527.02', 'with the measured 300 ns it would read 527.02 us')
    burst_us = sum(p.wire_ps(b) + p.gap_octets * p.octet_ps for b in p.sr_bytes) / 1e6
    check(burst_us < 125, f'the five SR frames of one interval take {burst_us:.2f} us of 125 us on the wire')

    # 6. The bind bounds by PR #1004's rule from the census's save-bind group.
    save = 353.671 - 100
    check(math.ceil(2 * save / 50) * 50 == 550 and math.floor((630 - 100) / save) + 2 == 4,
          f'2 x {save:.3f} = {2 * save:.3f} ms, up to 50 ms: 550; floor(530 / {save:.3f}) + 2 = 4 saves')

    # 7. The 100 Mb/s class A envelope (kb/s at 8,000 frames a second).
    aaf = lambda ch, samples: (24 + ch * samples * 4 + 43) * 64  # noqa: E731
    crf = (46 + 42) * 64
    check((aaf(2, 6), aaf(8, 6), aaf(8, 12), aaf(8, 24), crf) == (7360, 16576, 28864, 53440, 5632),
          'per-stream figures: 7,360 / 16,576 / 28,864 / 53,440 kb/s and the CRF 5,632 kb/s')
    check(4 * aaf(2, 6) + crf == 35072 and 4 * aaf(8, 6) + crf == 71936 <= 75000 < 4 * aaf(8, 12) + crf,
          'egress 35,072 and worst ingress 71,936 kb/s are inside 75,000; four 8-channel 96 kHz inputs are not')

    # 8. The memory ledger against the product size receipt.
    size = json.loads((ev / 'round4/receipts/product-4x4-size.json').read_text())
    sec, split = size['sections'], size['split']
    check((sec['.text'], sec['.rodata'], sec['.bss']) == (114844, 17630, 61104)
          and (split['rom']['RAMB36'] + split['rom']['RAMB18'] / 2, split['sram']['RAMB36'], split['tiles'])
          == (32.5, 17, 49.5) and split['tiles'] <= split['budget_tiles'] == 56,
          'size receipt: .text 114844, .rodata 17630, .bss 61104; ROM 32.5 + SRAM 17 = 49.5 of 56 RAMB36')
    for cell in ('| `.text` | 114844 bytes |', '| ROM allocation (banks 128 and 2 KiB) | 32.5 RAMB36 |',
                 '| Total allocation | 49.5 RAMB36 |'):
        check(cell in doc, f'section 15 states {cell}')

    # 9. The route grading receipt.
    route = json.loads((ev / 'round3/receipts/routefinal-graded-images.json').read_text())
    for cand in route['candidates']:
        wns = min(c['timing']['wns'] for c in cand['corners'])
        whs = min(c['timing']['whs'] for c in cand['corners'])
        failing = sum(c['timing']['failing_endpoints'] + c['timing']['failing_hold_endpoints'] for c in cand['corners'])
        floor = wns >= 0.030 and whs >= 0 and not failing
        check((cand['status'] == 'PASS') == floor and len(cand['corners']) == 4,
              f"{cand['directive']}: four corners, worst WNS {wns:+.3f} ns, worst WHS {whs:+.3f} ns, {failing} failing "
              f"endpoint(s): the #818 floor is {'met' if floor else 'missed'} ({cand['status']})")
    check(route['firmware']['sha256'] == size['artifacts'][2]['sha256'],
          f"the routed image's ELF is the size receipt's ({route['firmware']['sha256'][:16]}...)")

    # 10. Receipts the author's indexes name that the published packet does not carry.
    for rnd in ('round1', 'round3', 'round4'):
        index = (ev / rnd / 'receipts/INDEX.md').read_text()
        named = re.findall(r'^\| `([^`]+)` \| \d+ \| `[0-9a-f]{64}`', index, re.M)
        have = {os.path.relpath(os.path.join(r, f), ev / rnd / 'receipts')
                for r, _, fs in os.walk(ev / rnd / 'receipts') for f in fs}
        absent = [n for n in named if n not in have]
        OUT.append((True, f'NOTE {rnd}: {len(named)} receipts indexed, {len(absent)} of them not in the published '
                          f'packet, all compressed: {all(n.endswith(".gz") for n in absent)}'))
    for ok, text in OUT:
        print(('OK   ' if ok else 'FAIL ') + text)
    print(f'crosscheck: {sum(ok for ok, _ in OUT)} of {len(OUT)} hold')
    return int(not all(ok for ok, _ in OUT))


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
