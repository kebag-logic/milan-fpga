"""Robustness probe for the round-3 declaration replay (declarations.py).

Usage: python3 -B r3_robustness.py AUTHOR_R3_DIR EVIDENCE_DIR
1. Builds a well-formed MSRP PDU (IEEE 802.1Q 10.8 / 35.2.2) carrying one
   Listener Ready vector and checks the decoded event and Listener value.
2. Every strict truncation and a set of malformed variants must raise
   ValueError (refusal), never decode silently.
3. Checks the three-packed event order against 802.1Q 10.8.2.10
   (New 0, JoinIn 1, In 2, JoinMt 3, Mt 4, Lv 5).
4. Reports how close any DUT Talker Advertise event in the eight published
   talker TSVs lies to the half-open hold-window boundaries.
Exits 1 on any failed check.
"""
import csv
import json
import sys
from pathlib import Path

fails = []


def check(ok, what):
    print(('PASS ' if ok else 'FAIL ') + what)
    if not ok:
        fails.append(what)


def pdu(events_byte=5 * 36, listener_byte=2 * 64, count=1, lva=0):
    first = bytes.fromhex('0200000000010001')
    vec = ((lva << 13) | count).to_bytes(2, 'big') + first + bytes([events_byte]) + bytes([listener_byte])
    body = vec + bytes(2)
    return bytes([0]) + bytes([3, 8]) + len(body).to_bytes(2, 'big') + body + bytes(2)


def main():
    a3, ev = map(Path, sys.argv[1:])
    sys.path.insert(0, str(a3))
    import declarations as d
    good = pdu()
    out = d.decode_msrp(good, 1, 'bridge')
    check([(e['type'], e['event'], e['stream_id'], e['listener']) for e in out]
          == [('Listener', 'Lv', '0200000000010001', '2')], 'well-formed Listener Lv/Ready vector decodes exactly')
    out = d.decode_msrp(pdu(events_byte=0, lva=1), 1, 'bridge')
    check([e['event'] for e in out] == ['LeaveAll', 'New'], 'LeaveAll flag yields a LeaveAll row before the vector events')
    check(d.EVENTS == ('New', 'JoinIn', 'In', 'JoinMt', 'Mt', 'Lv'), 'three-packed event order matches 802.1Q 10.8.2.10')
    order = [d.decode_msrp(pdu(events_byte=v * 36), 1, 'x')[0]['event'] for v in range(6)]
    check(order == list(d.EVENTS), f'each event code decodes to its standard name: {order}')
    refused = silent = 0
    for n in range(1, len(good)):
        try:
            d.decode_msrp(good[:n], 1, 'x')
            silent += 1
            print(f'INFO truncation to {n} bytes decoded without refusal')
        except ValueError:
            refused += 1
        except Exception as error:  # a crash is not a refusal
            silent += 1
            print(f'INFO truncation to {n} bytes raised {type(error).__name__}')
    check(silent == 0, f'all {len(good) - 1} strict truncations refused with ValueError ({refused})')
    bad = {
        'version 1': bytes([1]) + good[1:],
        'unknown attribute type 5': good[:1] + bytes([5]) + good[2:],
        'wrong Listener width': good[:2] + bytes([9]) + good[3:],
        'event byte >= 216': pdu(events_byte=216),
        'count exceeds packed bytes': pdu(count=5),
        'missing PDU end mark': good[:-2],
        'attribute length overruns PDU': good[:3] + (200).to_bytes(2, 'big') + good[5:],
    }
    for label, payload in bad.items():
        try:
            d.decode_msrp(payload, 1, 'x')
            check(False, f'malformed input refused: {label}')
        except ValueError:
            check(True, f'malformed input refused: {label}')
        except Exception as error:
            check(False, f'malformed input refused: {label} (crashed with {type(error).__name__})')
    near = []
    dirs = [ev / 'author' / f'talker-{c:03d}' for c in range(1, 6)] + [a3 / f'talker-{c:03d}' for c in (13, 24, 75)]
    for folder in dirs:
        r = json.loads((folder / 'result.json').read_text())
        with (folder / 'msrp.tsv').open() as f:
            ta = [int(e['tap_ns']) for e in csv.DictReader(f, delimiter='\t')
                  if e['sender'] == 'DUT' and e['type'] == 'TalkerAdvertise' and e['stream_id'] == r['stream_id']]
        for edge in ('disconnect_response_ns', 'connect_command_ns'):
            near.append(min(abs(t - r[edge]) for t in ta))
    check(min(near) > 1_000_000, f'no published DUT Talker Advertise event within 1 ms of a hold boundary (closest {min(near) / 1e9:.6f} s)')
    print('RESULT ' + ('PASS' if not fails else f'FAIL ({len(fails)})'))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
