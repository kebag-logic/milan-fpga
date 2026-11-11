#!/usr/bin/env python3
"""Reviewer probes on the published unloaded wire logs, with the head's grader.

usage: regrade_probes.py <checkout> <receipts/head dir>

P0 regrade each log; compare rows, findings and load with the published results.json.
P1 census: each aecp-get_avb_info command's command_type/descriptor; every ACMP TX and AECP response status.
P2 mutations, each must be found by its own words:
   a  one BIND_RX_RESPONSE's status set to 1
   b  one AEM final response's status set to 2
   c  one MVU final response's status set to 1
   d  SUMMARY rx_frames + 1 (frame equation)
   e  one mid-run PROBE_TX moved after the next draw's bind (pairing by window)
   f  the grade asked for draws + 1 (PROBE_TX count == draws, bind count)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

CHECKOUT = Path(sys.argv[1]).resolve()
HEADDIR = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(CHECKOUT / 'tb/verilator/ctrl_wire_timing'))
import wire_grade as g  # noqa: E402

SYS_HZ = 100_000_000
RUNS = {'ci-1x1-none': 1, '8x8-none': 2}


def mutate_frame(lines, pick, edit):
    """Edit the hex of the first TXW line `pick` selects."""
    out, done = [], False
    for ln in lines:
        w = ln.split()
        if not done and w and w[0] == 'TXW' and pick(bytes.fromhex(w[4])):
            data = bytearray(bytes.fromhex(w[4]))
            edit(data)
            w[4] = data.hex()
            ln = ' '.join(w)
            done = True
        out.append(ln)
    assert done, 'nothing selected'
    return out


def grade(lines, draws, ifs):
    try:
        return g.grade('\n'.join(lines) + '\n', SYS_HZ, draws, ifs, 1)
    except g.Refused as why:
        return None, [f'REFUSED: {why}']


def main() -> int:
    bad = 0
    for run, ifs in RUNS.items():
        text = (HEADDIR / f'{run}__wire.log').read_text()
        lines = text.splitlines()
        meta = json.loads((HEADDIR / f'{run}__run.json').read_text())
        draws = meta['draws']
        pub = json.loads((HEADDIR / f'{run}__results.json').read_text())
        result, findings = grade(lines, draws, ifs)
        same_rows = result['rows'] == pub.get('rows')
        same_load = result['load'] == pub.get('load')
        print(f'P0 {run}: findings {len(findings)} rows-identical {same_rows} load-identical {same_load} '
              f'load {result["load"]}')
        bad += bool(findings) or not same_rows or not same_load
        log = g.parse(text)
        avb = [w for w in log.rx if w.tag.startswith('aecp-get_avb_info')]
        for w in avb:
            ct = int.from_bytes(w.data[36:38], 'big') & 0x7FFF
            dt, di = int.from_bytes(w.data[38:40], 'big'), int.from_bytes(w.data[40:42], 'big')
            cdl = int.from_bytes(w.data[16:18], 'big') & 0x7FF
            print(f'P1 {run}: {w.tag} command_type {ct:#06x} descriptor_type {dt} descriptor_index {di} '
                  f'control_data_length {cdl} frame bytes {len(w.data)}')
            bad += (ct, dt, di) != (0x0027, 9, 0)
        acmp_st = sorted({(w.kind, w.status) for w in log.tx if w.protocol == 'acmp'})
        aecp_st = sorted({(w.kind, w.status) for w in log.tx if w.protocol == 'aecp'})
        print(f'P1 {run}: ACMP TX (message_type, status) {acmp_st}; AECP TX {aecp_st}')
        bad += any(s for _, s in acmp_st) or any(s for _, s in aecp_st)
        # P2 mutations
        is_acmp = lambda d, k: d[12:15] == b'\x22\xf0\xfc' and (d[15] & 0x0F) == k  # noqa: E731
        is_aecp_resp = lambda d, k: d[12:15] == b'\x22\xf0\xfb' and (d[15] & 0x0F) == k  # noqa: E731

        def set_status(v):
            def edit(d):
                d[16] = (d[16] & 0x07) | (v << 3)
            return edit

        cases = {
            'a-bind-status': (mutate_frame(lines, lambda d: is_acmp(d, g.BIND_RX_RESPONSE), set_status(1)),
                              draws, 'carries status 1, not SUCCESS'),
            'b-aem-status': (mutate_frame(lines, lambda d: is_aecp_resp(d, 1), set_status(2)),
                             draws, 'carries status 2, not the 0'),
            'c-mvu-status': (mutate_frame(lines, lambda d: is_aecp_resp(d, 7), set_status(1)),
                             draws, 'carries status 1, not the 0'),
            'd-frame-equation': ([ln.replace(' rx_frames=', ' rx_frames=1', 1) if ln.startswith('SUMMARY') else ln
                                  for ln in lines], draws, 'frames the model received'),
            'f-draws-plus-one': (lines, draws + 1, 'PROBE_TX transactions graded'),
        }
        # e: drop draw 4's PROBE_TX from its window by placing the 5th bind before it (move bind 5 earlier)
        binds = [(i, ln) for i, ln in enumerate(lines) if ln.startswith('RXW') and ' acmp-bind-' in ln]
        probes = [(i, ln) for i, ln in enumerate(lines) if ln.startswith('TXW')
                  and is_acmp(bytes.fromhex(ln.split()[4]), g.PROBE_TX)]
        b4 = int(binds[4][1].split()[1])
        p4 = next(ln for _, ln in probes if int(ln.split()[1]) > b4)
        p4_first = int(p4.split()[1])
        resp4 = next(ln for ln in lines if ln.startswith('TXW') and int(ln.split()[1]) > b4 and
                     is_acmp(bytes.fromhex(ln.split()[4]), g.BIND_RX_RESPONSE))
        r4_last = int(resp4.split()[2])
        moved = []
        i5, ln5 = binds[5]
        w5 = ln5.split()
        width = int(w5[2]) - int(w5[1])
        new_first = (r4_last + p4_first) // 2
        w5[1], w5[2] = str(new_first), str(new_first + width)
        rest = [ln for i, ln in enumerate(lines) if i != i5]

        def cyc(ln):
            w = ln.split()
            try:
                return int(w[5] if w[0] == 'LOAD' else w[1])
            except (IndexError, ValueError):
                return None
        at = next(i for i, ln in enumerate(rest) if (cyc(ln) or -1) > new_first)
        body, tail = rest[:at] + [' '.join(w5)] + rest[at:], []
        cases['e-probe-after-next-bind'] = (body + tail, draws, 'acmp-bind-4 caused no PROBE_TX')
        for name, (mlines, d, words) in cases.items():
            _, fnd = grade(mlines, d, ifs)
            ok = any(words in f for f in fnd)
            print(f'P2 {run} {name}: {"found" if ok else "ESCAPED"}: {[f for f in fnd if words in f][:1] or fnd[:3]}')
            bad += not ok
    print(f'regrade_probes: {bad} failed')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
