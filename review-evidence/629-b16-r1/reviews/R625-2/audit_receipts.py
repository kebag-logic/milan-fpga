#!/usr/bin/env python3
"""Independent arithmetic over published reductions, never private captures.

Usage: audit_receipts.py REPOSITORY AUTHOR_EVIDENCE PUBLICATION_MANIFEST OUTPUT
OUTPUT is a public-safe JSON receipt. Raw capture fidelity remains outside this check.
"""
import csv
import hashlib
import json
from pathlib import Path
import re
import statistics as st
import sys

repo, root, manifest, output = map(Path, sys.argv[1:5])
def read(name):
    return json.loads((root/name).read_text())
def lines(name):
    return [json.loads(x) for x in (root/name).read_text().splitlines() if x.strip()]
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def signed(x, n):
    return x-(1<<n) if x&(1<<(n-1)) else x
out = {'scope': 'Published reductions only; no private raw capture read', 'checks': {}}
checks = out['checks']
pub = {x['file'].split('/',1)[1]: x for x in json.loads(manifest.read_text()) if x['file'].startswith('author-r2/')}
bad = [name for name, row in pub.items() if sha(root/name)!=row['published_sha256']]
assert not bad, bad
checks['publication_hashes'] = {'files': len(pub), 'mismatches': bad}
doc = (repo/'docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md').read_text()
section = doc[doc.index('## Dev 5603c353, 2026-10-12: lane B16'):]
hashes=[]
for line in section.splitlines():
    m=re.match(r'\| `([^`]+)`[^|]*\| ([\d,]+) \| `([a-f0-9]{64})` \|',line)
    if not m: continue
    name,size,digest=m.groups()
    assert name in pub, name
    actual=sha(root/name)
    assert digest in (pub[name]['original_sha256'],actual),(name,digest,actual)
    if actual==digest: assert (root/name).stat().st_size==int(size.replace(',','')),name
    hashes.append({'file':name,'quoted_hash':digest,'published_hash':actual,'publication_changed':actual!=digest})
checks['quoted_evidence_hashes']=hashes
raw={x['path']:x for x in read('RAW-ARTIFACTS.json')['files']}
raw_rows=0
for line in section.splitlines():
    cols=[x.strip() for x in line.split('|')[1:-1]]
    if len(cols)!=4 or not re.fullmatch(r'`[a-f0-9]{64}`',cols[3]):continue
    names=re.findall(r'`([^`]+)`',cols[1]);runs=re.findall(r'`([^`]+)`',cols[0])
    if not names or not runs:continue
    for run in runs:
        r=raw[run+'/'+names[0]]
        assert r['sha256']==cols[3].strip('`'),(run,names[0])
        if cols[2]!='Withheld':assert r['bytes']==int(cols[2].replace(',','')),(run,names[0])
    raw_rows+=1
checks['raw_hash_inventory']={'table_rows':raw_rows,'claim':'Quoted inventory entries agree; unavailable raw bytes were not rehashed.'}
source=read('r2/source-receipt.json')
for name,r in source['reads'].items():
    assert r['sha256']==raw['source/'+name+'.json']['sha256']
checks['source_reads']={'bound_read_count':len(source['reads']), 'class_map_sha256':source['class_map_sha256'],
                       'comparisons':source['compare'],
                       'limits':'The neutral receipt and extraction procedure were inspected; private reads and private role map were not independently regenerated.'}
