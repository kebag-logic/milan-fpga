#!/usr/bin/env python3
"""Independent receipt arithmetic and publication audit. Takes repo, author packet, review directory."""
import collections,csv,hashlib,json,pathlib,re,statistics,subprocess,sys
from decimal import Decimal
repo,packet,out=map(lambda s:pathlib.Path(s).resolve(),sys.argv[1:4])
def load(f):return json.loads((packet/f).read_text())
def jl(f):return [json.loads(x) for x in (packet/f).read_text().splitlines() if x.startswith('{')]
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*args):return subprocess.check_output(['git','-C',str(repo),*args])
result={}
manifest=json.loads((packet.parent/'MANIFEST.json').read_text());entries=[x for x in manifest if x['file'].startswith('author-r5/')]
for e in entries:
 b=(packet/e['file'].removeprefix('author-r5/')).read_bytes()
 assert sha(b)==e['published_sha256'],e['file']
 assert (e['original_sha256']!=e['published_sha256'])==e['path_redacted']
result['publication']={'evidence_commit':'a73ce5c42ee97fb53b272a51b5f41a55afba5fa5','files_verified':len(entries),'path_redacted':sum(e['path_redacted'] for e in entries),'check_sha256':sha((packet/'tools/check_b16_figures.py').read_bytes())}
b=git('show','b84584e4ccb069248909f0fdeb7f8b72a1c41ae4:review-evidence/629-b16-r1/MANIFEST.json');m=json.loads(b)
assert len(m)==1680 and sha(b)=='8d417d54b13a264484bfcb0b69f8a643e5cd3bf2819294cea201242a2f67f034'
result['historical_manifest']={'entries':len(m),'sha256':sha(b),'redacted_author_files':sum(e['path_redacted'] for e in m if e['file'].startswith('author-'))}
page=(repo/'docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md').read_text().split('## Dev 5603c353, 2026-10-12: lane B16',1)[1]
rows=re.findall(r'^\| `([^`]+)`[^|]*\| ([\d,]+) \| `([0-9a-f]{64})` \|$',page,re.M)
for f,size,h in rows:
 b=(packet/f).read_bytes();assert len(b)==int(size.replace(',','')) and sha(b)==h,f
result['current_page_packet_hash_rows']=len(rows)
for name in ['rows','coverage']:
 assert (out/f'receipts/figures-{name}.tsv').read_bytes()==(packet/f'r5/figures-{name}.tsv').read_bytes()
result['figure_outputs_byte_equal']=True
# Recompute the floor independently from all per-block values, not from the rounded summaries.
for run in ['b0-2','bcrf','baaf']:
 g=load(f'summary/{run}/c-b9-grade.json');blocks=g['blocks'];free=[x for x in blocks if x['events']==0]
 med=[statistics.median(x[f'ch{c}']['thdn_db'] for x in free) for c in (0,1)]
 floor=[x for x in free if all(x[f'ch{c}']['thdn_db']<=med[c]+3 for c in (0,1))]
 degraded=[x['block'] for x in free if x not in floor]
 assert len(floor)==g['summary']['blocks_at_floor'] and degraded==g['summary']['degraded_event_free_blocks']
 vals=[round(statistics.median(x[f'ch{c}']['thdn_db'] for x in floor),2) for c in (0,1)]
 assert vals==[g['summary'][f'ch{c}_floor']['thdn_db_median'] for c in (0,1)]
 align=[load(f'summary/{run}/align-{k}-c.json') for k in ('a','b')]
 overlap=min(x['covered_recording_frames'][1] for x in align)
 result[run]={'blocks':len(blocks),'floor_blocks':len(floor),'floor_medians_db':vals,'degraded_blocks':degraded,'degraded_inside':sum((x+1)*48000<=overlap for x in degraded),'degraded_beyond':sum(x*48000>=overlap for x in degraded),'alignment_covered_frames':[x['covered_recording_frames'][1] for x in align],'events':len(g['events'])}
 if run=='b0-2':
  assert vals==[-123.98,-123.95] and result[run]['degraded_inside']==23 and result[run]['degraded_beyond']==108
