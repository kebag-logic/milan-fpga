"""Offline round-3 stop checks; inputs are opened read-only.

Usage: python3 recompute.py OPERATOR_PACKET RAW_CAPTURE_ROOT OUTPUT_DIRECTORY
The output contains neutral roles and relative artifact identifiers only.
"""
import csv
import hashlib
import json
import math
from pathlib import Path
import statistics as st
import struct
import sys

if sys.flags.optimize:
    raise SystemExit("REFUSED: optimized execution disables evidence checks")

PERIOD_NS = 2_000_000
SETTLE_NS = 500_000_000


def read_json(path):
    return json.loads(path.read_text())


def json_rows(path):
    return [json.loads(line) for line in path.read_text().splitlines()]


def packets(raw):
    magic, major, minor, zone, accuracy, snap, network = struct.unpack('<IHHIIII', raw[:24])
    require((magic in (0xA1B2C3D4, 0xA1B23C4D) and network == 1), 'record consistency check failed')
    nano = magic == 0xA1B23C4D
    off, first, previous = 24, None, None
    while off < len(raw):
        require((off + 16 <= len(raw)), 'truncated record header')
        sec, frac, size, original = struct.unpack('<IIII', raw[off:off + 16])
        off += 16
        require((size == original and off + size <= len(raw)), 'truncated packet')
        pkt = raw[off:off + size]
        off += size
        require((len(pkt) >= 42), 'record consistency check failed')
        tag, envelope, port = struct.unpack('<III', pkt[:12])
        if tag != 6 or port not in (2, 3):
            continue
        host = sec * 10**9 + frac * (1 if nano else 1000)
        low = struct.unpack('<I', pkt[16:20])[0]
        if first is None:
            first = host, low
        ns = low - first[1] + round(((host - first[0]) - (low - first[1])) / 2**32) * 2**32
        require((previous is None or ns >= previous), 'timestamp reversal')
        previous = ns
        yield ns, port, pkt[28:], size + 16, host - first[0] - ns


def counter(path, role, what):
    r = next(r['response'] for r in json_rows(path)
             if r.get('role') == role and r.get('what') == what)
    require((r['status'] == 'SUCCESS' and int(r['valid'], 16) & 3 == 3), 'record consistency check failed')
    return [r['counters'][str(i)] for i in (0, 1)]


def delta(before, after):
    return [(a - b) % 2**32 for b, a in zip(before, after)]


def require(condition, message="record consistency check failed"):
    if not condition:
        raise ValueError(message)


def classify_stop(count, first_post_ns, response_ns):
    if count != 0:
        return 'NOT_RESTART'
    if first_post_ns < response_ns:
        return 'NOT_RESTART'
    return 'RESTART'


def outcome_lines(rows):
    passed = sum(r['stop_check'] == 'PASS' for r in rows)
    rejected = [f"{r['direction']}-{r['cycle']:03d}" for r in rows
                if r['classification'] != 'RESTART']
    return [
        f"PASS: {len(rows)} raw hashes, ACMP anchors, CRF validity, original timings and counter continuity checked.",
        f"Stop checks: {passed} PASS; {len(rejected)} FAIL, excluded as NOT_RESTART: "
        + (', '.join(rejected) if rejected else 'none') + '.',
    ]


def fit(rows):
    x = [r['cycle'] for r in rows]
    y = [r['latency_s'] for r in rows]
    n = len(x)
    mx, my = st.mean(x), st.mean(y)
    sxx = sum((a - mx)**2 for a in x)
    slope = sum((a - mx) * (b - my) for a, b in zip(x, y)) / sxx
    se = math.sqrt(sum((b - my - slope * (a - mx))**2 for a, b in zip(x, y)) / (n - 2) / sxx)
    # Student-t 0.975, expanded from the normal quantile through df^-3.
    # At df=95/98 this agrees with tabulated t to six decimal places.
    z, df = 1.959963984540054, n - 2
    t = z + (z**3 + z)/(4*df) + (5*z**5 + 16*z**3 + 3*z)/(96*df**2) + (3*z**7 + 19*z**5 + 17*z**3 - 15*z)/(384*df**3)
    return dict(n=n, slope_s_per_cycle=slope, standard_error=se,
                degrees_of_freedom=df, t_975=t,
                ci95_low=slope-t*se, ci95_high=slope+t*se,
                upper_ms_per_100_cycles=(slope+t*se)*100_000)


