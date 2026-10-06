#!/usr/bin/env python3
"""Independent, offline B13 receipt checks; no hardware or network operations.

Usage: python3 audit_evidence.py REPOSITORY PUBLIC_EVIDENCE_DIRECTORY
PUBLIC_EVIDENCE_DIRECTORY contains evidence-tree.json and author/ from the
published evidence commit b2bb3c89096c8fd4712a39677bae96e5987ccbbd.
"""
import collections
import csv
import hashlib
import json
from pathlib import Path
import re
import sys

repo, public = map(Path, sys.argv[1:])
p = public / 'author'
doc = (repo / 'docs/findings/667_TALKER_START_BENCH.md').read_text()
def read(name):
    return json.loads((p / name).read_text())
def lines(name):
    return [json.loads(x) for x in (p / name).read_text().splitlines()]
def csvrows(name):
    return list(csv.DictReader((p / name).open()))
def delta(new, old):
    value = (new - old) & 0xffffffff
    return value - 0x100000000 if value & 0x80000000 else value
def decode(x):
    b = bytes.fromhex(x.get('header', x.get('raw_header', '')))
    assert len(b) == 24
    assert b[0] in (2, 4)
    fields = {'sequence': b[2], 'mr': (b[1] >> 3) & 1, 'tu': b[3] & 1}
    if b[0] == 2:
        fields.update(tv=b[1] & 1, sp=(b[22] >> 4) & 1,
                      avtp_timestamp=int.from_bytes(b[12:16], 'big'))
    for k, v in fields.items():
        if k in x:
            assert int(x[k]) == v, (k, x[k], v)
    return fields

checked = 0
for entry in json.loads((public/'evidence-tree.json').read_text())['tree']:
    f = p / entry['path']
    if entry['type'] != 'blob' or not f.exists():
        continue
    b = f.read_bytes()
    assert len(b) == entry['size']
    assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest() == entry['sha']
    checked += 1
assert checked == 1446
print('PASS: 1446 downloaded public files match published Git blobs; three narrative handoffs excluded.')
for name, size, sha in re.findall(r'^\| ([\w.-]+) \| (\d+) \| ([0-9a-f]{64}) \|$', doc, re.M):
    b = (p / name).read_bytes()
    assert len(b) == int(size) and hashlib.sha256(b).hexdigest() == sha
print('PASS: all seven receipt sizes and SHA-256 values in findings page match.')

