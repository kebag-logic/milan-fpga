#!/usr/bin/env python3
"""Independent reductions of public receipts; arguments: evidence-root output-root repository."""
import csv
import hashlib
import json
import pathlib
import statistics
import sys
from decimal import Decimal, ROUND_HALF_UP

evidence,out=map(lambda x:pathlib.Path(x).resolve(),sys.argv[1:3])
p=evidence/'author-r9'
def load(rel):return json.loads((p/rel).read_text())
def events(run):return [json.loads(x) for x in (p/f'runs/{run}/events.jsonl').read_text().splitlines()]
def rounded(v,n=2):return str(Decimal(str(v)).quantize(Decimal(10)**-n,rounding=ROUND_HALF_UP))
manifest=json.loads((evidence/'MANIFEST.json').read_text())
checked=[];bad=[]
for m in manifest:
    rel=m['file']
    if not rel.startswith('author-') or pathlib.Path(rel).name.startswith(('HANDOFF','PR-BODY','REVIEW-READY','STOP')):
        continue
    got=hashlib.sha256((evidence/rel).read_bytes()).hexdigest()
    checked.append(rel)
    if got!=m['published_sha256']:bad.append(rel)
assert not bad,bad
grades={}
for run in ['b0-2','bcrf','baaf']:
    d=load(f'summary/{run}/c-b9-grade.json');b=d['blocks'];free=[x for x in b if x['events']==0]
    med=[statistics.median(x[f'ch{c}']['thdn_db'] for x in free) for c in (0,1)]
    floor=[x for x in free if all(x[f'ch{c}']['thdn_db']<=med[c]+3 for c in (0,1))]
    degraded=[x['block'] for x in free if x not in floor]
    assert degraded==d['summary']['degraded_event_free_blocks']
    assert len(floor)==d['summary']['blocks_at_floor']
    sums={}
    for c in (0,1):
        v=rounded(statistics.median(x[f'ch{c}']['thdn_db'] for x in floor))
        assert v==rounded(d['summary'][f'ch{c}_floor']['thdn_db_median'])
        sums[f'ch{c}']=dict(floor_median_db=v,all_median_db=rounded(med[c]),
                           worst_db=rounded(max(x[f'ch{c}']['thdn_db'] for x in b)))
    grades[run]=dict(blocks=len(b),floor=len(floor),degraded=degraded,tones=sums,
                     events=len(d['events']),phase_net_frames=d['phase_net_frames'])
    if run=='b0-2':
        r=load('r2/b0-2-receipt.json');assert r['degraded_inside']==23 if 'degraded_inside' in r else r['overlap']['degraded_inside']==23
        assert sum(x<34 for x in degraded)==23 and sum(x>=34 for x in degraded)==108
        assert 45 not in degraded

positive={}
for run in ['pts2','b0-2','bcrf','baaf']:
    d=load(f'summary/{run}/d-extcap-pair.json')
    tones=[(c,k,v) for c,row in enumerate(d['rows']) for k,v in row.items() if k.startswith('tone_') and v]
    per=[v['per_block'] for c,k,v in tones if k==('tone_997' if c==0 else 'tone_9973')]
    assert len(per)==2
    level_blocks=[i for i in range(len(per[0])) if all(abs(b[i]['level_dbfs']+1)<0.1 for b in per)]
    # Bound playback by its first and last full-level blocks; a repeated
    # sample inside playback can itself spoil the high-tone amplitude fit.
    whole=list(range(min(level_blocks),max(level_blocks)+1))
    at_floor=[i for i in whole if all(abs(b[i]['thdn_db']-statistics.median(x['thdn_db'] for x in b if abs(x['level_dbfs']+1)<0.1))<0.01 for b in per)]
    positive[run]=dict(blocks=len(per[0]),whole_playback=len(whole),at_floor=len(at_floor),
                       preplayback=[i for i in range(len(per[0])) if per[0][i]['level_dbfs']<-100])
    assert positive[run]['preplayback']==[0,1]
    assert (len(whole),len(at_floor))==((13,11) if run=='pts2' else (303,303))

