"""Independent integer and raw-byte audit of the public B12 evidence.

Usage: python3 -B audit_evidence.py ROUND2 ROUND1 CHECKOUT
No device access; no source imports from the packet.
"""
import csv
import hashlib
import json
from pathlib import Path
import re
import struct
import sys

packet, previous, repo = map(Path, sys.argv[1:])
def read(name):
    return json.loads((packet / name).read_text())
def series(root, glob):
    return {row['cycle']: row for f in sorted(root.glob(glob)) for row in json.loads(f.read_text())}

cycles = series(packet, 'cycles-*.json')
wire = series(packet, 'wire-receipts-*.json')
oldwire = series(previous, 'wire-receipts-*.json')
assert len(cycles) == len(wire) == 182
assert set(cycles) == set(wire)
page = (repo / 'docs/findings/653_DISCONNECT_ORDER_BENCH.md').read_text().split('## #653 bench: disconnect order with')[1]
tables = {}
for line in page.splitlines():
    if line.startswith('| '):
        values = [x.strip() for x in line.split('|')[1:-1]]
        if values[0] in cycles:
            tables.setdefault(values[0], []).append(values)
assert set(cycles) <= set(tables)
counts = {}
wire_count = 0
original_peer = set()
intervals = []
for name, c in cycles.items():
    assert c['result'] == 'OK' and c['status'] == 0
    assert c['library_state'] == 'NotConnected'
    assert c['sequence_max'] == c['interruption_max'] == c['stream_gaps'] == 0
    assert c['post_counters']['ML'] == c['post_counters']['MU']
    w = wire[name]
    decoded = {k: bytes.fromhex(w[k]['raw']) for k in ('command', 'response', 'unlock')}
    cmd, rsp, unlock = [decoded[k] for k in ('command', 'response', 'unlock')]
    assert cmd[0:2] == b'\xfc\x08' and rsp[0:2] == b'\xfc\x09'
    # Correlate controller, listener, input and transaction. The peer may
    # clear the talker fields in the successful disconnect response.
    assert cmd[12:20] == rsp[12:20] and cmd[28:36] == rsp[28:36]
    assert cmd[38:40] == rsp[38:40] and cmd[48:50] == rsp[48:50]
    assert rsp[2] >> 3 == 0
    assert unlock[0:2] == b'\xfb\x01' and unlock[2] >> 3 == 0
    assert unlock[22:24] == b'\x80\x29' and unlock[24:26] == b'\x00\x05'
    assert unlock[4:12] == rsp[28:36] and unlock[12:20] == rsp[12:20]
    assert unlock[26:28] == rsp[38:40]
    assert int.from_bytes(unlock[28:32], 'big') & 3 == 3
    locked, unlocked, interrupted, seq = struct.unpack('>4I', unlock[32:48])
    assert locked == unlocked and interrupted == seq == 0
    assert w['command']['i'] < w['response']['i'] < w['unlock']['i']
    delta = w['unlock']['tns'] - w['response']['tns']
    assert delta > 0 and abs(delta / 1000 - c['response_unlock_us']) < 1e-7
    assert c['selected_capture'] == w['capture']
    assert w['capture'].endswith('observer.pcap') == (c['direction'] == 'B')
    display = f"R / {delta / 1000:.3f}"
    assert any(display in row for row in tables[name]), name
    assert any(f"{c['actual_hold_ms']:.3f}" in ' | '.join(row) for row in tables[name]), name
    intervals.append(dict(cycle=name, interval_ns=delta, clock='controller capture' if c['direction']=='B' else 'tap'))
    key = (c['direction'], c['kind'], c['phase'])
    counts[str(key)] = counts.get(str(key), 0) + 1
    for kind in ('command', 'response', 'unlock'):
        new = decoded[kind]
        old = bytes.fromhex(oldwire[name][kind]['raw'].replace('<controller-host-id>', '000000000000'))
        if kind == 'command':
            original_peer.add(old[20:28] if c['direction'] == 'A' else old[28:36])
        excluded = set(range(4, 36)) | set(range(40, 46)) if old[0] == 0xfc else set(range(4, 20))
        assert len(old) == len(new)
        assert all(a == b for i, (a, b) in enumerate(zip(old, new)) if i not in excluded)
        assert all(w[kind][k] == oldwire[name][kind][k] for k in ('i', 'tns', 'port', 'status'))
        wire_count += 1
    first = w['first_twelve_pdus']
    assert len(first) == 12 and all(b['seq'] == (a['seq'] + 1) % 256 for a, b in zip(first, first[1:]))

