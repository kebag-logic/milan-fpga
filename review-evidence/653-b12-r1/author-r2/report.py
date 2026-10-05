"""Recompute final per-cycle observations from retained capture bytes."""
import collections,csv,json,sys,os
from pathlib import Path
from wire import analyze
RAW=Path('/tmp/653-b12/raw');OUT=Path(sys.argv[1]);DUT='020000fffe000001';PEER=os.environ['PEER_EID'];CTL=os.environ['CONTROLLER_EID']
rows=[]
for f in sorted(RAW.glob('*-result.json')):
 d=json.loads(f.read_text());p=d['plan'];ev=d['events'];listener=DUT if p['direction']=='A' else PEER;who='dut' if p['direction']=='A' else 'peer';idx=p['li']
 paths=[(a['path'],not a['path'].endswith('observer.pcap')) for a in d['artifacts']]
 g=analyze(paths,listener,idx,CTL);w=g['wire'];errors=collections.Counter();updates=[]
 for e in ev:
  if e.get('who')==who and e.get('idx')==idx:
   if e['ev']=='hive_rule':errors.update(e['increments'])
   if e['ev']=='si_counters':updates.append(e)
 bind=next((e for e in ev if e['ev']=='bind'),{});unbind=next((e for e in ev if e['ev']=='unbind'),{})
 polls=[e for e in ev if e['ev']=='poll'];post=next((e for e in reversed(polls) if e['phase']=='post-unbind'),{})
 phase=next((e for e in ev if e['ev']=='phase_target'),{})
 row=dict(cycle=p['tag'],direction=p['direction'],kind='AAF' if p['ti']==0 else 'CRF',requested_hold_ms=p['hold'],phase=p.get('phase','exact'),result=d['result'],status=w.get('status') if w else None,order=w.get('order') if w else 'NO_MATCH',response_unlock_us=w.get('response_unlock_us') if w else None,error_increments=dict(errors),library_state='unobserved',sequence_max=max((e['counters'].get('SEQ',0) for e in polls if e['phase']!='pre-bind'),default=None),interruption_max=max((e['counters'].get('SI',0) for e in polls if e['phase']!='pre-bind'),default=None),post_counters=post.get('counters'),poll_count=len(polls),artifacts=g['artifacts'],stream_frames=sum(x['count'] for x in g['streams']),stream_gaps=sum(x['gaps'] for x in g['streams']),first_sequences=[dict(port=x['port'],sub=x['sub'],sequence=[v['seq'] for v in x['first']]) for x in g['streams']],nonmonotonic=g['nonmonotonic'],command_time_us=unbind.get('t_cmd'))
 if w:
  row['capture_point']='controller' if w['capture'].endswith('observer.pcap') else 'DUT link'
  row['selected_capture']=w['capture'];row['command_response_us']=w['command_response_us'];row['unlock_frame']=(w.get('unlock') or {}).get('i');row['response_frame']=w['response']['i'];row['command_frame']=w['command']['i'];row['earlier_unlock_notifications']=len(w['earlier_increases'])
  same=[x for x in g['controls'] if x['capture']==w['capture']]
  bs=[x for x in same if x['kind']=='acmp' and x['mt']==7 and x['listener']==listener and x['luid']==idx and x['ctl']==CTL]
  if bs:row['actual_hold_ms']=(w['command']['tns']-bs[0]['tns'])/1e6
  prior=[x for x in w['pushes'] if x['i']<w['command']['i']]
  row['last_push_to_command_ms']=(w['command']['tns']-prior[-1]['tns'])/1e6 if prior else None
  mu=(w.get('unlock') or {}).get('counters',{}).get('MU')
  u=next((x for x in updates if x['t']>=unbind.get('t_cmd',0) and x['counters'].get('MU')==mu),None)
  if u:row['library_state']=u['lib_conn'];row['library_unlock_t_us']=u['t']
 rows.append(row)
for start in range(0,len(rows),25):
 (OUT/f'cycles-{start//25:02d}.json').write_text(json.dumps(rows[start:start+25],indent=1)+'\n')
columns=['cycle','direction','kind','requested_hold_ms','phase','actual_hold_ms','status','order','response_unlock_us','library_state','sequence_max','interruption_max','stream_frames','stream_gaps','capture_point','last_push_to_command_ms','error_increments']
with (OUT/'cycles.csv').open('w') as f:
 wr=csv.DictWriter(f,columns,extrasaction='ignore');wr.writeheader();wr.writerows(rows)
print('cycles',len(rows),'orders',dict(collections.Counter(r['order'] for r in rows)),'errors',dict(sum((collections.Counter(r['error_increments']) for r in rows),collections.Counter())))
