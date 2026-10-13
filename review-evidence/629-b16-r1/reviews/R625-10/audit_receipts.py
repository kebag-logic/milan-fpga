#!/usr/bin/env python3
"""Independent receipt arithmetic and publication integrity.
Usage: python audit_receipts.py REPO PACKET MANIFEST OUTPUT
"""
import csv
import datetime
import hashlib
import json
from pathlib import Path
import statistics
import subprocess
import sys

repo, packet, manifest, output = [Path(x).resolve() for x in sys.argv[1:]]
out = {}
def read(name):
    return json.loads((packet/name).read_text())
def events(run):
    return [json.loads(x) for x in (packet/f'runs/{run}/events.jsonl').read_text().splitlines()]
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def require(test, message):
    if not test:
        raise AssertionError(message)

entries = [x for x in json.loads(manifest.read_text()) if x['file'].startswith('author-r10/')]
bad = [x['file'] for x in entries if digest(packet/x['file'].split('/',1)[1]) != x['published_sha256']]
require(not bad, str(bad))
own = dict(line.split('  ',1)[::-1] for line in (packet/'MANIFEST.sha256').read_text().splitlines())
own = {k.removeprefix('./'):v for k,v in own.items()}
bad_orig = [x['file'] for x in entries if x['file'].split('/',1)[1] != 'MANIFEST.sha256' and own.get(x['file'].split('/',1)[1]) != x['original_sha256']]
require(not bad_orig, str(bad_orig))
out['publication'] = dict(evidence_commit='5775cfa78dc9250ea1b689fc2cfa8e20c41281bb', manifest_sha256=digest(manifest), author_files=len(entries), all_published_hashes_equal=True, original_hashes_equal_own_manifest=True, path_redacted=sum(x['path_redacted'] for x in entries))

# Per-block arithmetic is recomputed independently of the figures checker.
grades = {}
for run in ('b0-2','bcrf','baaf'):
    g = read(f'summary/{run}/c-b9-grade.json')
    bs = g['blocks']
    med = [statistics.median(b[c]['thdn_db'] for b in bs) for c in ('ch0','ch1')]
    floor = [b for b in bs if not b['events'] and all(b[c]['thdn_db'] <= med[i]+3 for i,c in enumerate(('ch0','ch1')))]
    degraded = [b['block'] for b in bs if b not in floor]
    runs = []
    for i in degraded:
        if runs and runs[-1][1]+1 == i: runs[-1][1] = i
        else: runs.append([i,i])
    r = dict(frames=g['frames'], seconds=g['seconds'], events=len(g['events']), blocks=len(bs), floor_blocks=len(floor), median_thdn_db=[round(x,2) for x in med], floor_median_db=[round(statistics.median(b[c]['thdn_db'] for b in floor),2) for c in ('ch0','ch1')], degraded_runs=runs)
    aligns = {pt:read(f'summary/{run}/align-{pt}-c.json') for pt in ('a','b')}
    r['alignments'] = aligns
    if run == 'b0-2':
        require(r['floor_blocks']==169 and r['floor_median_db']==[-123.98,-123.95], 'B0 floor')
        require(runs[:4]==[[0,18],[28,31],[43,44],[46,54]], 'B0 block runs')
        r['degraded_within_first_34_whole_blocks'] = sum(i<34 for i in degraded)
        r['degraded_beyond'] = sum(i>=34 for i in degraded)
        require((len(degraded), r['degraded_within_first_34_whole_blocks'],r['degraded_beyond'])==(131,23,108), 'overlap attribution')
    else:
        require(r['floor_blocks']==300 and not r['events'], 'following floor')
    grades[run]=r
out['grades']=grades

