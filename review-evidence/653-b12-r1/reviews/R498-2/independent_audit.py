"""Offline review: python3 -B independent_audit.py PACKET_R2 PACKET_R1 REPO PUBLICATION_MANIFEST.

Inputs are published evidence projections, not complete physical captures.
No device or network access; no input writes; stdout is a public-safe receipt.
"""
import csv
import hashlib
import json
import re
import struct
import sys
from collections import Counter
from pathlib import Path

p, old, repo, publication = map(Path, sys.argv[1:])
read = lambda name: json.loads((p / name).read_text())
page = (repo / 'docs/findings/653_DISCONNECT_ORDER_BENCH.md').read_text()
manifest = []
published = {r['file'].removeprefix('author-r2/'):r for r in json.loads(publication.read_text())}
redactions = []
for line in (p / 'MANIFEST.sha256').read_text().splitlines():
    sha, name = line.split('  ', 1)
    actual = hashlib.sha256((p / name).read_bytes()).hexdigest()
    assert actual == published[name]['published_sha256'], name
    assert sha == published[name]['original_sha256'], name
    if actual != sha:
        assert published[name]['path_redacted'], name
        redactions.append(name)
    manifest.append(name)
assert set(manifest) == {f.name for f in p.iterdir() if f.is_file()} - {'MANIFEST.sha256'}

wire = {x['cycle']: x for f in sorted(p.glob('wire-receipts-*.json')) for x in json.loads(f.read_text())}
prior = {x['cycle']: x for f in sorted(old.glob('wire-receipts-*.json')) for x in json.loads(f.read_text())}
cycles = {x['cycle']: x for f in sorted(p.glob('cycles-*.json')) for x in json.loads(f.read_text())}
assert len(wire) == len(cycles) == 182
private_ids = set()
for name, row in wire.items():
    c, r, u = [bytes.fromhex(row[k]['raw']) for k in ('command', 'response', 'unlock')]
    assert c[0] == r[0] == 0xfc and c[1] & 15 == 8 and r[1] & 15 == 9
    assert r[2] >> 3 == 0 and u[2] >> 3 == 0
    assert c[12:20] == r[12:20] and c[28:36] == r[28:36]
    assert c[38:40] == r[38:40] and c[48:50] == r[48:50]
    assert u[0] == 0xfb and u[1] & 15 == 1 and u[22:24] == bytes.fromhex('8029')
    assert u[4:12] == c[28:36] and u[12:20] == c[12:20]
    assert u[24:26] == bytes.fromhex('0005') and u[26:28] == c[38:40]
    valid = int.from_bytes(u[28:32], 'big')
    assert valid & 15 == 15
    ml, mu, si, seq = struct.unpack('>4I', u[32:48])
    assert (ml, mu, si, seq) == (1, 1, 0, 0)
    assert row['command']['i'] < row['response']['i'] < row['unlock']['i']
    interval = (row['unlock']['tns'] - row['response']['tns']) / 1000
    assert interval > 0 and interval == cycles[name]['response_unlock_us']
    table_rows=[line for line in page.splitlines() if line.startswith('| '+name+' |') and '| SUCCESS |' in line]
    assert len(table_rows)==1,name
    shown=re.search(r'\| R / ([0-9.]+) \| NC \|',table_rows[0])
    assert shown and shown.group(1)==f'{interval:.3f}',name
    assert cycles[name]['library_state'] == 'NotConnected'
    assert cycles[name]['selected_capture'] == row['capture']
    assert cycles[name]['sequence_max'] == cycles[name]['interruption_max'] == 0
    assert cycles[name]['earlier_unlock_notifications'] == 0
    assert cycles[name]['stream_gaps'] == 0
    assert len(row['first_twelve_pdus']) == 12
    ss = [x['seq'] for x in row['first_twelve_pdus']]
    assert all((b-a) % 256 == 1 for a, b in zip(ss, ss[1:]))
    # Compare against the older public raw headers outside allowed identity fields.
    for key in ('command', 'response', 'unlock'):
        b = bytes.fromhex(row[key]['raw'])
        prior_hex = prior[name][key]['raw']
        token = '<controller-host-id>'
        if token in prior_hex:
            # The earlier public packet replaced part of this identity with text.
            width = len(b)*2 - len(prior_hex.replace(token, ''))
            assert prior_hex.count(token)==1 and width in (12,16)
            prior_hex = prior_hex.replace(token, '0'*width)
        a = bytes.fromhex(prior_hex)
        assert len(a) == len(b)
        allowed = set(range(4, 12)) | set(range(12, 36)) | set(range(40, 46)) if a[0] == 0xfc else set(range(4, 20))
        assert all(x == y for i, (x, y) in enumerate(zip(a, b)) if i not in allowed)
        if a[0] == 0xfc:
            for off in (20, 28):
                if b[off:off+8] == bytes.fromhex('0000000000000003'):
                    private_ids.add(a[off:off+8])
        # Current protocol identity fields contain only declared role tokens or DUT identity.
        permitted = {bytes.fromhex(x) for x in ('0000000000000000', '0000000000000001', '0000000000000003', '020000fffe000001')}
        for off in ((12, 20, 28) if b[0] == 0xfc else (4, 12)):
            assert b[off:off+8] in permitted

assert len(private_ids) == 1
identity_hits = []
for value in private_ids:
    variants = [value.hex().encode(), b':'.join(f'{v:02x}'.encode() for v in value)]
    # EUI-64 carries its EUI-48 identity around the inserted ff:fe pair.
    if value[3:5] == bytes.fromhex('fffe'):
        mac = value[:3] + value[5:]
        variants.extend([mac.hex().encode(), b':'.join(f'{v:02x}'.encode() for v in mac)])
    for f in list(p.iterdir()) + [repo/'docs/findings/653_DISCONNECT_ORDER_BENCH.md']:
        if f.is_file() and any(v in f.read_bytes().lower() for v in variants):
            identity_hits.append(f.name)
