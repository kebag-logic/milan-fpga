"""Small receipts; original traces and large captures stay in scratch storage."""
import collections,csv,datetime,hashlib,json,os,sys,io
from pathlib import Path
from wire import analyze,records
RAW=Path('/tmp/653-b12/raw');OUT=Path(sys.argv[1]);DUT='020000fffe000001';PEER=os.environ['PEER_EID'];CTL='<controller-host-id>0c12'
def save(name,txt):
 assert len(txt.encode())<=200000,(name,len(txt.encode()))
 (OUT/name).write_text(txt)
receipts=[];poll_rows=[];rule_rows=[];builds=[];warnings=[]
for f in sorted(RAW.glob('*-result.json')):
 d=json.loads(f.read_text());p=d['plan'];ev=d['events'];who='dut' if p['direction']=='A' else 'peer';listener=DUT if who=='dut' else PEER
 # Results keep all original bytes. Final wire grading was exported by report.py.
 w=d['wire'];paths=[(a['path'],not a['path'].endswith('observer.pcap')) for a in d['artifacts']]
 if not w or not w.get('unlock'):w=analyze(paths,listener,p['li'],CTL)['wire']
 def control(r):
  if not r:return None
  return {k:r[k] for k in ('i','tns','port','status','raw')}
 begin=next(e for e in ev if e['ev']=='bind')['t_cmd']
 selected=[e for e in ev if e['ev']=='poll']
 for e in selected:
  poll_rows.append(dict(cycle=p['tag'],phase=e['phase'],utc=datetime.datetime.fromtimestamp(e['t_rsp']/1e6,datetime.timezone.utc).isoformat(),send_us=e['t_cmd'],response_us=e['t_rsp'],since_bind_command_ms=(e['t_rsp']-begin)/1000,status=e['status'],**e['counters']))
 for e in ev:
  if e['ev']=='hive_rule' and e.get('who')==who and e.get('idx')==p['li'] and e['increments']:
   rule_rows.append(dict(cycle=p['tag'],**e))
 tap_commands=[x for x in d['controls'] if x['kind']=='acmp' and x['mt']==6 and x['listener']==listener and x['luid']==p['li'] and not x['capture'].endswith('observer.pcap')]
 anchor=min((x['tns'] for x in tap_commands),default=None);first=[]
 for path,tap in paths:
  if not tap or not path.endswith('vlan.pcap'):continue
  for r in records(path,tap):
   if r['kind']=='stream' and (anchor is None or r['tns']>=anchor):
    first.append({k:r[k] for k in ('i','tns','port','sub','seq')})
    if len(first)==12:break
 receipts.append(dict(cycle=p['tag'],capture=w['capture'],command=control(w['command']),response=control(w['response']),unlock=control(w.get('unlock')),bind_command_tap_ns=anchor,first_twelve_pdus=first,format_read=next(e for e in ev if e['ev']=='formats')))
for start in range(0,len(receipts),25):save(f'wire-receipts-{start//25:02d}.json',json.dumps(receipts[start:start+25],indent=1)+'\n')
columns=['cycle','phase','utc','send_us','response_us','since_bind_command_ms','status','ML','MU','SI','SEQ','MRST','TU','TSV','TSNV','UF','LATE','EARLY','FRX']
# Split first-PDU reads and sustained two-second polls into compact tables.
for name,select in (('short-polls',lambda r:'600s' not in r['cycle']),('long-polls',lambda r:'600s' in r['cycle'])):
 f=io.StringIO();wr=csv.DictWriter(f,columns);wr.writeheader();wr.writerows(r for r in poll_rows if select(r));save(name+'.csv',f.getvalue())
save('rule-increments.json',json.dumps(rule_rows,indent=2)+'\n')
for p in RAW.glob('*-probe.jsonl'):
 for line in p.read_text().splitlines():
  e=json.loads(line)
  if e['ev'] in ('online','compatibility','compat_changed','diagnostics','query_error','transport_error','unsol_loss','aecp_timeout','aecp_unexpected'):
   # Exclude entity identifiers and interface names from these role-labelled receipts.
   warnings.append(dict(session=p.stem,**e))
  if e['ev']=='start':builds.append(dict(session=p.stem,protocol=e['lib'],controller=e['ctl_lib']))
save('library-observations.json',json.dumps(dict(builds=builds,events=warnings),indent=1)+'\n')
print('wire receipts',len(receipts),'polls',len(poll_rows),'rule increments',len(rule_rows))