polls={}
for run, want in [('bcrf',[2.585,3.161]),('baaf',[6.602,7.180])]:
    rows = list(csv.DictReader((packet/f'r2/{run}-poll-trace.tsv').open(),delimiter='\t'))
    r = read(f'r2/{run}-poll-receipt.json')
    first = next(i for i,x in enumerate(rows) if int(x['0x8f8'],16)&7 == 4)
    bracket=[float(rows[first-1]['start_after_set_s']),round(float(rows[first]['start_after_set_s'])+float(rows[first]['length_ms'])/1000,3)]
    require(bracket==want, 'LOCKED bracket')
    start,end=(r['marks_after_set_s'][k] for k in ('window-start','window-end'))
    window=[x for x in rows if start<=float(x['start_after_set_s']) and float(x['start_after_set_s'])+float(x['length_ms'])/1000<=end]
    states=[int(x['0x8f8'],16)&7 for x in window]
    transitions=[]
    for a,b in zip(rows,rows[1:]):
        if a['0x8d4'] != b['0x8d4']:
            transitions.append(dict(previous=int(a['n']),next=int(b['n']),start=float(a['start_after_set_s']),end=round(float(b['start_after_set_s'])+float(b['length_ms'])/1000,3),from_dups=int(a['0x8d4'],16)&65535,to_dups=int(b['0x8d4'],16)&65535,states=[int(x['0x8f8'],16)&7 for x in (a,b)]))
    require(len(window)==596 and set(states)=={4}, 'window polls')
    require(all(4 not in x['states'] for x in transitions), 'slip after lock')
    require(all(int(x['0x8d8'],16)==0 for x in window), 'TDM slip')
    require(digest(packet/f'runs/{run}/events.jsonl')==r['events']['sha256'], 'poll event hash')
    polls[run]=dict(first_locked_poll=first,bracket_s=bracket,window_polls=len(window),locked_polls=states.count(4),slip_transitions=transitions,raw_hash=r['raw']['sha256'],tdm_slip_zero=True)
out['polls']=polls

clocks={}
restores={}
for run in ('loop1','loop2','pts1','pts2','b0','b0-2','pts3','bcrf','baaf'):
    es=events(run)
    sets=[{k:v for k,v in x.items() if k in ('tag','who','src','status','readback','ok')} for x in es if x['kind']=='set-clock']
    require(all(x['ok'] and x['src']==x['readback'] and x['status']=='SUCCESS' for x in sets), 'clock readback')
    clocks[run]=sets
    # The run's comparison is backed by its before and after snapshots.
    initial=next(x for x in es if x['kind']=='as-found')
    terminal=next(x for x in es if x['kind']=='final')
    fields=[k for k in initial if k not in ('kind','t')]
    differences=[k for k in fields if initial[k]!=terminal.get(k)]
    require(not differences and terminal['equal_to_found'], 'restore snapshot comparison')
    restores[run]=dict(fields_compared=fields, equal_to_found=True, differences=differences)
    formats=[x for x in es if x['kind']=='format-check']
    require(all(x['ok'] and x['talker_fmt']==x.get('listener_after', x['listener_fmt']) for x in formats), 'binding format')
out['clock_readbacks']=clocks
out['restore_records']=restores

acmp=read('summary/loop2/acmp-peer-tap.json')['acmp']
origin=next(x['t'] for x in acmp if x['msg']=='DISCONNECT_RX_COMMAND')
probe=[x['t'] for x in acmp if x['msg']=='CONNECT_TX_COMMAND' and x.get('talker')=='<peer-eid>' and x.get('listener')=='<peer-eid>']
out['loopback']=dict(probes_ms_from_unbind=[round((t-origin)*1000,3) for t in probe],unreflected=not any(x['msg']=='CONNECT_TX_RESPONSE' and x.get('talker')=='<peer-eid>' for x in acmp))
require(len(probe)==2 and out['loopback']['unreflected'], 'loopback probes')