headers = csvrows('startup-first-ten.csv')
cycles = csvrows('startup-cycles.csv')
assert len(headers) == 1000 and len(cycles) == 100
hist = collections.Counter()
early_cycles = []
lead = []
holds = []
for i, c in enumerate(cycles, 1):
    tag = f'start-{i:03}'
    assert c['cycle'] == tag
    wire = read(tag+'-wire.json')
    streams = [s for s in wire['streams'] if (s['role'], s['subtype']) == ('dut', 2)]
    assert len(streams) == 1
    s = streams[0]
    hs = [h for h in headers if h['cycle'] == tag]
    assert len(s['first']) == len(hs) == 10
    values = []
    for j, (a, h) in enumerate(zip(s['first'], hs), 1):
        assert int(h['pdu']) == j and a['header'] == h['raw_header']
        d = decode(a)
        decode(h)
        assert d['tv'] == 1 and d['tu'] == 0 and d['sp'] == 0
        values.append(d)
    assert all(b['sequence'] == (a['sequence']+1)%256 for a,b in zip(values,values[1:]))
    steps = [delta(b['avtp_timestamp'], a['avtp_timestamp']) for a,b in zip(values,values[1:])]
    assert steps == s['first_ten_timestamp_steps_ns']
    assert steps[0] == s['first_step_ns'] == int(c['first_step_ns'])
    assert s['gaps'] == int(c['sequence_gaps']) == 0
    assert s['count'] == int(c['packets'])
    steady = float(c['steady_period_ns'])
    assert steady == s['steady_period_ns']
    assert steady-steps[0] == float(c['first_offset_from_steady_ns'])
    for j,(h,v) in enumerate(zip(hs,values)):
        assert delta(v['avtp_timestamp'],values[-1]['avtp_timestamp'])-(j-9)*steady == float(h['relative_to_tenth_pdu_trend_ns'])
    data = read(tag+'.json')
    assert data['result']['result'] == c['result'] == 'OK'
    bind, unbind = data['bind_unbind']
    assert bind['ev'] == 'bind' and unbind['ev'] == 'unbind'
    assert bind['status'] == unbind['status'] == 'Success'
    holds.append((unbind['t_cmd']-bind['t'])/1000)
    assert holds[-1] >= 2000
    assert len(data['formats']) == 1
    fmt = data['formats'][0]
    assert fmt['talker_status'] == fmt['listener_status'] == 'Success.'
    assert fmt['talker_format'] == fmt['listener_format']
    polls = [r for r in data['polls'] if r['phase'] not in ('pre-bind','post-unbind')]
    assert len(polls) == 7 and all(r['status'] == 'Success.' for r in polls)
    early = max(r['counters']['EARLY'] for r in polls)
    late = max(r['counters']['LATE'] for r in polls)
    assert early == data['early'] == int(c['early'])
    assert late == data['late'] == int(c['late']) == 0
    assert (early == 1) == (steps[0] < 0)
    if early:
        early_cycles.append(tag)
        first = next(r for r in polls if r['counters']['EARLY'])
        lead.append((unbind['t_cmd']-first['t_rsp'])/1000)
    hist[steps[0]] += 1
    expected = f'| {i:03} | {early} | {late} | {values[0]["sequence"]} | {steps[0]} | {steady-steps[0]:.1f} |'
    assert expected in doc
assert len(early_cycles) == 14 and min(lead) == 1900.062
assert dict(hist) == {int(k):v for k,v in read('startup-summary.json')['first_step_ns']['histogram'].items()}
assert all(f'| {k} | {v} |' in doc for k,v in hist.items())
print('PASS: 1000 raw startup headers, 100 table rows and histogram independently recomputed.')
print('PASS: EARLY=1 exactly matches 14 negative first steps; all LATE=0; all holds exceed 2000 ms.')
print('Startup minimum lead before unbind:',min(lead),'ms; hold range:',min(holds),max(holds),'ms')

expected_keys = {('dut',dt,idx) for dt,idx in [(0,0),(9,0),(36,0),(5,0),(5,1),(6,0),(6,1)]}|{('peer',5,0),('peer',5,8)}
previous = {}
firsts = {}
lasts = {}
intervals = []
timing_intervals = []
timing_previous = {}
timing_base = {}
counter_names = {5:['MEDIA_LOCKED','MEDIA_UNLOCKED','STREAM_INTERRUPTED','SEQ_NUM_MISMATCH','MEDIA_RESET','TIMESTAMP_UNCERTAIN','TIMESTAMP_VALID','TIMESTAMP_NOT_VALID','UNSUPPORTED_FORMAT','LATE_TIMESTAMP','EARLY_TIMESTAMP','FRAMES_RX'],6:['STREAM_START','STREAM_STOP','MEDIA_RESET','TIMESTAMP_UNCERTAIN','FRAMES_TX'],9:{0:'LINK_UP',1:'LINK_DOWN',5:'GPTP_GM_CHANGED'},36:['LOCKED','UNLOCKED']}
for i in range(145):
    rows = lines(f'counters-soak-{i:03}.jsonl')
    keyed = {(r['role'],r['descriptor_type'],r['descriptor_index']):r for r in rows}
    assert len(rows) == len(keyed) == 9 and set(keyed) == expected_keys
    n = 0
    for k,r in keyed.items():
        if k == ('dut',0,0):
            assert r['status'] == 'NOT_SUPPORTED'
            continue
        assert r['status'] == 'SUCCESS'
        b = bytes.fromhex(r['payload'])
        assert len(b) >= 136
        assert int.from_bytes(b[:2],'big') == k[1] and int.from_bytes(b[2:4],'big') == k[2]
        mask = int.from_bytes(b[4:8],'big')
        assert mask == r['valid_mask']
        counters = {str(bit):int.from_bytes(b[8+4*bit:12+4*bit],'big') for bit in range(32) if mask & (1<<bit)}
        assert counters == r['counters']
        n += len(counters)
        firsts.setdefault(k,r)
        lasts[k] = r
        if k in previous:
            old = previous[k]
            assert old['valid_mask'] == mask
            intervals.append((r['response_ns']-old['response_ns'])/1e9)
            assert 0 < intervals[-1] < 60
            assert all(v >= old['counters'][bit] for bit,v in counters.items())
        error_bits = (1,2,3,8,9,10) if k[1] == 5 else (1,4,5) if k[1] == 9 else (1,) if k[1] == 36 else ()
        assert all(counters.get(str(bit),0) == 0 for bit in error_bits)
        previous[k] = r
    assert n == 61
    timing = lines(f'timing-soak-{i:03}.jsonl')
    assert len(timing) == 4
    for r in timing:
        k=(r['role'],r['command'])
        assert r['status']=='SUCCESS'
        health={f:r[f] for f in ('gm_fingerprint','as_capable','path_fingerprint','path_count','domain') if f in r}
        assert health == timing_base.setdefault(k,health)
        if 'as_capable' in r: assert r['as_capable'] is True
        if k in timing_previous:
            timing_intervals.append((r['response_ns']-timing_previous[k])/1e9)
            assert 0 < timing_intervals[-1] < 60
        timing_previous[k]=r['response_ns']