# The positive control excludes the two silent blocks and the playback-start block.
for run in ['pts2','b0-2','bcrf','baaf']:
 g=load(f'summary/{run}/d-extcap-pair.json');tones=[row[k] for row in g['rows'] for k in ['tone_997','tone_9973'] if k in row]
 counts=[]
 for t in tones:
  bl=t['per_block'];assert all(x['level_dbfs']<-400 for x in bl[:2])
  whole=bl[3:];floor=sum(x['thdn_db']<-145 for x in whole);counts.append([len(whole),floor])
 assert all(x==([13,11] if run=='pts2' else [303,303]) for x in counts)
 result.setdefault(run,{})['positive_control_whole_and_floor']=counts
# Clock sets, matching format readbacks, and full per-run restore.
run_results={}
for run in ['loop1','loop2','pts1','pts2','b0','b0-2','pts3','bcrf','baaf']:
 ev=jl(f'runs/{run}/events.jsonl');found=next(x for x in ev if x['kind']=='as-found');end=next(x for x in ev if x['kind']=='final')
 checked=[k for k in found if k not in ('t','kind')]
 assert all(found[k]==end[k] for k in checked),run
 sets=[{k:e[k] for k in ['who','src','status','readback']} for e in ev if e['kind']=='set-clock']
 for e in sets:assert e['status']=='SUCCESS' and e['src']==e['readback']
 for e in ev:
  if e['kind']=='format-check':
   assert e['ok']
   if 'listener_after' in e: assert e['listener_after']==e['talker_fmt']
   else: assert e['set'] is None and e['listener_fmt']==e['talker_fmt']
 if run in ['bcrf','baaf']:
  assert [(e['who'],e['src']) for e in sets]==[('peer',0),('dut',1 if run=='bcrf' else 2),('dut',0),('peer',1)]
 else: assert not sets
 run_results[run]={'restore_fields_equal':len(checked),'clock_sets':sets}
result['run_restore']=run_results
controller=[]
for run in ['bcrf','baaf']:
 rows=[e['line'] for e in jl(f'runs/{run}/ctl.jsonl') if 'line' in e]
 for i,e in enumerate(rows):
  if e.get('cmd')!='SET_CLOCK_SOURCE':continue
  follow=next(x for x in rows[i+1:] if x.get('cmd')=='GET_CLOCK_SOURCE' and x.get('role')==e['role'])
  sent=int(e['payload'][8:12],16);got=int(follow['payload'][8:12],16)
  assert e['status']==follow['status']=='SUCCESS' and sent==got
  controller.append({'run':run,'role':e['role'],'set':sent,'get':got,'status':'SUCCESS'})
assert len(controller)==8
result['controller_clock_readbacks']=controller
# Independent register decoding from public reduced traces.
for run in ['bcrf','baaf']:
 r=load(f'r2/{run}-poll-receipt.json');trace=list(csv.DictReader((packet/f'r2/{run}-poll-trace.tsv').open(),delimiter='\t'))
 def state(x):return int(x['0x8f8'],16)&7
 k=next(i for i,x in enumerate(trace) if Decimal(x['start_after_set_s'])>=0 and state(x)==4)
 start=Decimal(trace[k-1]['start_after_set_s']);end=Decimal(trace[k]['start_after_set_s'])+Decimal(trace[k]['length_ms'])/1000
 assert state(trace[k-1])==3
 marks=r['marks_after_set_s'];w=[x for x in trace if float(x['start_after_set_s'])>=marks['window-start'] and float(x['start_after_set_s'])+float(x['length_ms'])/1000<=marks['window-end']]
 assert len(w)==596 and all(state(x)==4 for x in w)
 def signed(x,bits):return x-(1<<bits) if x&(1<<(bits-1)) else x
 trim=[signed(int(x['0x8f8'],16)>>16,16)/16 for x in w]
 crf=[signed(int(x['0x748'],16),32)/512 for x in w]
 aaf=[signed(int(x['0x8e4'],16),32)/512 for x in w]
 steps=[]
 for prev,cur in zip(trace,trace[1:]):
  if prev['0x8d4']!=cur['0x8d4']:
   steps.append({'polls':[int(prev['n']),int(cur['n'])],'states':[state(prev),state(cur)],'start_s':float(prev['start_after_set_s']),'end_s':round(float(cur['start_after_set_s'])+float(cur['length_ms'])/1000,4),'dups':[int(prev['0x8d4'],16)&65535,int(cur['0x8d4'],16)&65535]})
 assert [x['polls'] for x in steps]==[x['polls'] for x in r['slip_lb_steps']]
 assert all(x['states'] in ([0,0],[3,3]) for x in steps)
 assert sum(x['states']==[0,0] for x in steps)==5
 assert all(int(x['0x8d8'],16)==0 for x in trace)
 for key,vals in [('trim_ppm',trim),('crf_rate_ppm',crf)]:assert [min(vals),max(vals)]==r['spans']['window-start..window-end'][key]
 ev=jl(f'runs/{run}/events.jsonl');raw=next(e for e in ev if e['kind']=='raw' and e['file']=='poll-run.jsonl')
 assert raw['sha256']==r['raw']['sha256'] and raw['bytes']==r['raw']['bytes']
 assert abs(float(end)-r['locked']['recomputed_s'][1])<=0.0006
 result[run]['polls']={'lock_bracket_s':[float(start),r['locked']['recomputed_s'][1]],'upper_end_recomposed_from_rounded_trace_s':float(end),'window_count':len(w),'trim_range_ppm':[min(trim),max(trim)],'crf_range_ppm':[min(crf),max(crf)],'aaf_range_ppm':[min(aaf),max(aaf)] if run=='baaf' else None,'servo_low_counts':dict(collections.Counter(f"{int(x['0x8f8'],16)&65535:04x}" for x in w)),'slip_steps':steps,'raw_sha256':raw['sha256']}
 if run=='baaf':assert all(int(x['0x8e0'],16)==0x1e0007 for x in w)
