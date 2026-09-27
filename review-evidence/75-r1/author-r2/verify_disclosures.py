"""Verify the recorded initial-bind, declaration-state and restore disclosures.

Usage: python3 verify_disclosures.py OPERATOR_PACKET OUTPUT_DIRECTORY
"""
import csv
import hashlib
import json
from pathlib import Path
import sys


def main():
    packet, output = map(Path, sys.argv[1:])
    a = json.loads((packet/'talker-setup/analysis.json').read_text())
    events = list(csv.DictReader((packet/'talker-setup/msrp.tsv').open(), delimiter='\t'))
    for row in events:
        row['tap_ns'] = int(row['tap_ns'])
    declarations = [r for r in events if r['sender'] == 'DUT' and r['type'] == 'TalkerAdvertise'
                    and r['stream_id'] == a['stream_id'] and r['event'] in ('New', 'JoinIn', 'JoinMt', 'In', 'Mt', 'Lv')]
    first_advert = min(r['tap_ns'] for r in declarations)
    assert first_advert > a['response_ns']
    bridge = [r for r in events if r['sender'] == 'bridge']
    first_bridge = min(r['tap_ns'] for r in bridge)
    assert any(r['tap_ns'] == first_bridge and r['event'] == 'LeaveAll' for r in bridge)
    for cycle in range(1,101):
        folder = packet/f'talker-{cycle:03d}'
        r = json.loads((folder/'result.json').read_text())
        es = list(csv.DictReader((folder/'msrp.tsv').open(), delimiter='\t'))
        assert any(e['sender'] == 'DUT' and e['type'] == 'TalkerAdvertise'
                   and e['stream_id'] == r['stream_id'] and e['event'] in ('New','JoinIn','In','JoinMt','Mt')
                   and r['disconnect_response_ns'] < int(e['tap_ns']) < r['connect_command_ns'] for e in es)
    censuses = []
    for name in ('census-start.jsonl','census-end.jsonl'):
        rows = [json.loads(line) for line in (packet/name).read_text().splitlines()]
        states = {(r['role'],r['what']):r['response'] for r in rows if r.get('what','').startswith('state-')}
        assert len(states) == 18 and all(r['conn_count'] == 0 for r in states.values())
        censuses.append(states)
    assert censuses[0].keys() == censuses[1].keys()
    assert censuses[0][('dut','state-6-1')]['dmac'] == '000000000000'
    assert censuses[1][('dut','state-6-1')]['dmac'].startswith('91e0f0')
    report = dict(initial_bind_capture='talker-setup/tap.pcap',
                  initial_bind_latency_s=a['latency_s'],
                  first_dut_advertise_after_response_s=(first_advert-a['response_ns'])/1e9,
                  first_bridge_msrp_is_leaveall=True,
                  first_bridge_msrp_after_response_s=(first_bridge-a['response_ns'])/1e9,
                  ready_after_response_s=a['response_to_ready_s'],
                  ready_to_crf_s=a['ready_to_first_avtp_s'],
                  numbered_talker_holds_with_dut_advertise=100,
                  unbound_states_before=18, unbound_states_after=18,
                  dut_output_one_destination_before='all-zero',
                  dut_output_one_destination_after='MAAP-range',
                  source_hashes={name:hashlib.sha256((packet/name).read_bytes()).hexdigest()
                                 for name in ('talker-setup/analysis.json','talker-setup/msrp.tsv','census-start.jsonl','census-end.jsonl')})
    (output/'disclosures.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    main()
