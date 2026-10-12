#!/usr/bin/env python3
"""Independent arithmetic and restoration audit of public reduced receipts.
Usage: python audit_receipts.py REPO AUTHOR_PACKET OUT
Raw audio and private source-state captures are not read.
"""
import collections
import csv
import hashlib
import json
from pathlib import Path
import statistics as st
import subprocess
import sys

repo, packet, out = (Path(x).resolve() for x in sys.argv[1:])
result = {'audit': 'Independent reduced-receipt arithmetic; no raw capture remeasurement'}
def read(path):
    p = packet / path
    if p.suffix == '.jsonl':
        return [json.loads(x) for x in p.read_text().splitlines() if x.strip()]
    return json.loads(p.read_text())
def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def median(xs):
    return round(st.median(xs), 2)

manifest = json.loads((packet.parent / 'MANIFEST.json').read_text())
ours = [x for x in manifest if x['file'].startswith('author-r7/')]
assert len(ours) == len({x['file'] for x in ours})
for item in ours:
    p = packet / item['file'].removeprefix('author-r7/')
    assert p.is_file(), item['file']
    assert digest(p) == item['published_sha256'], item['file']
    assert (item['original_sha256'] != item['published_sha256']) == item['path_redacted'], item['file']
result['publication'] = dict(files=len(ours), hashes_match=True,
                             declared_redactions=sum(x['path_redacted'] for x in ours))

grades = {}
for run in ['b0-2', 'bcrf', 'baaf']:
    g = read(f'summary/{run}/c-b9-grade.json')
    blocks = g['blocks']
    free = [b for b in blocks if not b['events']]
    med = [st.median(b[f'ch{c}']['thdn_db'] for b in free) for c in (0, 1)]
    floor = [b for b in free if all(b[f'ch{c}']['thdn_db'] <= med[c]+3 for c in (0, 1))]
    bad = [b['block'] for b in free if b not in floor]
    assert len(floor) == g['summary']['blocks_at_floor']
    assert bad == g['summary']['degraded_event_free_blocks']
    floor_med = [median(b[f'ch{c}']['thdn_db'] for b in floor) for c in (0, 1)]
    all_med = [median(b[f'ch{c}']['thdn_db'] for b in blocks) for c in (0, 1)]
    assert floor_med == [g['summary'][f'ch{c}_floor']['thdn_db_median'] for c in (0, 1)]
    assert not g['events'] and g['silent_frames'] == 0
    alignment = {p:read(f'summary/{run}/align-{p}-c.json') for p in 'ab'}
    for v in alignment.values():
        assert v['verdict']=='SAMPLE-EXACT' and not v['slips'] and v['frames_differing']==0
    span = min(x['compared_equal'] for x in alignment.values()) / 48000
    inside = [i for i in bad if i+1 <= span]
    grades[run] = dict(blocks=len(blocks), floor_blocks=len(floor), floor_medians=floor_med,
                      all_medians=all_med, degraded=bad, inside_count=len(inside),
                      beyond_count=len(bad)-len(inside), overlap_seconds=span,
                      compared_frames={p:x['compared_equal'] for p,x in alignment.items()})
assert grades['b0-2']['inside_count']==23 and grades['b0-2']['beyond_count']==108
assert 45 not in grades['b0-2']['degraded'] and all(i in grades['b0-2']['degraded'] for i in [43,44,46,54])
result['grades']=grades

controls={}
for run in ['pts2','b0-2','bcrf','baaf']:
    g=read(f'summary/{run}/d-extcap-pair.json')
    tones=[g['rows'][c][f'tone_{hz}']['per_block'] for c,hz in enumerate([997,9973])]
    dec=read(f'summary/{run}/d-loop-decode.json')
    whole=[i for i in range(len(tones[0])) if i*48000 >= dec['first_decoded_frame']
           and (i+1)*48000-1 <= dec['last_decoded_frame']]
    assert not any(i in whole for i in [0,1,2])
    floor=[i for i in whole if all(ts[i]['thdn_db'] <= st.median(t['thdn_db'] for t in ts)+3 for ts in tones)]
    assert len(whole)==(13 if run=='pts2' else 303)
    assert len(floor)==(11 if run=='pts2' else 303)
    controls[run]=dict(whole_playback_blocks=len(whole), floor_blocks=len(floor),
                      decoded_frames=dec['decoded'],net_step_frames=dec['net_step_frames'],torn=dec['torn'])
result['positive_controls']=controls

result['tap_attribution']={}
for run in ['bcrf','baaf']:
    j=read(f'summary/{run}/a-peer-tap.json')
    result['tap_attribution'][run]=[]
    for c,hz in enumerate([997,9973]):
        t=j['channels'][c][f'tone_{hz}']; m=st.median(x['thdn_db'] for x in t['per_block'])
        assert abs(m-t['median']['thdn_db'])<0.00011
        result['tap_attribution'][run].append(dict(median_db=round(m,2),worst_db=t['worst_thdn_db']))

polls={}
def signed(x,bits):
    return x-(1<<bits) if x&(1<<(bits-1)) else x
