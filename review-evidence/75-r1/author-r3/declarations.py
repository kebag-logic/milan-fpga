"""Round-3 declaration census and non-stop chronology, from recorded data.

Usage: python3 declarations.py OPERATOR_PACKET RAW_CAPTURE_ROOT OUTPUT_DIRECTORY
Run recompute.py first. All source files are opened read-only.
"""
import csv
import hashlib
import json
from pathlib import Path
import sys

from recompute import packets, read_json, require

DECLARATIONS = {'New', 'JoinIn', 'JoinMt'}
EVENTS = ('New', 'JoinIn', 'In', 'JoinMt', 'Mt', 'Lv')
TYPES = {1: 'TalkerAdvertise', 2: 'TalkerFailed', 3: 'Listener', 4: 'Domain'}


def declaration_events(events):
    return [e for e in events if e['event'] in DECLARATIONS]


def require_all_holds_declared(rows):
    missing = [r['cycle'] for r in rows if r['declaration_count'] == 0]
    require(not missing, f'holds without DUT declaration: {missing}')


def ethernet(frame):
    et = int.from_bytes(frame[12:14], 'big')
    if et == 0x8100:
        return int.from_bytes(frame[16:18], 'big'), frame[18:]
    return et, frame[14:]


def decode_msrp(payload, ns, sender):
    require(payload and payload[0] == 0, 'MSRP version')
    offset = 1
    decoded = []
    while offset + 2 <= len(payload) and payload[offset:offset + 2] != bytes(2):
        require(offset + 4 <= len(payload), 'MSRP message header')
        kind, width = payload[offset:offset + 2]
        length = int.from_bytes(payload[offset + 2:offset + 4], 'big')
        offset += 4
        end = offset + length
        require(kind in TYPES and width == {1: 25, 2: 34, 3: 8, 4: 4}[kind]
                and end <= len(payload), 'MSRP message shape')
        while offset + 2 <= end and payload[offset:offset + 2] != bytes(2):
            header = int.from_bytes(payload[offset:offset + 2], 'big')
            offset += 2
            count, leave_all = header & 8191, header >> 13
            require(leave_all in (0, 1) and offset + width <= end, 'MSRP vector')
            first = payload[offset:offset + width]
            offset += width
            event_size = (count + 2) // 3
            listener_size = (count + 3) // 4 if kind == 3 else 0
            require(offset + event_size + listener_size <= end, 'MSRP packed events')
            events = payload[offset:offset + event_size]
            listeners = payload[offset + event_size:offset + event_size + listener_size]
            offset += event_size + listener_size
            base = dict(tap_ns=str(ns), sender=sender, type=TYPES[kind], first_value=first.hex())
            if leave_all:
                decoded.append(dict(base, event='LeaveAll', stream_id='None', listener='None'))
            for index in range(count):
                packed = events[index // 3]
                require(packed < 216, 'invalid three-packed event')
                event = EVENTS[(packed // (36, 6, 1)[index % 3]) % 6]
                stream = 'None'
                if kind in (1, 2, 3):
                    stream = (first[:6] + ((int.from_bytes(first[6:8], 'big') + index)
                                          % 65536).to_bytes(2, 'big')).hex()
                listener = str((listeners[index // 4] // (64, 16, 4, 1)[index % 4]) % 4) if kind == 3 else 'None'
                decoded.append(dict(base, event=event, stream_id=stream, listener=listener))
        require(offset + 2 == end and payload[offset:end] == bytes(2), 'MSRP attribute end')
        offset = end
    require(payload[offset:offset + 2] == bytes(2), 'MSRP PDU end')
    return decoded


def recorded_events(packet, raw_root, name, manifest):
    raw = (raw_root / name / 'tap.pcap').read_bytes()
    entry = manifest[f'{name}/tap.pcap']
    require(len(raw) == entry['size'] and hashlib.sha256(raw).hexdigest() == entry['sha256'], 'raw identity')
    recs = list(packets(raw))
    decoded, crf, disconnect_tx = [], [], []
    result = read_json(packet / name / 'result.json')
    for ns, port, frame, _, _ in recs:
        et, payload = ethernet(frame)
        if et == 0x22ea:
            decoded.extend(decode_msrp(payload, ns, 'DUT' if port == 3 else 'bridge'))
        if et == 0x22f0 and len(payload) >= 28 and payload[0] == 4:
            if port == 3 and payload[4:12].hex() == result['stream_id']:
                # Full CRF validity and progression are checked by recompute.py.
                crf.append(ns)
        if et == 0x22f0 and len(payload) >= 56 and payload[0] == 0xfc and payload[1] & 15 == 2:
            disconnect_tx.append(ns)
    with (packet / name / 'msrp.tsv').open() as source:
        retained = list(csv.DictReader(source, delimiter='\t'))
    require(decoded == retained, f'{name}: decoded MSRP differs from retained TSV')
    return result, retained, crf, disconnect_tx


def write_csv(path, rows):
    require(bool(rows), 'empty evidence table')
    with path.open('w') as destination:
        writer = csv.DictWriter(destination, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    packet, raw_root, output = map(Path, sys.argv[1:])
    require(output.resolve() not in (packet.resolve(), raw_root.resolve()), 'output aliases input')
    manifest = {r['identifier']: r for r in read_json(packet / 'RAW-ARTIFACTS.json')}
    with (output / 'stop-checks.csv').open() as source:
        stops = {int(r['cycle']): r for r in csv.DictReader(source) if r['direction'] == 'talker'}
    holds, hold_events, listener_events, nonstops, provenance = [], [], [], [], []
    for cycle in range(1, 101):
        name = f'talker-{cycle:03d}'
        result, events, crf, disconnect_tx = recorded_events(packet, raw_root, name, manifest)
        dr, command, response = (result[k] for k in ('disconnect_response_ns', 'connect_command_ns', 'response_ns'))
        target = [e for e in events if e['stream_id'] == result['stream_id']]
        adverts = [e for e in target if e['sender'] == 'DUT' and e['type'] == 'TalkerAdvertise']
        during = [e for e in adverts if dr <= int(e['tap_ns']) < command]
        declared = declaration_events(during)
        holds.append(dict(cycle=cycle, disconnect_response_ns=dr, connect_command_ns=command,
                          response_ns=response, declaration_count=len(declared),
                          withdrawal_count=sum(e['event'] == 'Lv' for e in during),
                          empty_count=sum(e['event'] == 'Mt' for e in during)))
        hold_events.extend(dict(cycle=cycle, tap_ns=int(e['tap_ns']),
                                after_disconnect_s=(int(e['tap_ns'])-dr)/1e9,
                                event=e['event'], is_declaration=e['event'] in DECLARATIONS) for e in during)
        for source in ('result.json', 'msrp.tsv'):
            provenance.append(dict(identifier=f'{name}/{source}', sha256=hashlib.sha256((packet/name/source).read_bytes()).hexdigest()))
        if cycle == 1:
            first_advert = min(int(e['tap_ns']) for e in declaration_events(adverts) if int(e['tap_ns']) >= response)
            ready = min(int(e['tap_ns']) for e in declaration_events(target)
                        if e['sender'] == 'bridge' and e['type'] == 'Listener' and e['listener'] == '2'
                        and int(e['tap_ns']) >= response)
            cycle_one = dict(**holds[-1], latency_s=result['latency_s'],
                             declarations_disconnect_to_response=sum(dr <= int(e['tap_ns']) < response
                                                                     for e in declaration_events(adverts)),
                             first_advert_after_response_s=(first_advert-response)/1e9,
                             ready_after_response_s=(ready-response)/1e9,
                             advert_to_ready_s=(ready-first_advert)/1e9,
                             ready_to_crf_s=(result['first_avtp_ns']-ready)/1e9)
        if stops[cycle]['classification'] != 'NOT_RESTART':
            continue
        bridge = [e for e in target if e['sender'] == 'bridge' and e['type'] == 'Listener'
                  and int(e['tap_ns']) >= dr]
        leaves = [e for e in bridge if e['event'] == 'Lv']
        redeclarations = declaration_events(bridge)
        require(len(leaves) == 1 and redeclarations, 'non-stop Listener chronology needs separate analysis')
        leave = int(leaves[0]['tap_ns'])
        first_decl = min(int(e['tap_ns']) for e in redeclarations)
        around_absence = [max(t for t in crf if t < leave)]
        around_absence += [t for t in crf if leave <= t < first_decl]
        around_absence += [min(t for t in crf if t >= first_decl)]
        absence_gap = max(b-a for a, b in zip(around_absence, around_absence[1:]))
        for e in bridge:
            ns = int(e['tap_ns'])
            before, after = max(t for t in crf if t < ns), min(t for t in crf if t >= ns)
            listener_events.append(dict(cycle=cycle, tap_ns=ns, event=e['event'], listener=int(e['listener']),
                                        after_disconnect_s=(ns-dr)/1e9, after_reconnect_response_s=(ns-response)/1e9,
                                        previous_crf_ns=before, next_crf_ns=after,
                                        bracketing_crf_gap_s=(after-before)/1e9))
        nonstops.append(dict(cycle=cycle, disconnect_response_ns=dr, connect_command_ns=command,
                             response_ns=response, listener_lv_ns=leave,
                             lv_after_disconnect_s=(leave-dr)/1e9,
                             first_listener_declaration_ns=first_decl,
                             first_declaration_after_disconnect_s=(first_decl-dr)/1e9,
                             first_declaration_after_response_s=(first_decl-response)/1e9,
                             declarations_between_lv_and_response=sum(leave < int(e['tap_ns']) < response for e in redeclarations),
                             pdus_lv_to_response=sum(leave <= t < response for t in crf),
                             pdus_lv_to_redeclaration=sum(leave <= t < first_decl for t in crf),
                             maximum_lv_to_redeclaration_gap_s=absence_gap/1e9,
                             maximum_hold_gap_s=float(stops[cycle]['maximum_hold_gap_s']),
                             dut_start_delta=int(stops[cycle]['dut_start_delta']),
                             dut_stop_delta=int(stops[cycle]['dut_stop_delta']),
                             disconnect_tx_count=len(disconnect_tx)))
    setup, events, _, _ = recorded_events(packet, raw_root, 'talker-setup', manifest)
    adverts = declaration_events([e for e in events if e['sender'] == 'DUT' and e['type'] == 'TalkerAdvertise'
                                  and e['stream_id'] == setup['stream_id']])
    setup_summary = dict(latency_s=setup['latency_s'],
                         declarations_before_response=sum(int(e['tap_ns']) < setup['response_ns'] for e in adverts),
                         first_advert_after_response_s=(min(int(e['tap_ns']) for e in adverts)-setup['response_ns'])/1e9)
    for source in ('result.json', 'msrp.tsv'):
        provenance.append(dict(identifier=f'talker-setup/{source}', sha256=hashlib.sha256((packet/'talker-setup'/source).read_bytes()).hexdigest()))
    summary = dict(hold_window='[disconnect response, connect command)',
                   declaration_events=sorted(DECLARATIONS), inspected_holds=len(holds),
                   holds_with_dut_declaration=sum(r['declaration_count'] > 0 for r in holds),
                   holds_without_dut_declaration=[r['cycle'] for r in holds if not r['declaration_count']],
                   raw_msrp_tsv_matches=len(holds)+1, cycle_one=cycle_one, initial_bind=setup_summary,
                   nonstops=nonstops)
    for name, rows in [('hold-declarations.csv', holds), ('hold-events.csv', hold_events),
                       ('listener-events.csv', listener_events), ('declaration-input-hashes.csv', provenance)]:
        write_csv(output/name, rows)
    (output/'declarations-summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
