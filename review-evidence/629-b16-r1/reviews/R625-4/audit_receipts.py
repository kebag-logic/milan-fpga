#!/usr/bin/env python3
"""Independent reduced-receipt audit. Usage: audit_receipts.py AUTHOR_PACKET OUT_JSON."""
import csv
import hashlib
import json
import statistics
import sys
from collections import Counter
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

root, output = map(Path, sys.argv[1:3])
def read(name):
    p = root / name
    if p.suffix == '.jsonl':
        return [json.loads(x) for x in p.read_text().splitlines()]
    return json.loads(p.read_text(), parse_float=Decimal)
def digest(name):
    return hashlib.sha256((root / name).read_bytes()).hexdigest()
def display(x):
    return str(Decimal(x).quantize(Decimal('.01'), rounding=ROUND_HALF_UP))
def ranges(indices):
    r = []
    for i in indices:
        if r and i == r[-1][1] + 1:
            r[-1][1] = i
        else:
            r.append([i, i])
    return r
def signed(x, bits):
    return x - (1 << bits) if x & (1 << (bits - 1)) else x

out = {'grades': {}, 'positive_control': {}, 'polls': {}, 'restores': {}, 'loopback': {}}
for run in ('b0-2', 'bcrf', 'baaf'):
    d = read(f'summary/{run}/c-b9-grade.json')
    blocks = d['blocks']
    med = [statistics.median(b[f'ch{c}']['thdn_db'] for b in blocks if b['events'] == 0) for c in (0, 1)]
    floor = [b for b in blocks if b['events'] == 0 and all(b[f'ch{c}']['thdn_db'] <= med[c]+3 for c in (0,1))]
    bad = [b['block'] for b in blocks if b not in floor]
    tones = []
    for c in (0, 1):
        row = {'floor_median': display(statistics.median(b[f'ch{c}']['thdn_db'] for b in floor)),
               'all_median': display(med[c]), 'worst': display(max(b[f'ch{c}']['thdn_db'] for b in blocks))}
        assert Decimal(row['floor_median']) == d['summary'][f'ch{c}_floor']['thdn_db_median']
        assert Decimal(row['all_median']) == d['summary'][f'ch{c}_all']['thdn_db_median']
        tones.append(row)
    aligns = {p: read(f'summary/{run}/align-{p}-c.json') for p in 'ab'}
    for a in aligns.values():
        assert a['frames_differing'] == 0 and not a['slips'] and a['comparison'] == 'full 24-bit values'
    complete = min(a['covered_recording_frames'][1] for a in aligns.values()) // 48000
    out['grades'][run] = {'blocks':len(blocks), 'floor_blocks':len(floor), 'degraded_runs':ranges(bad),
       'degraded_inside':sum(i < complete for i in bad), 'degraded_beyond':sum(i >= complete for i in bad),
       'compared_frames':{p:a['compared_equal'] for p,a in aligns.items()}, 'tones':tones,
       'events':len(d['events']), 'phase_net_frames':d['phase_net_frames']}
    if run == 'b0-2':
        rec = read('r2/b0-2-receipt.json')
        assert ranges(bad) == rec['degraded_runs']
        assert len(floor) == 169 and len(bad) == 131 and sum(i < complete for i in bad) == 23
        ev = read('runs/b0-2/events.jsonl')
        last_bind = max(e['t'] for e in ev if e['kind']=='bind')
        launch = next(e['started']['mcasp'] for e in ev if e['kind']=='captures-started')
        out['b0_start_after_bind_s'] = round(launch+2-last_bind,3)
        assert 25.9 < launch+2-last_bind < 26.1
    else:
        assert len(floor) == 300 and len(d['events']) == 0
        upstream = read(f'summary/{run}/a-peer-tap.json')
        up = []
        for c,hz in enumerate((997,9973)):
            t = upstream['channels'][c][f'tone_{hz}']; pb=t['per_block']
            up.append({'median':display(statistics.median(b['thdn_db'] for b in pb)),
                       'worst':display(max(b['thdn_db'] for b in pb))})
        out['grades'][run]['upstream_tones'] = up

