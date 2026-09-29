"""Analyze raw UART, controller and tapped-wire records without changing the bench."""
from pathlib import Path
import json,re,statistics,struct,sys,hashlib
from wire_summary import records,decode
name=sys.argv[1];root=Path("/tmp/a375")/name;packet=Path(__file__).resolve().parent.parent
load=lambda n:[json.loads(l) for l in (root/n).read_text().splitlines() if l.strip()]
events=load("events.jsonl");console=load("console.jsonl");ctrl=load("controller.jsonl")
def offset(role):
 a=[r for r in events if r['kind']=='clock' and r['role']==role];r=min(a,key=lambda x:x['t1']-x['t0'])
 return r['remote']-(r['t0']+r['t1'])/2,(r['t1']-r['t0'])/2
co,ce=offset('controller');to,te=offset('tap')
for r in ctrl:r['local_t']=r['t']-co
sts=[];words={}
for r in console:
 if r['cmd']=='milan_status':
  d={k:v for k,v in re.findall(r'(\w+)=([a-zA-Z0-9_]+)',r['raw'])};d['t']=r['t'];d['end']=r['end'];sts.append(d)
 else:
  m=re.search(r'^(0x[0-9a-f]+)  ((?:[0-9a-f]{2} ){3}[0-9a-f]{2})',r['raw'],re.M)
  if m:words.setdefault(m[1],[]).append((r['t'],int.from_bytes(bytes.fromhex(m[2]),'little')))
def changes(rows):
 out=[];prev=None
 for t,v in rows:
  if v!=prev:out.append([t,v]);prev=v
 return out
raw_wire=list(records(str(root/'tap.pcap')))
anchors=[(r['host_ns']-r['tap_ns'])/1e9 for r in raw_wire]
anchor=statistics.median(anchors)
wire=[]
for r in raw_wire:
 try:d=decode(r)
 except (IndexError,struct.error):continue
 d['t']=r['tap_ns']/1e9+anchor-to
 if d['kind']=='CRF':
  f=r['frame'];o=18 if f[12:14]==b'\x81\x00' else 14;p=f[o:];d['avtp']['mr']=(p[1]>>3)&1
  d['avtp']['valid']=(len(p)>=28 and p[0]==4 and p[1]&0xF0==0x80 and p[3]==1 and int.from_bytes(p[12:16],'big')==48000 and p[16:20]==bytes.fromhex('00080060') and d['vlan']==(3,2) and p[4:12].hex()==('0200000000010001' if r['port']==3 else '3cc0c60102034000'))
 wire.append(d)
wire.sort(key=lambda d:d['t'])
summary=dict(name=name,clock_offset_s={'controller':co,'tap':to},clock_half_rtt_s={'controller':ce,'tap':te},console_samples=len(sts),max_console_gap_s=max([b['t']-a['t'] for a,b in zip(sts,sts[1:])] or [0]),reset_epochs=sorted({v for t,v in words.get('0x90000720',[])}),mac_status=changes(words.get('0x90000110',[])),servo_states=changes([(t,v&7) for t,v in words.get('0x900008f8',[])]),gm=changes([(r['t'],r['GPTP_GM']) for r in sts]),health=changes([(r['t'],[r['SYNC'],r['ASCAPABLE'],r['TU']]) for r in sts]),crf_licence=changes(words.get('0x90000750',[])),counter_endpoints={},wire={})
for role,what in [('dut','counter-9-0'),('dut','counter-5-1'),('dut','counter-6-1'),('dut','counter-36-0'),('peer','counter-9-0'),('peer','counter-5-8'),('peer','counter-6-2'),('peer','counter-36-0')]:
 a=[r for r in ctrl if r.get('role')==role and r.get('what')==what and r['response'].get('status')=='SUCCESS']
 if a:
  first,last=a[0]['response']['counters'],a[-1]['response']['counters'];summary['counter_endpoints'][role+':'+what]=dict(first=first,last=last,delta={k:last[k]-v for k,v in first.items()})
summary['counter_transitions']={}
for role,what in [('dut','counter-9-0'),('dut','counter-5-1'),('dut','counter-6-1'),('dut','counter-36-0'),('peer','counter-5-8'),('peer','counter-6-2')]:
 a=[r for r in ctrl if r.get('role')==role and r.get('what')==what and r['response'].get('status')=='SUCCESS']
 summary['counter_transitions'][role+':'+what]=changes([(r['local_t'],{k:v for k,v in r['response']['counters'].items() if int(k)<4}) for r in a])
summary['carrier']=changes([(r['local_t'],r['value']) for r in ctrl if r.get('type')=='carrier'])
steps=[]
for a,b in zip(sts,sts[1:]):
 delta=(int(b['TAI_NS'],16)-int(a['TAI_NS'],16))/1e9-(b['t']-a['t'])
 if abs(delta)>.01:steps.append(dict(bracket=[a['t'],b['end']],phc_minus_wall_delta_s=delta))
