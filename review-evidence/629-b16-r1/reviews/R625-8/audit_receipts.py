#!/usr/bin/env python3
"""Independently recount public measurements, hashes and restore records.
Usage: audit_receipts.py REPO AUTHOR_PACKET OUTPUT
"""
import csv
import hashlib
import json
import re
import statistics
import subprocess
import sys
from pathlib import Path

repo,packet,out=map(lambda p:Path(p).resolve(),sys.argv[1:])
def j(p):return json.loads((packet/p).read_text())
def jl(p):return [json.loads(s) for s in (packet/p).read_text().splitlines() if s.strip()]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
record={}
manifest=json.loads((packet.parent/'MANIFEST.json').read_text())
files=[x for x in manifest if x['file'].startswith('author-r8/')]
bad=[x['file'] for x in files if sha(packet.parent/x['file'])!=x['published_sha256']]
record['publication']={'commit':'b0134c639a35a731787dd62586fca6c4500842c8','files':len(files),'mismatches':bad,'manifest_sha256':sha(packet.parent/'MANIFEST.json')}
assert not bad
text=(repo/'docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md').read_text()
section=text[text.index('## Dev 5603c353, 2026-10-12: lane B16'):]
hash_rows=[]
for m in re.finditer(r'^\| `([^`]+)`[^\n]*?\| ([\d,]+) \| `([a-f0-9]{64})` \|$',section,re.M):
    name,size,digest=m.groups()
    if not (packet/name).is_file():continue
    hash_rows.append({'file':name,'bytes':int(size.replace(',','')),'sha256':digest,'equal':sha(packet/name)==digest and (packet/name).stat().st_size==int(size.replace(',',''))})
record['page_hash_rows']=hash_rows
assert all(x['equal'] for x in hash_rows)
grade=j('summary/b0-2/c-b9-grade.json');blocks=grade['blocks']
med=[statistics.median(b[f'ch{i}']['thdn_db'] for b in blocks) for i in (0,1)]
good=[b for b in blocks if b['events']==0 and all(b[f'ch{i}']['thdn_db']<=med[i]+3 for i in (0,1))]
degraded=[b['block'] for b in blocks if b not in good]
overlap=min(j('summary/b0-2/align-a-c.json')['compared_frames'],j('summary/b0-2/align-b-c.json')['compared_frames']) if 'compared_frames' in j('summary/b0-2/align-a-c.json') else None
record['b0']={'blocks':len(blocks),'floor':len(good),'floor_medians':[round(statistics.median(b[f'ch{i}']['thdn_db'] for b in good),2) for i in (0,1)],'degraded':degraded,'alignment':j('summary/b0-2/align-a-c.json'),'inside_degraded':len([b for b in degraded if b<34]),'outside_degraded':len([b for b in degraded if b>=34])}
assert len(good)==169 and 45 not in degraded and record['b0']['inside_degraded']==23
record['positive_control']={}
for run in ('pts2','b0-2','bcrf','baaf'):
    d=j(f'summary/{run}/d-extcap-pair.json');r=[]
    for ch,tone in ((0,997),(1,9973)):
        b=d['rows'][ch][f'tone_{tone}']['per_block']
        active=[i for i,x in enumerate(b) if x['level_dbfs']>-200]
        inside=b[active[0]+1:active[-1]+1]
        median=statistics.median(x['thdn_db'] for x in inside)
        r.append({'wholly_inside':len(inside),'floor':sum(x['thdn_db']<=median+3 for x in inside),'preplayback':active[0]})
    record['positive_control'][run]=r