for run in ['bcrf','baaf']:
    trace=list(csv.DictReader((packet/f'r2/{run}-poll-trace.tsv').open(),delimiter='\t'))
    r=read(f'r2/{run}-poll-receipt.json')
    def start(t): return float(t['start_after_set_s'])
    def end(t): return start(t)+float(t['length_ms'])/1000
    def word(t,k): return int(t[k],16)
    def state(t): return word(t,'0x8f8')&7
    first=next(i for i,t in enumerate(trace) if start(t)>=0 and state(t)==4)
    assert state(trace[first-1])==3
    bracket=[round(start(trace[first-1]),3),round(end(trace[first]),3)]
    bounds=r['spans']['window-start..window-end']
    window=[t for t in trace if start(t)>=bounds['from_s'] and end(t)<=bounds['to_s']]
    states=collections.Counter(state(t) for t in window)
    assert states=={4:596}
    trims=[signed(word(t,'0x8f8')>>16,16)/16 for t in window]
    crf=[signed(word(t,'0x748'),32)/512 for t in window]
    assert [min(trims),max(trims)]==bounds['trim_ppm']
    assert [min(crf),max(crf)]==bounds['crf_rate_ppm']
    assert all(word(t,'0x8d8')==0 for t in trace)
    changes=[]
    for earlier,later in zip(trace,trace[1:]):
        if word(later,'0x8d4')!=word(earlier,'0x8d4'):
            changes.append(dict(bracket=[start(earlier),round(end(later),3)],
                                states=[state(earlier),state(later)],
                                delta=word(later,'0x8d4')-word(earlier,'0x8d4')))
    assert all(x['states'] in ([0,0],[3,3]) and x['delta']==2 for x in changes)
    assert sum(x['states']==[0,0] for x in changes)==5
    assert sum(x['states']==[3,3] for x in changes)==(1 if run=='bcrf' else 2)
    assert all(word(t,'0x8e0')==(0 if run=='bcrf' else 0x001e0007) for t in window)
    polls[run]=dict(rows=len(trace),lock_bracket=bracket,window_polls=len(window),
                    trim_ppm=[min(trims),max(trims)],crf_rate_ppm=[min(crf),max(crf)],
                    status_low_counts=dict(collections.Counter(hex(word(t,'0x8f8')&65535) for t in window)),
                    slip_steps=changes)
    assert digest(packet/f'runs/{run}/events.jsonl')==r['events']['sha256']
result['polls']=polls

restores={}
for run in ['loop1','loop2','pts1','pts2','b0','b0-2','pts3','bcrf','baaf']:
    es=read(f'runs/{run}/events.jsonl')
    initial=next(e for e in es if e['kind']=='as-found')
    final=next(e for e in es if e['kind']=='final')
    diffs=[]
    for key in initial.keys()-{'t','kind'}:
        aa,bb=initial[key],final[key]
        if isinstance(aa,dict):
            aa={k:v for k,v in aa.items() if k!='flags'}
            bb={k:v for k,v in bb.items() if k!='flags'}
        if aa!=bb: diffs.append(key)
    assert not diffs and final['equal_to_found']
    formats=[e for e in es if e['kind']=='format-check']
    assert all(e['ok'] and e['talker_fmt']==e.get('listener_after',e['listener_fmt']) for e in formats)
    sets=[e for e in es if e['kind']=='set-clock']
    assert all(e['src']==e['readback'] and e['status']=='SUCCESS' for e in sets)
    if run in ['bcrf','baaf']:
        assert [(e['who'],e['src']) for e in sets]==[('peer',0),('dut',1 if run=='bcrf' else 2),('dut',0),('peer',1)]
        assert sets[-2]['t'] < min(e['t'] for e in es if e['kind']=='unbind')
        assert max(e['t'] for e in es if e['kind']=='unbind') < sets[-1]['t']
    restores[run]=dict(fields_compared=len(initial)-2,equals_as_found=True,formats=len(formats),
                        sets=[dict(role=e['who'],selection=e['src'],readback=e['readback']) for e in sets])
result['restores']=restores
def census(name):
    def stable(e):
        if isinstance(e,dict):
            return {k:stable(v) for k,v in e.items() if k not in ('t','t_tx','t_rx','seq','sequence_id','rtt_ms')}
        if isinstance(e,list): return [stable(v) for v in e]
        return e
    return [stable(e) for e in read('restore/'+name) if e.get('type')!='start']
a,b=census('census-start.jsonl'),census('census-endc.jsonl')
diffs=[dict(read=i,what=x.get('what'),role=x.get('role')) for i,(x,y) in enumerate(zip(a,b)) if x!=y]
assert len(a)==len(b)==45 and len(diffs)==1
result['full_census']=dict(reads=45,equal=44,differing=diffs)

j=read('summary/loop2/acmp-peer-tap.json')
commands=[e for e in j['acmp'] if e['msg']=='CONNECT_TX_COMMAND']
responses=[e for e in j['acmp'] if e['msg']=='CONNECT_TX_RESPONSE']
assert len(commands)==2 and not responses
result['loopback']=dict(probes=2,responses=0,probe_interval_ms=(commands[1]['t']-commands[0]['t'])*1000)
result['source_comparisons']=read('r2/source-receipt.json')['compare']
result['source_read_hashes']={k:v['sha256'] for k,v in read('r2/source-receipt.json')['reads'].items()}
raw=read('RAW-ARTIFACTS.json')['files']
raw_hashes={x['sha256'] for x in raw}
assert all(v in raw_hashes for v in result['source_read_hashes'].values())
for run in ['bcrf','baaf']:
    assert read(f'r2/{run}-poll-receipt.json')['raw']['sha256'] in raw_hashes
result['raw_binding']='Source reads and poll hashes match the public raw inventory; private bytes not read.'
(out/'receipts/independent-receipt-audit.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS: publication hashes, block arithmetic, attribution overlap, positive-control boundaries, poll decoding, clock readbacks, restoration and raw-hash citations')