for k,r in firsts.items():
    end=lasts[k]
    for bit,v in r['counters'].items():
        name=counter_names[k[1]][int(bit)]
        dtype={5:'STREAM_INPUT',6:'STREAM_OUTPUT',9:'AVB_INTERFACE',36:'CLOCK_DOMAIN'}[k[1]]
        ev=end['counters'][bit]
        assert f'| {k[0]} | {dtype} | {k[2]} | {name} | {v} | {ev} | {ev-v} |' in doc
soak=csvrows('soak-cycles.csv')
assert len(soak)==145
events=lines('run-events.jsonl')
polls=[r for r in events if r['event']=='soak_poll']
assert len(polls)==145
wire_previous={}
raw_matches=0
for i,(c,event) in enumerate(zip(soak,polls)):
    tag=f'soak-{i:03}'
    assert c['cycle']==event['cycle']==tag and not event['errors']
    assert c['elapsed_s']==f'{event["elapsed_s"]:.3f}'
    assert f'| {tag} | {c["elapsed_s"]} | {c["counter_errors"]} | {c["segment_sequence_gaps"]} | {c["overlap_recovered"]} |' in doc
    wire=read(tag+'-wire.json')
    assert sum(s['gaps'] for s in wire['streams'])==int(c['segment_sequence_gaps'])
    assert len(wire['streams'])==4
    for s in wire['streams']:
        key=(s['role'],s['subtype'],s['stream_unique_id'])
        first,last=s['first'][0]['tap_ns'],s['last'][-1]['tap_ns']
        if key in wire_previous:assert first<=wire_previous[key],(tag,key)
        wire_previous[key]=last
    for row in lines('counters-'+tag+'.jsonl'):
        if row['role']!='dut':continue
        matches=[r for r in wire['counter_wire'] if r['role']=='dut' and r['message_type']==1 and not r['unsolicited'] and r['sequence']==row['sequence'] and r['descriptor_type']==row['descriptor_type'] and r['descriptor_index']==row['descriptor_index']]
        assert matches,(tag,row['sequence'])
        if row['status']=='SUCCESS':
            assert any(bytes.fromhex(r['raw'])[24:160]==bytes.fromhex(row['payload'])[:136] for r in matches)
        else:
            assert any(r['status']==11 for r in matches)
        raw_matches+=1