grades={}
for run in ('pts1','pts2','pts3','b0-2','bcrf','baaf'):
    g=read(f'summary/{run}/c-b9-grade.json'); b=g['blocks'];s=g['summary']
    free=[x for x in b if x['events']==0]
    med={c:st.median(x[c]['thdn_db'] for x in free) for c in ('ch0','ch1')}
    floor=[x for x in free if all(x[c]['thdn_db']<=med[c]+3 for c in med)]
    degraded=[x['block'] for x in free if x not in floor]
    assert degraded==s['degraded_event_free_blocks'] and len(floor)==s['blocks_at_floor']
    tones={}
    for c in med:
        for name,rows in [('all',b),('floor',floor)]:
            assert round(st.median(x[c]['thdn_db'] for x in rows),2)==s[c+'_'+name]['thdn_db_median']
            assert round(max(x[c]['thdn_db'] for x in rows),2)==s[c+'_'+name]['thdn_db_worst']
        tones[c]={'floor_median':s[c+'_floor']['thdn_db_median'], 'all_median':s[c+'_all']['thdn_db_median'],
                  'worst':s[c+'_all']['thdn_db_worst']}
    aa=read(f'summary/{run}/align-a-c.json');bb=read(f'summary/{run}/align-b-c.json')
    for a in (aa,bb):
        assert a['covered_recording_frames'][0]==0 and a['frames_differing']==0 and a['slips']==[]
        assert a['compared_equal']==a['covered_recording_frames'][1]
        assert a['stream_offset']+a['compared_equal']<=a['stream_frames']
    cover=min(aa['compared_equal'],bb['compared_equal'])
    inside=[i for i in degraded if (i+1)*48000<=cover]
    beyond=[i for i in degraded if i*48000>=cover]
    grades[run]={'blocks':len(b),'floor':len(floor),'degraded':len(degraded),'inside':len(inside),'beyond':len(beyond),
                 'coverage_frames':cover,'events':len(g['events']),'phase_net_frames':g['phase_net_frames'],'tones':tones}
assert grades['b0-2']['inside']==23 and grades['b0-2']['beyond']==108
checks['grades_and_overlaps']=grades
points=[]
for run in ('pts1','pts2','pts3','b0-2','bcrf','baaf'):
    for point,filename in [('a','a-peer-tap.json'),('b','b-dut-tap.json'),('c','c-mcasp.json')]:
        d=read(f'summary/{run}/{filename}')
        if point!='c': assert d['info']['seq_gaps']==0 and d['info']['bad_length']==0
        for channel,key in [(0,'tone_997'),(1,'tone_9973')]:
            t=next(x[key] for x in d['channels'] if x.get('channel')==channel)
            assert abs(st.median(b['thdn_db'] for b in t['per_block'])-t['median']['thdn_db'])<0.00011
            points.append({'run':run,'point':point,'tone':key,'median_thdn_db':t['median']['thdn_db'],
                           'rounded':format(t['median']['thdn_db'],'.2f'),'worst_thdn_db':t['worst_thdn_db']})
checks['point_medians']=points
numeric_rows=0
for lineno,line in enumerate(doc.splitlines(),1):
    if lineno<2279:continue
    cols=[x.strip() for x in line.split('|')[1:-1]]
    if len(cols)!=10 or not re.match(r'`(pts[123]|b0-2|bcrf|baaf)`',cols[0]) or cols[1] not in ('(a)','(b)','(c)'):continue
    run=re.match(r'`([^`]+)`',cols[0])[1]
    point=cols[1][1]
    for key,idx in [('tone_997',5),('tone_9973',8)]:
        p=next(x for x in points if x['run']==run and x['point']==point and x['tone']==key)
        assert cols[idx]==f"{p['median_thdn_db']:.2f} ({p['worst_thdn_db']:.2f})",(lineno,key)
    numeric_rows+=1