record['following']={}
for run in ('bcrf','baaf'):
    trace=list(csv.DictReader((packet/f'r2/{run}-poll-trace.tsv').open(),delimiter='\t'))
    states=[int(x['0x8f8'],16)&7 for x in trace]
    first=states.index(4)
    bracket=[float(trace[first-1]['start_after_set_s']),float(trace[first]['start_after_set_s'])+float(trace[first]['length_ms'])/1000]
    r=j(f'r2/{run}-poll-receipt.json'); marks=r['marks_after_set_s']
    window=[x for x in trace if marks['window-start']<=float(x['start_after_set_s']) and float(x['start_after_set_s'])+float(x['length_ms'])/1000<=marks['window-end']]
    steps=[{'poll':i,'start':float(trace[i-1]['start_after_set_s']),'end':float(x['start_after_set_s'])+float(x['length_ms'])/1000,'states':[states[i-1],states[i]],'previous':int(trace[i-1]['0x8d4'],16)&65535,'now':int(x['0x8d4'],16)&65535} for i,x in enumerate(trace) if i and x['0x8d4']!=trace[i-1]['0x8d4']]
    ev=jl(f'runs/{run}/events.jsonl');sets=[{k:e[k] for k in ('who','src','status','readback','ok')} for e in ev if e['kind']=='set-clock']
    assert all(e['ok'] and e['src']==e['readback'] for e in sets)
    trim=[]
    for x in window:
        t=int(x['0x8f8'],16)>>16;trim.append((t if t<32768 else t-65536)/16)
    record['following'][run]={'polls':len(trace),'locked_bracket':bracket,'window_polls':len(window),'window_states':sorted(set(int(x['0x8f8'],16)&7 for x in window)),'trim_extrema': [min(trim),max(trim)],'steps':steps,'steps_after_lock':sum(s['poll']>first for s in steps),'clock_sets':sets,'grade':j(f'summary/{run}/c-b9-grade.json')['summary'],'raw_hash':r['raw']['sha256']}
    assert len(window)==596 and all((int(x['0x8f8'],16)&7)==4 for x in window)
    assert not record['following'][run]['steps_after_lock']
record['source_comparisons']=j('r2/source-receipt.json')['compare']
record['run_restoration']={}
for run in ('loop1','loop2','pts1','pts2','pts3','b0','b0-2','bcrf','baaf'):
    es=jl(f'runs/{run}/events.jsonl')
    found=next(e for e in es if e['kind']=='as-found')
    final=next(e for e in es if e['kind']=='final')
    keys=[k for k in found if k not in ('t','kind')]
    differences=[k for k in keys if found[k]!=final[k]]
    record['run_restoration'][run]={'fields_compared':len(keys),'differences':differences,'recorded_equal':final['equal_to_found']}
    assert not differences
acmp=j('summary/loop2/acmp-peer-tap.json')['acmp']
tx=[e for e in acmp if e['msg']=='CONNECT_TX_COMMAND']
record['loopback']={'probes':len(tx),'probe_spacing_ms':(tx[1]['t']-tx[0]['t'])*1000,'responses':sum(e['msg']=='CONNECT_TX_RESPONSE' for e in acmp)}
assert len(tx)==2 and record['loopback']['responses']==0
raws=j('RAW-ARTIFACTS.json')['files'];raw_hashes={x['sha256'] for x in raws}
record['source_raw_bindings']={k:v['sha256'] in raw_hashes for k,v in j('r2/source-receipt.json')['reads'].items()}
assert all(record['source_raw_bindings'].values())
record['census']={}
for suffix in ('','b','c'):
    a={(x.get('role','')+':'+x['what']):x for x in jl(f'restore/census-start{suffix}.jsonl') if 'what' in x}
    b={(x.get('role','')+':'+x['what']):x for x in jl(f'restore/census-end{suffix}.jsonl') if 'what' in x}
    def clean(x):return {k:v for k,v in x.items() if k not in ('t','t_tx','t_rx','seq','sequence_id','rtt_ms')}
    different=[k for k in a if clean(a[k])!=clean(b[k])]
    record['census'][suffix or 'b16']={'reads':len(a),'equal':len(a)-len(different),'different':different}
    assert len(a)==45 and len(different)==1
record['author_source_validation']=j('gates/r8/results.json')
record['regenerated_check']={'sha256':sha(out/'scratch/regenerated-check.py'),'published_sha256':sha(packet/'tools/check_b16_figures.py'),'equal':(out/'scratch/regenerated-check.py').read_bytes()==(packet/'tools/check_b16_figures.py').read_bytes()}
assert record['regenerated_check']['equal']
record['manager_source_validation']='No manager source bank asserted or inferred'
(out/'receipts'/'independent-audit.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'publication_files':len(files),'hash_rows':len(hash_rows),'b0_floor':len(good),'following_cases':list(record['following']),'census':record['census']}))