polls={};clocks={};restores={}
for run in ['loop1','loop2','pts1','pts2','b0','b0-2','pts3','bcrf','baaf']:
    ev=events(run);fin=next(x for x in ev if x['kind']=='final')
    assert fin['equal_to_found'] and not fin['differ']
    restores[run]=dict(equal_to_found=True,differences=[],dut_source=fin.get('clk-dut'),peer_source=fin.get('clk-peer'))
    if run not in ['bcrf','baaf']:continue
    sets=[{k:x[k] for k in ['who','src','readback','status']} for x in ev if x['kind']=='set-clock']
    assert all(x['status']=='SUCCESS' and x['src']==x['readback'] for x in sets)
    assert [(x['who'],x['src']) for x in sets]==[('peer',0),('dut',1 if run=='bcrf' else 2),('dut',0),('peer',1)]
    clocks[run]=sets
    r=load(f'r2/{run}-poll-receipt.json')
    rows=list(csv.DictReader((p/f'r2/{run}-poll-trace.tsv').open(),delimiter='\t'))
    start=r['marks_after_set_s']['window-start'];end=r['marks_after_set_s']['window-end']
    selected=[x for x in rows if float(x['start_after_set_s'])>=start and float(x['start_after_set_s'])+float(x['length_ms'])/1000<=end]
    assert len(selected)==596 and all(int(x['0x8f8'],16)&7==4 for x in selected)
    trim=[int(x['0x8f8'][:4],16) for x in selected];trim=[(v-65536 if v>=32768 else v)/16 for v in trim]
    assert [min(trim),max(trim)]==[-6.125,-6.0]
    lock=next(i for i,x in enumerate(rows) if int(x['0x8f8'],16)&7==4)
    bracket=[float(rows[lock-1]['start_after_set_s']),round(float(rows[lock]['start_after_set_s'])+float(rows[lock]['length_ms'])/1000,3)]
    assert bracket==([2.585,3.161] if run=='bcrf' else [6.602,7.180])
    changes=[(a,b) for a,b in zip(rows,rows[1:]) if a['0x8d4']!=b['0x8d4']]
    steps=[dict(polls=[int(a['n']),int(b['n'])],states=[int(a['0x8f8'],16)&7,int(b['0x8f8'],16)&7],
                dups=[int(a['0x8d4'],16)&65535,int(b['0x8d4'],16)&65535]) for a,b in changes]
    assert len(steps)==(6 if run=='bcrf' else 7)
    assert all(x['states'] in ([0,0],[3,3]) for x in steps)
    assert all(int(x['0x8d8'],16)==0 for x in rows)
    polls[run]=dict(window_polls=len(selected),lock_bracket_s=bracket,trim_ppm=[min(trim),max(trim)],slip_steps=steps,
                    raw_sha256=r['raw']['sha256'],trace_sha256=hashlib.sha256((p/f'r2/{run}-poll-trace.tsv').read_bytes()).hexdigest())

a=load('summary/loop2/acmp-peer-tap.json')['acmp']
first=lambda kind:next(Decimal(str(x['t'])) for x in a if x['msg']==kind)
probes=[Decimal(str(x['t'])) for x in a if x['msg']=='CONNECT_TX_COMMAND']
assert len(probes)==2 and not any(x['msg']=='CONNECT_TX_RESPONSE' for x in a)
timing=dict(unbind_s=str(first('DISCONNECT_RX_COMMAND')),bind_s=str(first('CONNECT_RX_COMMAND')),
            probe_s=[str(x) for x in probes],after_unbind_ms=str((probes[0]-first('DISCONNECT_RX_COMMAND'))*1000),
            after_bind_ms=str((probes[0]-first('CONNECT_RX_COMMAND'))*1000),
            repeated_after_ms=str((probes[1]-probes[0])*1000))
volatile={'t','seq','rtt_ms','sequence_id','t_tx','t_rx'}
def strip(x):
    if isinstance(x,dict):return {k:strip(v) for k,v in x.items() if k not in volatile}
    if isinstance(x,list):return [strip(v) for v in x]
    return x
census={}
for name in ['start','endc']:
    rows=[json.loads(line) for line in (p/f'restore/census-{name}.jsonl').read_text().splitlines()]
    census[name]=[strip(x) for x in rows if x.get('type')!='start']
assert len(census['start'])==len(census['endc'])==45
pairs=list(zip(census['start'],census['endc']))
differences=[dict(index=i,first=a,last=b) for i,(a,b) in enumerate(pairs) if a!=b]
assert len(differences)==1 and differences[0]['first']['cmd']=='GET_AVB_INFO'
assert all(x.get('status') in (0,'SUCCESS') for rows in census.values() for x in rows)
restore_census=dict(first='restore/census-start.jsonl',last='restore/census-endc.jsonl',
                    reads=45,equal=44,differences=differences,
                    ignored_exchange_fields=sorted(volatile),all_reads_successful=True)
raw_hashes=[r['sha256'] for r in load('r2/source-receipt.json')['reads'].values()]
raw_hashes += [load(f'r2/{run}-poll-receipt.json')['raw']['sha256'] for run in ['bcrf','baaf']]
page=(pathlib.Path(sys.argv[3])/'docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md').read_text()
assert all(x in page for x in raw_hashes)
result=dict(restore_census=restore_census,raw_hash_bindings=dict(count=len(raw_hashes),all_in_findings_hash_tables=True,raw_material_republished=False,sha256=raw_hashes),manifest_checked=len(checked),manifest_mismatches=bad,grades=grades,positive_controls=positive,
            polls=polls,clock_sets=clocks,restores=restores,probe_timing=timing,
            source_comparisons=load('r2/source-receipt.json')['compare'])
(out/'receipts/independent-evidence-audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(manifest_checked=len(checked),independent_audit='PASS',probe_timing=timing)))