checks['document_numeric_point_rows']={'rows':numeric_rows,'thdn_medians_and_worst_equal_receipts':True}
polls={}
for run,src in [('bcrf',1),('baaf',2)]:
    receipt=read(f'r2/{run}-poll-receipt.json')
    assert receipt['raw']['sha256']==raw[f'{run}/poll-run.jsonl']['sha256']
    assert receipt['events']['sha256'] in [pub[f'runs/{run}/events.jsonl']['original_sha256'],sha(root/f'runs/{run}/events.jsonl')]
    rows=list(csv.DictReader((root/f'r2/{run}-poll-trace.tsv').open(),delimiter='\t'))
    def decode(r):
        w={k:int(r[k],16) for k in r if k.startswith('0x')}
        return {'n':int(r['n']),'start':float(r['start_after_set_s']),'end':float(r['start_after_set_s'])+float(r['length_ms'])/1000,
                'state':w['0x8f8']&7,'lo':format(w['0x8f8']&65535,'04x'),
                'trim':signed(w['0x8f8']>>16,16)/16,'crf':signed(w['0x748'],32)/512,
                'aaf_stat':format(w['0x8e0'],'08x'),'aaf':signed(w['0x8e4'],32)/512,
                'lb':w['0x8d4'],'tdm':w['0x8d8']}
    ds=[decode(r) for r in rows]
    win=receipt['spans']['window-start..window-end']
    ws=[x for x in ds if x['start']>=win['from_s'] and x['end']<=win['to_s']]
    assert len(ws)==596 and all(x['state']==4 and x['tdm']==0 for x in ws)
    assert [min(x['trim'] for x in ws),max(x['trim'] for x in ws)]==win['trim_ppm']
    assert [min(x['crf'] for x in ws),max(x['crf'] for x in ws)]==win['crf_rate_ppm']
    lo={v:sum(x['lo']==v for x in ws) for v in set(x['lo'] for x in ws)}
    assert lo==win['mcsrv_stat_lo16']
    steps=[(a,b) for a,b in zip(ds,ds[1:]) if a['lb']!=b['lb']]
    assert len(steps)==len(receipt['slip_lb_steps'])
    for (a,b),s in zip(steps,receipt['slip_lb_steps']):
        assert [a['n'],b['n']]==s['polls'] and [a['lb'],b['lb']]==s['dups']
        assert all(x in (0,3) for x in [a['state'],b['state']])
        assert abs(a['start']-s['after_set_s'][0])<=0.0011 and abs(b['end']-s['after_set_s'][1])<=0.0011
    assert all(x['tdm']==0 for x in ds)
    if src==2:
        assert all(x['aaf_stat']=='001e0007' for x in ws)
        assert [min(x['aaf'] for x in ws),max(x['aaf'] for x in ws)]==win['aafm_rate_ppm_valid']
    ev=lines(f'runs/{run}/events.jsonl')
    sets=[x for x in ev if x['kind']=='set-clock']
    assert [(x['who'],x['src']) for x in sets]==[('peer',0),('dut',src),('dut',0),('peer',1)]
    assert all(x['ok'] and x['status']=='SUCCESS' and x['readback']==x['src'] for x in sets)
    wire=[x['line'] for x in lines(f'runs/{run}/ctl.jsonl') if x.get('line',{}).get('cmd') in ('SET_CLOCK_SOURCE','GET_CLOCK_SOURCE')]
    wire_sets=[]
    for i,x in enumerate(wire):
        assert x['status']=='SUCCESS'
        if x['cmd']=='SET_CLOCK_SOURCE':
            value=int(x['payload'][8:12],16)
            nxt=wire[i+1]
            assert nxt['cmd']=='GET_CLOCK_SOURCE' and nxt['role']==x['role'] and int(nxt['payload'][8:12],16)==value
            wire_sets.append((x['role'],value))
    assert wire_sets==[(x['who'],x['src']) for x in sets]
    marks=[x for x in ev if x['kind']=='mark']
    mark0=next(x for x in marks if x['tag']=='window-mark-0')
    cap=next(x for x in ev if x['kind']=='captures-started')['started']['mcasp']+2
    controls=[x for x in ev if x['kind']=='format-check']
    assert all(x['ok'] and x['set'] is None and x['listener_fmt']==x['talker_fmt'] for x in controls)
    polls[run]={'rows':len(rows),'window':win,'slip_steps':receipt['slip_lb_steps'],
                'clock_sets_readback_verified':wire_sets,
                'counter_mark_after_set_s':round(mark0['t']-sets[1]['t'],3),
                'counter_mark_before_recording_s':round(cap-mark0['t'],3)}
checks['polls_and_clock_readbacks']=polls
restores={}
volatile={'t','seq','rtt_ms','sequence_id','t_tx','t_rx'}
def strip(x):
    if isinstance(x,dict):return {k:strip(v) for k,v in x.items() if k not in volatile}
    if isinstance(x,list):return [strip(v) for v in x]
    return x
for lane,suffix in [('b16',''),('b16b','b'),('b16c','c')]:
    a=lines(f'restore/census-start{suffix}.jsonl');b=lines(f'restore/census-end{suffix}.jsonl')
    changes=[(x,y) for x,y in zip(a,b) if strip(x)!=strip(y)]
    assert len(a)==len(b)==46 and len(changes)==1
    assert changes[0][0]['cmd']=='GET_AVB_INFO' and changes[0][0]['role']=='dut'
    restores[lane]={'entries':46,'equal':45,'difference':'DUT live propagation delay only'}
