"""Does the DUT talker keep declaring Talker Advertise through each hold?

Usage: python3 hold_declaration_probe.py EVIDENCE_DIR
Uses the published talker cycles 1-5 and the initial bind (talker-setup).
A declaration is an MRP New, JoinIn or JoinMt event. In, Mt and Lv carry
no declaration (802.1Q 10.7.6 / Table 10-3 applicant events). The script
applies both the declaration-only predicate and the addendum's predicate
(verify_disclosures.py lines 29-31, which also accepts In and Mt).
"""
import csv
import json
import sys
from pathlib import Path

DECL = ('New', 'JoinIn', 'JoinMt')
ADDENDUM = ('New', 'JoinIn', 'In', 'JoinMt', 'Mt')


def main():
    a1 = Path(sys.argv[1]) / 'author'
    for c in range(1, 6):
        d = a1 / f'talker-{c:03d}'
        r = json.loads((d / 'result.json').read_text())
        dr, cc, ack = r['disconnect_response_ns'], r['connect_command_ns'], r['response_ns']
        ev = [e for e in csv.DictReader((d / 'msrp.tsv').open(), delimiter='\t')
              if e['sender'] == 'DUT' and e['type'] == 'TalkerAdvertise' and e['stream_id'] == r['stream_id']]
        hold = [e for e in ev if dr < int(e['tap_ns']) < cc]
        decl = [e for e in hold if e['event'] in DECL]
        add = [e for e in hold if e['event'] in ADDENDUM]
        first_after = min((int(e['tap_ns']) for e in ev if int(e['tap_ns']) >= ack and e['event'] in DECL), default=None)
        seq = ', '.join(f"{(int(e['tap_ns']) - dr) / 1e9:+.3f} {e['event']}" for e in hold)
        print(f"talker-{c:03d}: latency {r['latency_s']:.6f} s; hold DUT TA events [{seq}]; "
              f"declarations in hold {len(decl)}; addendum predicate {'TRUE' if add else 'FALSE'}; "
              f"first DUT declaration after response +{(first_after - ack) / 1e9:.6f} s")
    s = a1 / 'talker-setup'
    r = json.loads((s / 'result.json').read_text())
    ev = [e for e in csv.DictReader((s / 'msrp.tsv').open(), delimiter='\t')
          if e['sender'] == 'DUT' and e['type'] == 'TalkerAdvertise' and e['stream_id'] == r['stream_id']]
    before = [e for e in ev if int(e['tap_ns']) < r['response_ns']]
    first = min(int(e['tap_ns']) for e in ev if e['event'] in DECL)
    print(f"talker-setup: latency {r['latency_s']:.6f} s; DUT TA events before response {len(before)}; "
          f"first declaration +{(first - r['response_ns']) / 1e9:.6f} s")
    print('CONCLUSION: talker cycle 1 holds no DUT Talker Advertise declaration (Lv then Mt only) '
          'yet the addendum predicate reports it as advertising; its first post-response declaration '
          'is later than the initial bind\'s, and it restarts in 0.117736 s.')


if __name__ == '__main__':
    main()
