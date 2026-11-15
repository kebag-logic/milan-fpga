#!/usr/bin/env python3
"""The AECP record per group of budget-harness legs: every aecp_mbx:frame SPAN (the record handler, aecp_mbx.c frame;
the span parts.py's record.aecp and measured_inputs.py read), each matched to the AECP command it handled.

usage: python3 -I aecp_records.py TREE OUT.json RESULTS_DIR...

A group's script (<group>.txt) sends its frames in order ('frame <if> <hex>' lines); the testbench logs each frame it
injects as RXS (bus cycle, interface, length, probe label or '-') and its delivery to a channel as RXC (bus cycle,
channel). The n-th RXS is the n-th script frame. AECP's records are handled in ring order, so the n-th aecp_mbx:frame
span is the n-th RXC on AECP's channel (checked: the counts must agree and each RXC must precede its span). Each record
is held against the stated cost of its group: rows_tiers.LONG_RECORD_US for aecp-largest-notice (the largest legal
command's records, LONG_ROWS), load_grade.GRADED's record.aecp otherwise (also STATED_US's, the pin column). Only logs
that end in a RESULT line are read, as parts.py reads them.
"""
import json
import os
import math
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / 'tb/verilator/ctrl_service_budget'))
import load_grade  # noqa: E402
import rows_tiers  # noqa: E402
import grade  # noqa: E402
import scenario  # noqa: E402

AECP = scenario.CH['aecp']
POINT = os.environ.get('AECP_RECORDS_POINT', '1x1/1if')  # #894 round 12: any point
GRADED = load_grade.GRADED[POINT]['record.aecp']
PIN = load_grade.STATED_US[POINT]['record.aecp']
LONG = rows_tiers.LONG_RECORD_US[POINT]
LONG_GROUP = 'aecp-largest-notice'
AEM = {0x00: 'ACQUIRE_ENTITY', 0x01: 'LOCK_ENTITY', 0x02: 'ENTITY_AVAILABLE', 0x03: 'CONTROLLER_AVAILABLE',
       0x04: 'READ_DESCRIPTOR', 0x05: 'WRITE_DESCRIPTOR', 0x06: 'SET_CONFIGURATION', 0x07: 'GET_CONFIGURATION',
       0x08: 'SET_STREAM_FORMAT', 0x09: 'GET_STREAM_FORMAT', 0x0E: 'SET_STREAM_INFO', 0x0F: 'GET_STREAM_INFO',
       0x10: 'SET_NAME', 0x11: 'GET_NAME', 0x12: 'SET_ASSOCIATION_ID', 0x13: 'GET_ASSOCIATION_ID',
       0x14: 'SET_SAMPLING_RATE', 0x15: 'GET_SAMPLING_RATE', 0x16: 'SET_CLOCK_SOURCE', 0x17: 'GET_CLOCK_SOURCE',
       0x18: 'SET_CONTROL', 0x19: 'GET_CONTROL', 0x24: 'REGISTER_UNSOLICITED_NOTIFICATION',
       0x25: 'DEREGISTER_UNSOLICITED_NOTIFICATION', 0x26: 'IDENTIFY_NOTIFICATION', 0x27: 'GET_AVB_INFO',
       0x28: 'GET_AS_PATH', 0x29: 'GET_COUNTERS', 0x2A: 'REBOOT', 0x2B: 'GET_AUDIO_MAP', 0x2C: 'ADD_AUDIO_MAPPINGS',
       0x2D: 'REMOVE_AUDIO_MAPPINGS', 0x4B: 'GET_DYNAMIC_INFO'}


def rule(cycles: int) -> int:
    """The stated cost in us by the cost tools' rule: cycles at 100 MHz, plus 5 %, rounded up to 5 us."""
    return int(math.ceil(cycles * 1.05 / 100 / 5 - 1e-9) * 5)


def describe(hexframe: str) -> str:
    b = bytes.fromhex(hexframe)
    if len(b) < 38 or b[12:14] != b'\x22\xf0' or b[14] != 0xFB:
        return f'non-AECP subtype 0x{b[14]:02x}' if len(b) > 14 else 'short frame'
    mt = b[15] & 0x0F
    if mt == 0:
        ct = ((b[36] << 8) | b[37]) & 0x7FFF
        return f'AEM_COMMAND {AEM.get(ct, "0x%04x" % ct)}'
    return f'AECP message_type {mt}'