assert not identity_hits, identity_hits

polls = [x for name in ('short-polls.csv', 'long-polls.csv') for x in csv.DictReader((p/name).open())]
assert len(polls) == 1510
assert all(x['status'] == 'Success.' and int(x['SEQ']) == int(x['SI']) == 0 for x in polls)
assert sum(x['phase'].startswith('first-pdus-') for x in polls) == 546
assert sum(x['phase'].startswith('hold-') for x in polls) == 600
matrix = Counter((c['direction'], c['kind'], c['requested_hold_ms']) for c in cycles.values() if c['phase']=='exact' and c['requested_hold_ms'] != 600000)
assert len(matrix) == 28 and set(matrix.values()) == {5}
assert Counter(c['direction'] for c in cycles.values()) == {'A':91, 'B':91}
assert sum(c['phase'] != 'exact' for c in cycles.values()) == 40

startup = []
doc = read('startup-headers.json')
for case in doc['cycles']:
    fs = case['first_twelve_pdus']; headers = [bytes.fromhex(f['avtp_header']) for f in fs]
    assert len(headers) == 12
    assert all(len(h)==24 and h[0]==2 and h[1]==0x81 and h[3]&1==0 and h[22]&0x10==0 and h[4:12]==bytes(8) for h in headers)
    ts = [struct.unpack('>I', h[12:16])[0] for h in headers]
    steps = [struct.unpack('>i', ((b-a) % 2**32).to_bytes(4,'big'))[0] for a,b in zip(ts, ts[1:])]
    seq = [h[2] for h in headers]
    assert all((b-a)%256==1 for a,b in zip(seq,seq[1:]))
    before = wire[case['cycle']]
    assert [(f['record'],f['tap_ns'],h[2]) for f,h in zip(fs,headers)] == [(f['i'],f['tns'],f['seq']) for f in before['first_twelve_pdus']]
    assert case['bind_command']['tap_ns'] == before['bind_command_tap_ns']
    assert set(case['media_ether_types']) == {'22f0'}
    output = dict(cycle=case['cycle'], initial_timestamps_hex=[f'{t:08x}' for t in ts[:2]], first_step_ns=steps[0], remaining_step_range_ns=[min(steps[1:]),max(steps[1:])], first_tap_spacing_ns=fs[1]['tap_ns']-fs[0]['tap_ns'], bind_to_first_tap_ns=fs[0]['tap_ns']-case['bind_command']['tap_ns'], tv=1,tu=0,mr=0,sp=0)
    cs = case['controller']
    nonzero = sorted([r for r in polls if r['cycle']==case['cycle'] and r['phase'] != 'pre-bind' and (int(r['EARLY']) or int(r['LATE']))],key=lambda r:int(r['response_us']))
    if nonzero:
        first = nonzero[0]; t = int(first['response_us'])
        assert t < cs['unbind_submit_us']
        assert all(int(r['EARLY'])==int(r['LATE'])==0 for r in polls if r['cycle']==case['cycle'] and r['phase']=='pre-bind')
        output.update(first_nonzero_utc=first['utc'], first_nonzero_frames=int(first['FRX']), bind_to_read_us=t-cs['bind_submit_us'], read_before_unbind_us=cs['unbind_submit_us']-t, read_to_callback_us=cs['callback_us']-t)
    assert str(steps[0]) in page
    startup.append(output)
assert [r['first_step_ns'] for r in startup] == [-23612829,521369096,124999,124999]
assert 'ether[40:2]=0x22f0' in (p/'run.py').read_text()
assert 'ether[44:2]=0x22f0' in (p/'run.py').read_text()

start, end = read('restore-start.json'),read('restore-end.json')
keep = ('observation','role','category','command','descriptor_type','descriptor_index','status','value')
canon = lambda d:{r['observation']:{k:r[k] for k in keep} for r in d['observations']}
assert len(start['observations']) == len(end['observations']) == len(canon(start)) == 43
assert canon(start) == canon(end)
groups = Counter((r['role'],r['category']) for r in start['observations'])
assert dict(groups) == {('dut','bindings'):4,('dut','formats'):4,('dut','maps'):2,('dut','clocks'):2,('peer','bindings'):14,('peer','formats'):14,('peer','maps'):2,('peer','clocks'):1}
for endpoint in (start,end):
    assert all(r['status'] == (0 if r['category']=='bindings' else 'SUCCESS') for r in endpoint['observations'])
    assert all(r['value']['connections']==0 for r in endpoint['observations'] if r['category']=='bindings')
    for role, dt, n in [('dut',5,2),('dut',6,2),('peer',5,10),('peer',6,4)]:
        for cat in ('bindings','formats'):
            assert sorted(r['descriptor_index'] for r in endpoint['observations'] if (r['role'],r['descriptor_type'],r['category'])==(role,dt,cat)) == list(range(n))

print(json.dumps(dict(passed=True,manifest_files=len(manifest),publication_redactions=redactions,cycles=182,wire_headers=546,nonidentity_bytes_unchanged=True,peer_identity_scan_hits=identity_hits,privacy_limit='Independent scan covers peer entity ID and derivable MAC; names and serials rely on published retained-source audit.',counter_polls=1510,early_polls=546,hold_polls=600,startup=startup,restore_observations_per_endpoint=43,unbound_observations_per_endpoint=18,gptp_correlation='NOT RUN: no retained gPTP reference or measured clock mapping',capture_limit='Complete captures are indexed, not present in this packet.'),indent=2))