for run in ('pts2','b0-2','bcrf','baaf'):
    d=read(f'summary/{run}/d-extcap-pair.json'); result=[]
    for c,hz in enumerate((997,9973)):
        pb=d['rows'][c][f'tone_{hz}']['per_block']
        playing=[i for i,b in enumerate(pb) if b['level_dbfs'] > -200]
        interior=list(range(playing[0]+1, playing[-1]+1 if playing[-1]==len(pb)-1 else playing[-1]))
        mid=statistics.median(pb[i]['thdn_db'] for i in interior)
        good=[i for i in interior if pb[i]['thdn_db'] <= mid+3]
        result.append({'all':len(pb),'pre_playback':[i for i in range(playing[0])],
                       'interior':len(interior),'floor':len(good),
                       'degraded':[i for i in interior if i not in good]})
        assert result[-1]['pre_playback']==[0,1]
        assert (len(interior),len(good))==((13,11) if run=='pts2' else (303,303))
    out['positive_control'][run]=result

raws={f['path']:f for f in read('RAW-ARTIFACTS.json')['files']}
for run in ('bcrf','baaf'):
    rec=read(f'r2/{run}-poll-receipt.json')
    assert rec['raw']['sha256']==raws[f'{run}/poll-run.jsonl']['sha256']
    assert rec['events']['sha256']==digest(f'runs/{run}/events.jsonl')
    rows=list(csv.DictReader((root/f'r2/{run}-poll-trace.tsv').open(),delimiter='\t'))
    marks=rec['marks_after_set_s']; win=[r for r in rows if marks['window-start'] <= Decimal(r['start_after_set_s']) and Decimal(r['start_after_set_s'])+Decimal(r['length_ms'])/1000 <= marks['window-end']]
    words=[{k:int(v,16) for k,v in r.items() if k.startswith('0x')} for r in win]
    states=Counter(w['0x8f8']&7 for w in words)
    assert states=={4:596}
    extrema={
      'trim_ppm': [min(signed(w['0x8f8']>>16,16)/16 for w in words),max(signed(w['0x8f8']>>16,16)/16 for w in words)],
      'crf_rate_ppm': [min(signed(w['0x748'],32)/512 for w in words),max(signed(w['0x748'],32)/512 for w in words)],
      'aaf_rate_ppm': [min(signed(w['0x8e4'],32)/512 for w in words),max(signed(w['0x8e4'],32)/512 for w in words)]}
    for k in ('trim_ppm','crf_rate_ppm'):
        assert extrema[k]==rec['spans']['window-start..window-end'][k]
    k=next(i for i,r in enumerate(rows) if int(r['0x8f8'],16)&7==4)
    assert int(rows[k-1]['0x8f8'],16)&7==3
    bracket=[Decimal(rows[k-1]['start_after_set_s']),Decimal(rows[k]['start_after_set_s'])+Decimal(rows[k]['length_ms'])/1000]
    changes=[]
    for i,(before,after) in enumerate(zip(rows,rows[1:]),1):
        if before['0x8d4']!=after['0x8d4']:
            changes.append({'polls':[i-1,i], 'states':[int(x['0x8f8'],16)&7 for x in (before,after)],
                            'dups':[int(x['0x8d4'],16)&65535 for x in (before,after)]})
    assert [x['polls'] for x in changes]==[x['polls'] for x in rec['slip_lb_steps']]
    assert all(4 not in x['states'] for x in changes)
    assert all(w['0x8d8']==0 for w in words)
    out['polls'][run]={'window_polls':len(win),'lock_bracket_s':bracket,'extrema':extrema,
                       'transitions':changes,'window_servo_words':dict(Counter(f"{w['0x8f8']&65535:04x}" for w in words)),
                       'window_aaf_stat':sorted({f"{w['0x8e0']:08x}" for w in words})}

