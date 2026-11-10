#!/usr/bin/env python3
"""Round 25 (#665): the figures the docs, the handoff and the STOP quote, read from the gate at a checkout.

usage: python3 -I round25_numbers.py CHECKOUT

Prints, per point: both columns' loads, the compute factor for 0.70, the pass's own cost, the graded terms by share;
at each held point over 0.70, the top three graded terms and what each alone would need (its cost, or its source's
period, to bring the point to 0.70); and the costs tsn-c-stack#32 moves (pin -> donor, the stated() values).
"""
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
import load_grade as L  # noqa: E402

for point in L.POINTS:
    pin, don = L.load(root, point, L.STATED_US), L.load(root, point, L.STATED_US_DONOR)
    tp, td = sum(pin.values()), sum(don.values())
    ranked = sorted(don.items(), key=lambda t: -t[1])
    print(f'{point}: pin {tp:.3f} donor {td:.3f} compute {max(1.0, td / 0.70):.2f}x own '
          f'{L.pass_own_us(root, point, L.STATED_US_DONOR):.0f} (pin own {L.pass_own_us(root, point, L.STATED_US):.0f})')
    print('   graded terms: ' + ', '.join(f'{t} {v:.3f}' for t, v in ranked))
    print('   pin terms:    ' + ', '.join(f'{t} {v:.3f}' for t, v in sorted(pin.items(), key=lambda t: -t[1])))
    if td > 0.70:
        need = td - 0.70
        print(f'   over 0.70 by {need:.3f}; the top three, each alone:')
        c = L.stated(root, point, L.STATED_US_DONOR)
        k = L.contract(root)
        for term, v in ranked[:3]:
            left = v - need
            if term == 'srp':
                per = 1 / k['refill']['srp'] + 1 / k['tick_ms']  # the record and the retry at the record's cost
                cost = left * 1000 / per
                rec_part = c['record.srp'] / k['refill']['srp'] / 1000
                retry = c['item.retained'] / k['tick_ms'] / 1000
                refill = c['record.srp'] / ((left - retry) * 1000) if left > retry else float('inf')
                print(f'     srp {v:.3f} (records {rec_part:.3f}, retries {retry:.3f}) -> {left:.3f}: an SRP record '
                      f'(and its retry) {c["record.srp"]:.0f} -> {cost:.0f} us ({cost / c["record.srp"] - 1:+.0%}), or '
                      f'SRP refill {k["refill"]["srp"]} -> {refill:.2f} ms')
            elif term == 'item.aecp':
                frame = max(c['item.aecp.response'], c['item.aecp.notice'])
                probes = L.POINTS[point]['n_if'] * L.POINTS[point]['registrations'] * c['item.aecp.probe'] / \
                    L.probe_retry_ms(root) / 1000
                rec = (left - probes) * 1000 * k['refill']['aecp']
                print(f'     item.aecp {v:.3f} (records {frame / k["refill"]["aecp"] / 1000:.3f}, probes {probes:.3f})'
                      f' -> {left:.3f}: a record\'s owed frame {frame:.0f} -> {rec:.0f} us '
                      f'({rec / frame - 1:+.0%}), or AECP refill {k["refill"]["aecp"]} -> '
                      f'{frame / ((left - probes) * 1000):.1f} ms')
            elif term.startswith('rec.'):
                ch = term[4:]
                cost = left * 1000 * k['refill'][ch]
                print(f'     {term} {v:.3f} -> {left:.3f}: a {ch} record {c["record." + ch]:.0f} -> {cost:.0f} us '
                      f'({cost / c["record." + ch] - 1:+.0%}), or {ch} refill {k["refill"][ch]} -> '
                      f'{c["record." + ch] / (left * 1000) if left > 0 else float("inf"):.1f} ms')
            else:
                print(f'     {term} {v:.3f} -> {left:.3f} ({left / v - 1:+.0%} of the term)')
    a, b = L.stated(root, point, L.STATED_US), L.stated(root, point, L.STATED_US_DONOR)
    moved = [(key, a.get(key), b[key]) for key in sorted(b) if a.get(key) != b[key]]
    print('   costs moved by the donor (pin -> donor): ' + ', '.join(f'{key} {x} -> {y}' for key, x, y in moved))