for run in ('loop1','loop2','pts1','pts2','pts3','b0','b0-2','bcrf','baaf'):
    ev=lines(f'runs/{run}/events.jsonl')
    final=next(x for x in ev if x['kind']=='final')
    assert final['equal_to_found'] and not final['differ']
    found=next(x for x in ev if x['kind']=='as-found')
    assert all(final[k]==v for k,v in found.items() if k not in ('kind','t'))
    if run not in ('bcrf','baaf'): assert not [x for x in ev if x['kind']=='set-clock']
checks['restores']={'census':restores,'run_final_equals_found':9}
first=lines('restore/census-start.jsonl');last=lines('restore/census-endc.jsonl')
changed=[x.get('what') for x,y in zip(first,last) if strip(x)!=strip(y)]
assert len(first)==len(last)==46 and changed==['avb']
checks['restores']['full_b16_start_to_b16c_end']={'entries':46,'equal':45,'only_changed_read':'DUT live propagation delay'}
counter_data={}
for marker in ('startc','endc'):
    counter_data[marker]={}
    for x in lines(f'restore/counters-{marker}.jsonl'):
        if x.get('cmd')!='GET_COUNTERS':continue
        b=bytes.fromhex(x['payload']);dtype=int.from_bytes(b[:2],'big');idx=int.from_bytes(b[2:4],'big')
        values=[int.from_bytes(b[i:i+4],'big') for i in range(8,len(b),4)]
        if dtype==36:counter_data[marker][x['role']+'_clock']=values[:2]
        if dtype==6 and x['role']=='dut':counter_data[marker]['dut_output_'+str(idx)+'_media_reset']=values[2]
assert counter_data['startc']['dut_clock']==[22,21] and counter_data['endc']['dut_clock']==[24,23]
assert counter_data['startc']['peer_clock']==[6,5] and counter_data['endc']['peer_clock']==[8,7]
for idx in (0,1):
    assert counter_data['startc']['dut_output_'+str(idx)+'_media_reset']==0
    assert counter_data['endc']['dut_output_'+str(idx)+'_media_reset']==4
checks['b16c_counters']=counter_data
loop={}
for run,frames in [('loop1',1056000),('loop2',768000)]:
    ev=lines(f'runs/{run}/events.jsonl')
    pol=[x for x in ev if x['kind']=='listener-poll']
    assert len(pol)==14 and all(x['media_locked']==0 and x['frames_rx']==0 for x in pol)
    for name in ('a-peer-tap.json','b-dut-tap.json'):
        d=read(f'summary/{run}/{name}');assert d.get('frames',0)==0
    d=read(f'summary/{run}/d-extcap-pair.json')
    assert d['frames']==frames and all(x['nonzero']==0 for x in d['rows'])
    loop[run]={'listener_polls':14,'media_locked':0,'frames_rx':0,'external_zero_frames':frames}
acmp=read('summary/loop2/acmp-peer-tap.json')['acmp']
probe=[x for x in acmp if x['msg']=='CONNECT_TX_COMMAND']
assert len(probe)==2 and not [x for x in acmp if x['msg']=='CONNECT_TX_RESPONSE']
unbind=next(x for x in acmp if x['msg']=='DISCONNECT_RX_COMMAND')['t']
bind=next(x for x in acmp if x['msg']=='CONNECT_RX_COMMAND')['t']
loop['probe_timing_ms']={'after_unbind':round((probe[0]['t']-unbind)*1000,3),
                         'after_bind':round((probe[0]['t']-bind)*1000,3),
                         'repeat_spacing':round((probe[1]['t']-probe[0]['t'])*1000,3)}
checks['loopback']=loop
out['remaining_figure_discrepancy']={'artifact':'docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:3189',
    'claim':'-123.98 dB median on both tones in both cases',
    'receipt':next(x for x in points if x['run']=='bcrf' and x['point']=='a' and x['tone']=='tone_9973')}
output.write_text(json.dumps(out,indent=2)+'\n')
print('PASS: publication hashes, quoted hashes, grade arithmetic, overlaps, traces, source bindings, readbacks and restore records')
print('Remaining attribution figure:',out['remaining_figure_discrepancy'])