max_poll=max(b['elapsed_s']-a['elapsed_s'] for a,b in zip(polls,polls[1:]))
end=next(r for r in events if r['event']=='soak_end')
assert not end['stopped'] and end['elapsed_s']>=7200
assert f'{max_poll:.3f}'=='55.727' and f'{end["elapsed_s"]:.3f}'=='7203.971'
formats=[r for r in read('soak-controller-receipts.json') if r['ev']=='formats']
assert len(formats)==4
assert all(r['talker_format']==r['listener_format'] and r['talker_status']==r['listener_status']=='Success.' for r in formats)
print('PASS: all 145 soak table rows, 580 stream-segment boundaries and four soak format pairs.')
print('PASS:',raw_matches,'DUT solicited counter responses cross-matched to retained raw wire payloads/status.')
print('PASS: all 1305 counter responses; 1160 successful payloads decoded into 61 supported counters per checkpoint.')
print('PASS: no assigned error increase or counter decrease; all 61 document counter rows match raw payloads.')
print('PASS: 580 timing responses have stable GM/path and asserted asCapable; maximum response intervals:',max(intervals),max(timing_intervals),'s')

recover=read('overlap-recovery.json')
assert recover['segment_gaps']==recover['recovered_gaps']==9 and recover['unrecovered_gaps']==0
for gap in recover['gaps']:
    packets=gap['recovered']['packets']
    assert packets[0]['tap_ns']==gap['before']['tap_ns'] and packets[-1]['tap_ns']==gap['after']['tap_ns']
    assert packets[0]['header']==gap['before']['header'] and packets[-1]['header']==gap['after']['header']
    for a,b in zip(packets,packets[1:]):
        assert b['tap_ns']>a['tap_ns'] and b['sequence']==(a['sequence']+1)%256
    for h in packets:decode(h)
print('PASS: all nine overlap recovery paths connect identical endpoints through consecutive independently decoded headers.')
drops=[]
for f in sorted(p.glob('667-b13-*.pcap.json')):
    r=json.loads(f.read_text())
    ds=[int(re.match(r'\s*(\d+)',s)[1]) for s in r['summary'] if 'dropped by kernel' in s]
    assert all(v==0 for v in ds)
    if not ds:drops.append(f.name)
assert len(list(p.glob('667-b13-soak-*.pcap.json')))==435
assert len(list(p.glob('667-b13-start-*.pcap.json')))==300
assert drops==['667-b13-soak-063-vlan.pcap.json']
print('PASS: 735 capture receipts; only declared soak-063 VLAN drop statistic is absent.')

def effective(name):
    rows=lines(name)
    seen={}
    for r in rows:
        k=(r['role'],r['category'],r.get('descriptor_type'),r.get('descriptor_index'))
        assert k not in seen
        cat=r['category']
        if cat=='inventory':
            v={f:r[f] for f in ('counts','configuration')}
        else:
            assert r['status']==(0 if cat=='binding' else 'SUCCESS')
            fs={'format':['value'],'clock':['value'],'binding':['connections'],'map':['mapping_count','effective_sha256']}[cat]
            v={f:r[f] for f in fs}
            if cat=='binding':assert r['connections']==0
        seen[k]=v
    assert len(rows)==44
    assert sum(k[1]=='binding' for k in seen)==18
    assert sum(k[1]=='format' for k in seen)==18
    assert sum(k[1]=='map' for k in seen)==4
    assert sum(k[1]=='clock' for k in seen)==2
    return seen
assert effective('restore-start.jsonl')==effective('restore-end.jsonl')
c=read('console-restore.json')
assert c['servo_start_hex']==c['servo_end_hex'] and c['audio_start_hex']==c['audio_end_hex']
assert c['nvm_end']['image_sequence']-c['nvm_start']['image_sequence']==3
assert c['nvm_end']['commits_ok']-c['nvm_start']['commits_ok']==3
assert all(c['nvm_end'][x]==c['nvm_start'][x]==0 for x in ['commits_failed','dirty','stale'])
print('PASS: 42 effective-state observations, two inventories, console bytes and explicit NVM residuals.')
print('LIMIT: raw complete captures, physical identity and clock correlation were not independently remeasured.')