positive={}
for run in ('pts2','b0-2','bcrf','baaf'):
    g=read(f'summary/{run}/d-extcap-pair.json')
    r=[]
    for i,key in [(0,'tone_997'),(1,'tone_9973')]:
        pb=g['rows'][i][key]['per_block']
        require(all(pb[j]['level_dbfs'] < -200 for j in (0,1)) and pb[2]['level_dbfs'] > -200, 'playback start')
        med=statistics.median(x['thdn_db'] for x in pb[3:])
        r.append(dict(pre_playback=[0,1],start_block=2,whole_blocks=len(pb)-3,floor_blocks=sum(x['thdn_db']<=med+3 for x in pb[3:])))
    require(all(x['floor_blocks']==(11 if run=='pts2' else 303) for x in r), 'positive floor')
    positive[run]=r
out['positive_control']=positive

source=read('r2/source-receipt.json')
out['source_comparisons']={k:v for k,v in source.items() if k not in ('tool','reads')}
raw=read('RAW-ARTIFACTS.json')['files']
rawhash={x['sha256'] for x in raw}
require(all(v['sha256'] in rawhash for v in source['reads'].values()), 'source hashes')
require(all(x['raw_hash'] in rawhash for x in polls.values()), 'poll raw hashes')
out['raw_hash_bindings']=True
timing = {}
for run in ('b0-2', 'bcrf', 'baaf'):
    es = events(run)
    start = next(x['started']['mcasp'] for x in es if x['kind']=='captures-started') + 2.0
    last_bind = max(x['t'] for x in es if x['kind']=='bind')
    r = dict(recording_after_last_bind_s=round(start-last_bind, 3), playback_lead_s=2)
    if run=='b0-2':
        r['recording_start_CEST'] = datetime.datetime.fromtimestamp(start, datetime.timezone(datetime.timedelta(hours=2))).strftime('%H:%M:%S.%f')[:-5]
        require(round(start-last_bind)==26 and r['recording_start_CEST']=='06:38:05.2', 'B0 timing')
    else:
        mark = next(x['t'] for x in es if x.get('tag')=='window-mark-0')
        set_t = next(x['t'] for x in es if x['kind']=='set-clock' and x['tag']==run)
        r.update(first_mark_after_set_s=round(mark-set_t,3), first_mark_before_recording_s=round(start-mark,3))
    timing[run]=r
require('sleep 2; ' in (packet/'tools/run_b16.py').read_text(), 'playback lead in published command')
out['timing']=timing

tap_medians={}
for run in ('bcrf','baaf'):
    tap=read(f'summary/{run}/a-peer-tap.json')
    taps=[]
    for i,key in [(0,'tone_997'),(1,'tone_9973')]:
        vals=[x['thdn_db'] for x in tap['channels'][i][key]['per_block']]
        taps.append(dict(median=round(statistics.median(vals),2), worst=round(max(vals),2)))
    require([x['median'] for x in taps]==([-123.98,-123.97] if run=='bcrf' else [-123.98,-123.98]), 'point-a medians')
    require(all(x['worst']==-123.93 for x in taps), 'point-a worst')
    tap_medians[run]=taps
out['point_a_medians']=tap_medians

def stable(x):
    if isinstance(x,dict):
        return {k:stable(v) for k,v in x.items() if k not in {'t','seq','rtt_ms','sequence_id','t_tx','t_rx'}}
    if isinstance(x,list):
        return [stable(v) for v in x]
    return x
censuses={}
for suffix in ('','b','c'):
    before=[stable(json.loads(x)) for x in (packet/f'restore/census-start{suffix}.jsonl').read_text().splitlines()]
    after=[stable(json.loads(x)) for x in (packet/f'restore/census-end{suffix}.jsonl').read_text().splitlines()]
    require(before[0]['type']=='start' and after[0]['type']=='start', 'census header')
    differences=[a['what'] for a,b in zip(before[1:],after[1:]) if a!=b]
    require(len(before)==len(after)==46 and len(differences)==1, 'census restore')
    censuses[suffix or 'a']=dict(reads=45,equal=44,different=differences)
out['censuses']=censuses

(output/'receipts/receipt-audit.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: publication hashes, independent block statistics, lock brackets, slip states, clock readbacks, binding formats, loopback origin, positive-control counts and reduced-receipt hash bindings.')