def distribution(rows):
    y = sorted(r['latency_s'] for r in rows)
    return dict(n=len(y), below_one_second=sum(v < 1 for v in y),
                minimum=min(y), median=st.median(y), p95=y[math.ceil(.95*len(y))-1], maximum=max(y))


def main():
    packet, raw_root, output = map(Path, sys.argv[1:])
    require((output.resolve() not in (packet.resolve(), raw_root.resolve())), 'record consistency check failed')
    manifest = {r['identifier']: r for r in read_json(packet/'RAW-ARTIFACTS.json')}
    rows, provenance, summaries = [], [], {}
    for direction in ('listener', 'talker'):
        active_role, active_what = ('peer', 'counter-6-2') if direction == 'listener' else ('dut', 'counter-6-1')
        last_active = counter(packet/f'{direction}-setup/snapshot-after.jsonl', active_role, active_what)
        initial_active = last_active
        for cycle in range(1, 101):
            name = f'{direction}-{cycle:03d}'
            folder = packet/name
            result, analysis = read_json(folder/'result.json'), read_json(folder/'analysis.json')
            for source in ('result.json', 'analysis.json', 'snapshot-before.jsonl', 'snapshot-after.jsonl', 'cycle.jsonl'):
                provenance.append(dict(identifier=f'{name}/{source}', sha256=hashlib.sha256((folder/source).read_bytes()).hexdigest()))
            require((result['capture_rc'] == 0 and not result['errors'] and not analysis['msrp_parse_errors']), 'record consistency check failed')
            require(('0 packets dropped by kernel' in (folder/'capture.txt').read_text()), 'record consistency check failed')
            identifier = f'{name}/tap.pcap'
            raw = (raw_root/identifier).read_bytes()
            digest = hashlib.sha256(raw).hexdigest()
            require((len(raw) == manifest[identifier]['size'] and digest == manifest[identifier]['sha256']), name)
            recs = list(packets(raw))
            require((max(r[4] for r in recs)-min(r[4] for r in recs) < 2**31), 'ambiguous unwrap')
            transactions = [r for r in json_rows(folder/'cycle.jsonl') if r.get('kind') == 'transaction']
            tx = next(r for r in transactions if r['mt'] == 6)
            dis = next(r for r in transactions if r['mt'] == 8)
            listener_role, state_id = ('dut', 'state-5-1') if direction == 'listener' else ('peer', 'state-5-8')
            state = next(r['response'] for r in json_rows(folder/'snapshot-after.jsonl')
                         if r.get('role') == listener_role and r.get('what') == state_id)
            require((state['status'] == 0 and state['conn_count'] == 1 and state['stream_id'] == result['stream_id']), 'record consistency check failed')
            acmp, target = [], []
            for ns, port, frame, stored_bytes, offset in recs:
                et, payload, vlan = int.from_bytes(frame[12:14], 'big'), frame[14:], None
                if et == 0x8100:
                    tci = int.from_bytes(frame[14:16], 'big')
                    vlan = tci >> 13, tci & 4095
                    et, payload = int.from_bytes(frame[16:18], 'big'), frame[18:]
                if et != 0x22f0 or len(payload) < 12:
                    continue
                if payload[0] == 0xfc and len(payload) >= 56:
                    acmp.append(dict(ns=ns, mt=payload[1]&15, status=payload[2]>>3,
                                     seq=int.from_bytes(payload[48:50], 'big'), controller=payload[12:20].hex()))
                if payload[0] != 4 or payload[4:12].hex() != result['stream_id']:
                    continue
                valid = (len(payload) >= 28 and payload[1]&0xf0 == 0x80 and payload[3] == 1
                         and int.from_bytes(payload[12:16], 'big') == 48000
                         and payload[16:20] == bytes.fromhex('00080060') and vlan == (3, 2)
                         and port == (2 if direction == 'listener' else 3)
                         and frame[6:12].hex() == result['stream_id'][:12]
                         and frame[:6].hex() == state['dmac'])
                require((valid), f'{name}: invalid target CRF requires separate analysis')
                target.append(dict(ns=ns, seq=payload[2], timestamp=int.from_bytes(payload[20:28], 'big'), stored_bytes=stored_bytes,
                                   mr=(payload[1]>>3)&1, fs=(payload[1]>>1)&1, tu=payload[1]&1))
            def anchor(mt, transaction):
                matching = [r for r in acmp if r['mt'] == mt and r['seq'] == transaction['seq']
                            and r['controller'] == transaction['response']['controller']]
                require((len(matching) == 1 and matching[0]['status'] == 0), 'record consistency check failed')
                return matching[0]['ns']
            dr, cc, ack = anchor(9, dis), anchor(6, tx), anchor(7, tx)
            require(((dr, cc, ack) == (result['disconnect_response_ns'], result['connect_command_ns'], result['response_ns'])), 'record consistency check failed')
            require((cc - dr >= 2_000_000_000), 'record consistency check failed')
            after = [r for r in target if r['ns'] >= ack]
            require((len(after) >= 2), 'record consistency check failed')
            first, second = after[:2]
            require((second['seq'] == (first['seq']+1)%256 and second['timestamp'] > first['timestamp']), 'record consistency check failed')
            latency = (first['ns'] - ack)/1e9
            require((first['ns'] == result['first_avtp_ns'] and latency == result['latency_s'] == analysis['latency_s']), 'record consistency check failed')
            require((len(target) == analysis['valid_avtp']), 'record consistency check failed')
            require((not any(r['mr'] or r['fs'] or r['tu'] for r in target)), 'recorded flags changed')
            last_half = sum(cc-SETTLE_NS < r['ns'] < cc for r in target)
            require((last_half == result['frames_last_half_second_disconnected']), 'record consistency check failed')
            stop_begin = dr + SETTLE_NS
            settled_count = sum(stop_begin <= r['ns'] < ack for r in target)
            pre_command = sum(stop_begin <= r['ns'] < cc for r in target)
            command_response = sum(cc <= r['ns'] < ack for r in target)
            full_hold = sum(dr <= r['ns'] < cc for r in target)
            post_settle = next(r for r in target if r['ns'] >= stop_begin)
            verdict = classify_stop(settled_count, post_settle['ns'], ack)
            # Wire classification is independent of the counters.
            before = counter(folder/'snapshot-before.jsonl', active_role, active_what)
            end = counter(folder/'snapshot-after.jsonl', active_role, active_what)
            require((before == last_active), 'counter discontinuity between cycles')
            active_delta = delta(before, end)
            last_active = end
            dut_before = counter(folder/'snapshot-before.jsonl', 'dut', 'counter-6-1')
            dut_after = counter(folder/'snapshot-after.jsonl', 'dut', 'counter-6-1')
            dut_delta = delta(dut_before, dut_after)
            require((active_delta == ([1, 1] if verdict == 'RESTART' else [0, 0])), 'wire/counter disagreement')
            near_hold = [max((r for r in target if r['ns'] < dr), key=lambda r:r['ns'])]
            near_hold += [r for r in target if dr <= r['ns'] < ack] + [first]
            max_gap = max(b['ns']-a['ns'] for a, b in zip(near_hold, near_hold[1:]))
            if verdict == 'NOT_RESTART':
                require((max_gap < PERIOD_NS*2), 'early resumption or gap requires separate censoring analysis')
                require((all(b['seq'] == (a['seq']+1)%256 and b['timestamp'] > a['timestamp'] for a,b in zip(near_hold, near_hold[1:]))), 'nonrestart progression')
            prior = max(r['ns'] for r in target if r['ns'] < stop_begin)
            row = dict(direction=direction, cycle=cycle, capture=identifier, sha256=digest,
                       disconnect_response_ns=dr, settle_begin_ns=stop_begin, connect_command_ns=cc, response_ns=ack,
                       last_half_second_pdus=last_half, settled_to_command_pdus=pre_command,
                       command_to_response_pdus=command_response, settled_to_response_pdus=settled_count,
                       disconnect_to_command_pdus=full_hold, last_before_settle_ns=prior,
                       first_after_settle_ns=post_settle['ns'], silence_gap_s=(post_settle['ns']-prior)/1e9,
                       maximum_hold_gap_s=max_gap/1e9, dut_start_delta=dut_delta[0], dut_stop_delta=dut_delta[1],
                       active_start_delta=active_delta[0], active_stop_delta=active_delta[1],
                       first_post_response_ns=first['ns'], latency_s=latency, stop_check='PASS' if verdict == 'RESTART' else 'FAIL', classification=verdict,
                       capture_bytes=len(raw), capture_span_s=(recs[-1][0]-recs[0][0])/1e9,
                       capture_tail_s=(recs[-1][0]-first['ns'])/1e9, target_pdus=len(target),
                       mr_one_pdus=sum(r['mr'] for r in target), fs_one_pdus=sum(r['fs'] for r in target),
                       tu_one_pdus=sum(r['tu'] for r in target),
                       target_stored_bytes=sum(r['stored_bytes'] for r in target),
                       other_stored_bytes=len(raw)-24-sum(r['stored_bytes'] for r in target),
                       unwrap_spread_s=(max(r[4] for r in recs)-min(r[4] for r in recs))/1e9)
            rows.append(row)
        restored = counter(packet/f'{direction}-restore/snapshot-before.jsonl', active_role, active_what)
        require((restored == last_active), 'record consistency check failed')
        series = [r for r in rows if r['direction'] == direction]
        accepted = [r for r in series if r['classification'] == 'RESTART']
        rejected = [r['cycle'] for r in series if r['classification'] != 'RESTART']
        summaries[direction] = dict(attempts=len(series), demonstrated=distribution(accepted),
                                   original=distribution(series), excluded_cycles=rejected,
                                   active_counter_before=initial_active, active_counter_after=last_active,
                                   active_counter_delta=delta(initial_active, last_active),
                                   fit=fit(accepted), fit_without_cycle_one=fit([r for r in accepted if r['cycle'] != 1]),
                                   first_ten_median=st.median(r['latency_s'] for r in accepted if r['cycle'] <= 10),
                                   last_ten_median=st.median(r['latency_s'] for r in accepted if r['cycle'] > 90),
                                   blocks=[dict(first=n, last=n+9, **distribution([r for r in accepted if n <= r['cycle'] <= n+9])) for n in range(1,101,10)],
                                   largest_six_captures=sorted(series, key=lambda r:r['capture_bytes'], reverse=True)[:6],
                                   median_capture_bytes=st.median(r['capture_bytes'] for r in series),
                                   median_capture_span_s=st.median(r['capture_span_s'] for r in series),
                                   median_capture_tail_s=st.median(r['capture_tail_s'] for r in series))
    output.mkdir(exist_ok=True)
    for name, data in [('stop-checks.csv', rows), ('input-hashes.csv', provenance)]:
        with (output/name).open('w') as f:
            writer = csv.DictWriter(f, fieldnames=list(data[0]))
            writer.writeheader()
            writer.writerows(data)
    (output/'recomputed-summary.json').write_text(json.dumps(summaries, indent=2)+'\n')
    stop_lines = ['| Direction | Cycle | Settled PDUs | Command-response PDUs | DUT start/stop | Active talker start/stop | Stop check |',
                  '|---|---|---|---|---|---|---|']
    for r in rows:
        stop_lines.append(f"| DUT {r['direction']} | {r['cycle']} | {r['settled_to_response_pdus']} | {r['command_to_response_pdus']} | {r['dut_start_delta']} / {r['dut_stop_delta']} | {r['active_start_delta']} / {r['active_stop_delta']} | {r['stop_check']} |")
    (output/'stop-table.md').write_text('\n'.join(stop_lines)+'\n')
    size_lines = ['| Talker cycle | Bytes | Span, seconds | Tail, seconds | CRF PDUs | CRF bytes | Other bytes | Explanation |',
                  '|---|---|---|---|---|---|---|---|']
    for r in summaries['talker']['largest_six_captures']:
        why = 'Continuous hold; shorter tail' if r['cycle'] == 13 else ('Continuous hold' if r['classification'] == 'NOT_RESTART' else 'Longer capture tail')
        size_lines.append(f"| {r['cycle']} | {r['capture_bytes']} | {r['capture_span_s']:.6f} | {r['capture_tail_s']:.6f} | {r['target_pdus']} | {r['target_stored_bytes']} | {r['other_stored_bytes']} | {why} |")
    (output/'capture-size-table.md').write_text('\n'.join(size_lines)+'\n')
    for line in outcome_lines(rows):
        print(line)
    for direction, summary in summaries.items():
        print(direction, json.dumps(summary['demonstrated']), json.dumps(summary['fit']))


if __name__ == '__main__':
    main()