def group_records(log: Path) -> dict:
    text = log.read_text(errors='replace')
    script = log.with_suffix('.txt')
    frames = [l.split()[2] for l in script.read_text().splitlines() if l.startswith('frame ')] if script.is_file() else []
    rxs, rxc, spans = [], [], []
    for line in text.splitlines():
        f = line.split()
        if not f:
            continue
        if f[0] == 'RXS':
            rxs.append((int(f[1]), f[4] if len(f) > 4 else '-'))
        elif f[0] == 'RXC':
            rxc.append((int(f[1]), int(f[2]), len(rxs) - 1))
        elif f[0] == 'SPAN' and f[-1] == 'aecp_mbx:frame':
            spans.append((int(f[1]), int(f[3])))
    aecp_rxc = [r for r in rxc if r[1] == AECP]
    paired = len(aecp_rxc) == len(spans) and all(r[0] <= s[0] for r, s in zip(aecp_rxc, spans))
    # the device's AECP commits (grade.Log.tx, as aecp_kinds.py reads them): a record's command is that of the first
    # solicited response (an odd message_type, its u bit clear) committed at or after the record's start
    log_ = grade.parse(text[:text.rfind('\n') + 1], 100_000_000, 100_000_000)
    answers = sorted((c, fr) for c, ch, _i, fr in log_.tx if ch == AECP and len(fr) >= 38 and (fr[15] & 1) == 1
                     and not (fr[15] & 0x0F == 1 and fr[36] & 0x80))
    records = []
    for n, (start, cycles) in enumerate(spans):
        label, frame_cmd = '-', '?'
        if paired:
            k = aecp_rxc[n][2]
            label = rxs[k][1] if 0 <= k < len(rxs) else '-'
            frame_cmd = describe(frames[k]) if len(frames) == len(rxs) and 0 <= k < len(frames) else '?'
        resp = next((fr for c, fr in answers if c >= start), None)
        if resp is None:
            answered = 'no response'
        elif resp[15] & 0x0F == 1:
            ct = ((resp[36] << 8) | resp[37]) & 0x7FFF
            answered = f'AEM_COMMAND {AEM.get(ct, "0x%04x" % ct)}'
        else:
            answered = f'AECP message_type {resp[15] & 0x0F}'
        agree = frame_cmd in ('?', answered)
        what = answered + (f' ({label})' if label != '-' else '') + ('' if agree else f' [script: {frame_cmd}]')
        records.append(dict(n=n, sys=start, cycles=cycles, command=what, label=label, frame_cmd=frame_cmd,
                            answered=answered, agree=agree))
    return dict(records=records, paired=paired, rxs=len(rxs), frames=len(frames), aecp_rxc=len(aecp_rxc),
                spans=len(spans))


def main() -> None:
    out = {}
    for d in map(Path, sys.argv[3:]):
        for log in sorted(d.glob('*.log')):
            text = log.read_text(errors='replace')
            if 'RESULT' not in text[-4000:]:
                continue
            g = group_records(log)
            name = log.stem
            stated = LONG if name == LONG_GROUP else GRADED
            top = max(g['records'], key=lambda r: r['cycles']) if g['records'] else None
            # the group's ordinary records too: in the long group, those under the largest legal command's
            out[f'{d.parent.name}/{d.name}/{name}'] = dict(
                group=name, records=len(g['records']), paired=g['paired'], stated_us=stated,
                stated_name='rows_tiers.LONG_RECORD_US' if name == LONG_GROUP else 'load_grade.GRADED record.aecp',
                most=top, most_us=(top['cycles'] / 100 if top else 0), most_rule_us=(rule(top['cycles']) if top else 0),
                over_rule=(rule(top['cycles']) > stated if top else False),
                over_raw=(top['cycles'] / 100 > stated if top else False),
                top5=sorted(g['records'], key=lambda r: -r['cycles'])[:5], all=g['records'], counts={k: g[k] for k in
                                                                                    ('rxs', 'frames', 'aecp_rxc', 'spans')})
    Path(sys.argv[2]).write_text(json.dumps(out, indent=1) + '\n')
    print(f'# stated: load_grade.GRADED record.aecp {GRADED} us (STATED_US pin column {PIN}); '
          f'rows_tiers.LONG_RECORD_US {LONG} us for {LONG_GROUP}; rule = cycles/100 x 1.05 rounded up to 5 us')
    print(f'{"group":34} {"records":>7} {"most cycles":>11} {"us":>7} {"rule":>5} {"stated":>6} over  command')
    for k, v in sorted(out.items(), key=lambda kv: -(kv[1]['most']['cycles'] if kv[1]['most'] else 0)):
        m = v['most']
        if not m:
            print(f'{k:34} {0:>7}')
            continue
        flag = 'OVER' if v['over_raw'] else ('rule' if v['over_rule'] else '-')
        print(f"{k:34} {v['records']:>7} {m['cycles']:>11,} {v['most_us']:>7.2f} {v['most_rule_us']:>5} "
              f"{v['stated_us']:>6} {flag:5} {m['command']}{'' if v['paired'] else ' [unpaired]'}")


if __name__ == '__main__':
    main()