summary['large_phc_discontinuities']=steps
for role,port in [('dut',3),('peer',2)]:
 a=[r for r in wire if r['kind']=='CRF' and r['port']==port];summary['wire'][role]=dict(pdus=len(a),valid_pdus=sum(bool(r['avtp']['valid']) for r in a),tu_counts={str(i):sum(r['avtp']['tu']==i for r in a) for i in [0,1]},mr=changes([(r['t'],r['avtp']['mr']) for r in a]),max_gap_s=max([b['t']-a['t'] for a,b in zip(a,a[1:])] or [0]))
summary['tap_anchor_spread_s']=[min(anchors)-anchor,max(anchors)-anchor]
summary['bindings_ok']=all(r['response'].get('conn_count')==1 for r in ctrl if r.get('what','').startswith('state-') and r['response'].get('status')==0)
summary['states_end']={role:[r['response'] for r in ctrl if r.get('role')==role and r.get('what','').startswith('state-') and r['response'].get('status')==0][-1:] for role in ['dut','peer']}
if name.startswith('cycle'):
 off=next(r['t'] for r in events if r['kind']=='power-command' and r['value']=='off');on=next(r['t'] for r in events if r['kind']=='power-command' and r['value']=='on');summary.update(off=off,on=on,off_hold_s=on-off)
 gm=[r for r in wire if r['t']>on and r['port']==2 and r['kind'] in ('gPTP Announce','gPTP Sync')]
 first=gm[0]['t'] if gm else None;summary['first_gm']=first
 summary['first_gm_kind']=gm[0]['kind'] if gm else None
 post=[r for r in wire if r['t']>on]
 summary['first_wire_return']=post[0]['t'] if post else None
 summary['last_wire_before_gap']=max((r['t'] for r in wire if off<r['t']<on),default=None)
 healthy=[r for r in sts if r['t']>on and r['SYNC']=='1' and r['ASCAPABLE']=='1' and r['TU']=='0' and r['GPTP_GM']=='3cc0c6fffefe0210']
 summary['gptp_recovered_at']=healthy[0]['end'] if healthy else None
 summary['gptp_recovery_s']=healthy[0]['end']-first if healthy and first else None
 summary['last_health']=sts[-1] if sts else None
 for role,port in [('dut',3),('peer',2)]:
  a=[r for r in wire if r['t']>on and r['kind']=='CRF' and r['port']==port and r['avtp']['valid']]
  summary['wire'][role]['first_after_on']=a[0]['t'] if a else None
  summary['wire'][role]['post_pdus']=len(a)
  summary['wire'][role]['post_tu1']=sum(r['avtp']['tu'] for r in a)
  summary['wire'][role]['first_valid_after_wire_return_s']=a[0]['t']-summary['first_wire_return'] if a and summary['first_wire_return'] else None
  summary['wire'][role]['post_last']=a[-1]['t'] if a else None
  summary['wire'][role]['post_max_gap_s']=max([b['t']-a['t'] for a,b in zip(a,a[1:])] or [0])
 summary['media_locked_at']={}
 for role,what in [('dut','counter-5-1'),('peer','counter-5-8')]:
  a=[r for r in ctrl if r.get('role')==role and r.get('what')==what and r['local_t']>on and r['response'].get('status')=='SUCCESS' and r['response']['counters']['0']==r['response']['counters']['1']+1]
  summary['media_locked_at'][role]=a[0]['local_t'] if a else None
 servo=[t for t,v in words.get('0x900008f8',[]) if t>on and v&7==4];summary['servo_locked_at']=servo[0] if servo else None
 summary['steady_recovered']=bool(sts[-1]['SYNC']=='1' and sts[-1]['ASCAPABLE']=='1' and sts[-1]['TU']=='0' and (words['0x900008f8'][-1][1]&7)==4 and healthy and all(summary['media_locked_at'].values()) and servo and all(summary['wire'][role]['post_pdus']>100 for role in ['dut','peer']) and summary['bindings_ok'] and all((summary['wire'][role]['post_last'] or 0)>sts[-1]['t']-1 for role in ['dut','peer']) and all(summary['counter_endpoints'][key]['last']['0']==summary['counter_endpoints'][key]['last']['1']+1 for key in ['dut:counter-5-1','peer:counter-5-8']))
 summary['switch_frames_absent_off']=not any(r['port']==2 and r['kind'].startswith('gPTP') and off+5<r['t']<on for r in wire)
 summary['proof_dut_alive']=summary['reset_epochs']==[1] and summary['max_console_gap_s']<1
 summary['post_media_restarts']={role:summary['counter_endpoints'][role+':counter-6-'+('1' if role=='dut' else '2')]['delta']['0'] for role in ['dut','peer']}
 summary['peer_available_index']=changes([(r['local_t'],r['available_index']) for r in ctrl if r.get('type')=='adp' and r.get('entity_id')=='3cc0c60102030000'])
 summary['mr_observation_limit']='Only levels carried by captured PDUs are observable; a gap cannot prove the number of unseen toggles.'
dest=packet/name;dest.mkdir(exist_ok=True);(dest/'analysis.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
manifest=[]
for f in root.iterdir():
 if f.is_file():manifest.append(dict(path=str(f),size=f.stat().st_size,sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
(dest/'raw-artifacts.json').write_text(json.dumps(manifest,indent=2)+'\n')