short = list(csv.DictReader((packet / 'short-polls.csv').open()))
long = list(csv.DictReader((packet / 'long-polls.csv').open()))
early = [r for r in short + long if r['phase'].startswith('first-pdus-')]
assert len(early) == 546 and all(int(r['SEQ']) == int(r['SI']) == 0 for r in early)
holds = [r for r in long if r['phase'].startswith('hold-')]
assert len(holds) == 600 and all(int(r['SEQ']) == int(r['SI']) == 0 for r in long)
startup = []
doc = read('startup-headers.json')
for case in doc['cycles']:
    name = case['cycle']
    frames = case['first_twelve_pdus']
    times, sequence = [], []
    for row in frames:
        b = bytes.fromhex(row['avtp_header'])
        assert len(b) == 24 and b[0] == 2 and b[4:12] == bytes(8)
        assert b[1] == 0x81 and b[3] & 1 == 0 and b[22] & 0x10 == 0
        times.append(struct.unpack('>I', b[12:16])[0])
        sequence.append(b[2])
    steps = []
    for a, b in zip(times, times[1:]):
        d = (b - a) & 0xffffffff
        steps.append(d if d < 0x80000000 else d - 0x100000000)
    assert all(124999 <= x <= 125020 for x in steps[1:])
    assert [(f['record'], f['tap_ns'], s) for f, s in zip(frames, sequence)] == [(f['i'],f['tns'],f['seq']) for f in oldwire[name]['first_twelve_pdus']]
    row = dict(cycle=name, first_two_hex=[f'{x:08x}' for x in times[:2]], first_step_ns=steps[0], later_steps_min_ns=min(steps[1:]), later_steps_max_ns=max(steps[1:]), tap_spacing_ns=frames[1]['tap_ns']-frames[0]['tap_ns'], tap_bind_interval_ns=frames[0]['tap_ns']-case['bind_command']['tap_ns'], sequence=sequence, tv=1, tu=0, mr=0, sp=0)
    c = case['controller']
    polls = sorted((p for p in short if p['cycle'] == name), key=lambda p: int(p['response_us']))
    assert polls[0]['phase'] == 'pre-bind' and int(polls[0]['EARLY']) == int(polls[0]['LATE']) == 0
    nz = [p for p in polls if int(p['EARLY']) or int(p['LATE'])]
    if nz:
        t = int(nz[0]['response_us'])
        assert t < c['unbind_submit_us']
        callback = next(r for r in read('rule-increments.json') if r['cycle'] == name)
        assert c['callback_us'] == callback['t']
        for p in nz:
            assert int(p['EARLY']) + int(p['LATE']) == 1
        row['controller_intervals_us'] = [t-c['bind_submit_us'], c['unbind_submit_us']-t, c['callback_us']-t]
        row['first_nonzero_utc'] = nz[0]['utc']
        row['frames_rx'] = int(nz[0]['FRX'])
    else:
        assert 124999 <= steps[0] <= 125019
    assert set(case['media_ether_types']) == {'22f0'}
    startup.append(row)
assert [r['first_step_ns'] for r in startup] == [-23612829,521369096,124999,124999]

restores = {}
for endpoint in ('start','end'):
    rows = read('restore-'+endpoint+'.json')['observations']
    assert len(rows) == 43
    observed = {}
    for r in rows:
        key = (r['role'],r['category'],r['command'],r['descriptor_type'],r['descriptor_index'],r['observation'])
        assert key not in observed
        assert r['status'] == (0 if r['category'] == 'bindings' else 'SUCCESS')
        if r['category'] == 'bindings': assert r['value'] == {'connections':0}
        assert r['source_line'] > 0 and r['source_file'].endswith('-'+endpoint+'.jsonl')
        observed[key] = r['value']
    restores[endpoint] = observed
assert restores['start'] == restores['end']
groups = {}
for key in restores['start']:
    groups[str(key[:2])] = groups.get(str(key[:2]),0)+1
assert sorted(groups.values()) == [1,2,2,2,4,4,14,14]

private_hits = []
for f in list(packet.iterdir()) + [repo/'docs/findings/653_DISCONNECT_ORDER_BENCH.md']:
    if not f.is_file(): continue
    data = f.read_bytes().lower()
    for value in original_peer:
        variants = [value, value.hex().encode(), ':'.join(f'{b:02x}' for b in value).encode()]
        if any(v in data for v in variants): private_hits.append(f.name)
assert not private_hits
assert len(original_peer) == 1
result = dict(passed=True, cycles=len(cycles), nonidentity_wire_headers_equal=wire_count, table_intervals_matched=len(intervals), matrix_counts=counts, early_polls=len(early), long_hold_polls=len(holds), restoration_observations_per_endpoint=43, restore_inventory=groups, peer_entity_identity_matches=private_hits, startup=startup, gptp_correlation='NOT RUN: capture filters and retained EtherTypes contain no gPTP reference; no cross-clock mapping supplied.')
print(json.dumps(result,indent=2))