for run in ('loop1','loop2','pts1','pts2','b0','b0-2','pts3','bcrf','baaf'):
    ev=read(f'runs/{run}/events.jsonl'); final=next(e for e in ev if e['kind']=='final')
    assert final['equal_to_found'] and final['differ']==[]
    formats=[e for e in ev if e['kind']=='format-check']
    assert all(e['ok'] for e in formats)
    changes=[{k:e[k] for k in ('tag','who','src','status','readback','ok')} for e in ev if e['kind']=='set-clock']
    assert all(e['status']=='SUCCESS' and e['src']==e['readback'] and e['ok'] for e in changes)
    if run in ('bcrf','baaf'):
        assert [(x['who'],x['src']) for x in changes]==[('peer',0),('dut',1 if run=='bcrf' else 2),('dut',0),('peer',1)]
        unbind_t=max(e['t'] for e in ev if e['kind']=='unbind')
        peer_restore=next(e['t'] for e in ev if e['kind']=='set-clock' and e['tag']=='restore' and e['who']=='peer')
        assert peer_restore>unbind_t
        assert final['clk-dut']==0 and final['clk-peer']==1
    else:
        assert not changes
    out['restores'][run]={'equal_to_found':True,'format_checks':len(formats),'clock_changes':changes}
for run in ('loop1','loop2'):
    ev=read(f'runs/{run}/events.jsonl');poll=[e for e in ev if e['kind']=='listener-poll']
    assert len(poll)==14
    assert all(e['rx']['stream_id']=='0000000000000000' and e['peer_tx0']['conn_count']==0 and e['frames_rx']==0 for e in poll)
    out['loopback'][run]={'unresolved_polls':14}
tap=read('summary/loop2/acmp-peer-tap.json')
probes=[e for e in tap['acmp'] if e['msg']=='CONNECT_TX_COMMAND']
assert len(probes)==2 and not any(e['msg']=='CONNECT_TX_RESPONSE' for e in tap['acmp'])
out['loopback']['probe_spacing_ms']=(probes[1]['t']-probes[0]['t'])*1000
source=read('r2/source-receipt.json')
for name,r in source['reads'].items():
    assert r['sha256']==raws[f'source/{name}.json']['sha256']
out['source_comparisons']=source['compare']
out['controller_clock_readbacks']={}
for run in ('bcrf','baaf'):
    lines=[x['line'] for x in read(f'runs/{run}/ctl.jsonl') if 'line' in x and 'cmd' in x['line']]
    pairs=[]
    for i,x in enumerate(lines):
        if x['cmd']!='SET_CLOCK_SOURCE':
            continue
        y=next(y for y in lines[i+1:] if y['cmd']=='GET_CLOCK_SOURCE' and y['role']==x['role'])
        assert x['status']==y['status']=='SUCCESS'
        assert x['payload'][:12]==y['payload'][:12]
        pairs.append({'role':x['role'],'selected':int(x['payload'][8:12],16),
                      'readback':int(y['payload'][8:12],16),'set_sequence':x['seq'],'get_sequence':y['seq']})
    assert [(x['role'],x['selected']) for x in pairs]==[('peer',0),('dut',1 if run=='bcrf' else 2),('dut',0),('peer',1)]
    out['controller_clock_readbacks'][run]=pairs
volatile={'t','seq','rtt_ms','sequence_id','t_tx','t_rx'}
def stable(v):
    if isinstance(v,dict):return {k:stable(x) for k,x in v.items() if k not in volatile}
    if isinstance(v,list):return [stable(x) for x in v]
    return v
out['censuses']={}
for start,end in [('start','end'),('startb','endb'),('startc','endc'),('start','endc')]:
    a=read(f'restore/census-{start}.jsonl');b=read(f'restore/census-{end}.jsonl')
    assert a[0]['type']==b[0]['type']=='start' and len(a)==len(b)==46
    changed=[x['what'] for x,y in zip(a[1:],b[1:]) if stable(x)!=stable(y)]
    assert len(changed)==1 and 'avb' in changed[0].lower(),changed
    out['censuses'][start+'..'+end]={'reads':45,'equal':44,'different_read':changed}
out['status']='PASS'
output.write_text(json.dumps(out,indent=2,default=str)+'\n')
print('PASS: independent grade, overlap, playback, poll, restore, loopback and raw-hash checks')