# Census: ignore only per-exchange timestamps and sequence identifiers.
volatile={'t','seq','rtt_ms','sequence_id','t_tx','t_rx'}
def strip(x):
 if isinstance(x,dict):return {k:strip(v) for k,v in x.items() if k not in volatile}
 if isinstance(x,list):return [strip(v) for v in x]
 return x
for suffix in ['','b','c','start_to_end']:
 start_suffix='' if suffix=='start_to_end' else suffix;end_suffix='c' if suffix=='start_to_end' else suffix
 a=[strip(x) for x in jl(f'restore/census-start{start_suffix}.jsonl') if x.get('type')!='start'];b=[strip(x) for x in jl(f'restore/census-end{end_suffix}.jsonl') if x.get('type')!='start']
 dif=[(x,y) for x,y in zip(a,b) if x!=y]
 assert len(a)==len(b)==45 and len(dif)==1 and dif[0][0]['cmd']=='GET_AVB_INFO'
 result[f'census_{suffix or "initial"}']={'reads':45,'equal':44,'difference':'live propagation-delay read'}
source=load('r2/source-receipt.json');rawfiles=load('RAW-ARTIFACTS.json')['files'];hashes={x['sha256'] for x in rawfiles}
assert all(x['sha256'] in hashes for x in source['reads'].values())
assert [x['both'] for x in source['compare']]==[2262,1255,618,668]
result['source_comparisons']=[{k:x[k] for k in ['first','second','entries','both','differ','differing']} for x in source['compare']]
a=load('summary/loop2/acmp-peer-tap.json')['acmp'];probes=[x for x in a if x['msg']=='CONNECT_TX_COMMAND' and x.get('talker')==x.get('listener')=='<peer-eid>']
assert len(probes)==2 and round(1000*(probes[1]['t']-probes[0]['t']))==200
assert not [x for x in a if x['msg']=='CONNECT_TX_RESPONSE' and x.get('talker')=='<peer-eid>']
result['loopback']={'unanswered_probes':2,'spacing_ms':round(1000*(probes[1]['t']-probes[0]['t']),3)}
g=load('gates/r5/results.json');assert g['head']=='3619019350936d5af851933df0b5444ef8387e69' and all(x['rc']==0 for x in g['gates'])
result['author_source_gates']={'head':g['head'],'gates':[{k:x[k] for k in ('gate','rc')} for x in g['gates']],'manager_source_banks':'NOT RUN'}
(out/'receipts/receipt-audit.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS: publication hashes, figure outputs, block arithmetic, positive controls, restores, register traces, source comparisons and author receipts')
