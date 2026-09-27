"""Decode captured MSRP vectors and independently recompute wire timing."""
from pathlib import Path
import collections,json,struct,sys
from wire_summary import records
packet=Path(__file__).resolve().parent.parent
name=sys.argv[1];dest=packet/name
result=json.loads((dest/'result.json').read_text())
raw=list(records('/tmp/a386/'+name+'/tap.pcap'))
events=[];acmp=[];avtp=[];pdus=[];malformed=[]
EV=['New','JoinIn','In','JoinMt','Mt','Lv'];TYPES={1:'TalkerAdvertise',2:'TalkerFailed',3:'Listener',4:'Domain'}
def msrp(p,rec,sender):
 assert p and p[0]==0,'MSRP version'
 o=1
 while o+2<=len(p) and p[o:o+2]!=bytes(2):
  assert o+4<=len(p),'message header'
  typ,alen=p[o:o+2];length=int.from_bytes(p[o+2:o+4],'big');o+=4;end=o+length
  assert typ in TYPES and alen=={1:25,2:34,3:8,4:4}[typ] and end<=len(p),'message shape'
  while o+2<=end and p[o:o+2]!=bytes(2):
   h=int.from_bytes(p[o:o+2],'big');o+=2;n=h&8191;la=h>>13
   assert la in (0,1) and o+alen<=end,'vector header'
   fv=p[o:o+alen];o+=alen
   ne=(n+2)//3;nf=(n+3)//4 if typ==3 else 0
   assert o+ne+nf<=end,'packed events length'
   ep=p[o:o+ne];fp=p[o+ne:o+ne+nf];o+=ne+nf
   base=dict(ns=rec['tap_ns'],sender=sender,type=TYPES[typ],la=bool(la),values=n,first_value=fv.hex())
   if la:events.append(dict(base,event='LeaveAll',stream_id=None,listener=None))
   for k in range(n):
    v=ep[k//3];assert v<216,'three-packed event'
    ev=(v//(36,6,1)[k%3])%6
    sid=(fv[:6]+((int.from_bytes(fv[6:8],'big')+k)&65535).to_bytes(2,'big')).hex() if typ in (1,2,3) else None
    listener=(fp[k//4]//(64,16,4,1)[k%4])%4 if typ==3 else None
    events.append(dict(base,event=EV[ev],stream_id=sid,listener=listener))
  assert o+2==end and p[o:o+2]==bytes(2),'attribute endmark'
  o=end
 assert o+2<=len(p) and p[o:o+2]==bytes(2),'PDU endmark'
for rec in raw:
 fr=rec['frame'];et=int.from_bytes(fr[12:14],'big');off=14;vlan=None
 if et==0x8100:
  tci=int.from_bytes(fr[14:16],'big');vlan=(tci>>13,tci&4095);et=int.from_bytes(fr[16:18],'big');off=18
 p=fr[off:];sender='DUT' if rec['port']==3 else 'bridge'
 if et==0x22ea:
  pdus.append(dict(ns=rec['tap_ns'],sender=sender,source=fr[6:12].hex()))
  try:msrp(p,rec,sender)
  except (AssertionError,IndexError) as e:malformed.append(dict(ns=rec['tap_ns'],error=str(e)))
 if et==0x22f0 and len(p)>=12:
  if p[0]==0xfc and len(p)>=56:
   acmp.append(dict(ns=rec['tap_ns'],mt=p[1]&15,status=p[2]>>3,seq=int.from_bytes(p[48:50],'big'),controller=p[12:20].hex(),sender=sender))
  if p[0]==4:
   valid=(len(p)>=28 and p[1]&0xf0==0x80 and p[3]==1 and int.from_bytes(p[12:16],'big')==48000 and p[16:20]==bytes.fromhex('00080060') and vlan==(3,2))
   avtp.append(dict(ns=rec['tap_ns'],sid=p[4:12].hex(),valid=valid,port=rec['port'],seq=p[2],timestamp=int.from_bytes(p[20:28],'big'),dmac=fr[:6].hex(),src=fr[6:12].hex()))
if result.get('seq') is not None:
 rows=[json.loads(s) for s in (dest/(result['mode']+'.jsonl')).read_text().splitlines()]
 tx=next(r for r in rows if r.get('kind')=='transaction' and r['mt']==6)
 ack=next(r for r in acmp if r['mt']==7 and r['status']==0 and r['seq']==result['seq'] and r['controller']==tx['response']['controller'])
 arr=[r for r in avtp if r['valid'] and r['sid']==result['stream_id'] and r['ns']>=ack['ns']]
 latency=(arr[0]['ns']-ack['ns'])/1e9 if arr else None
 states=[json.loads(s) for s in (dest/'snapshot-after.jsonl').read_text().splitlines()]
 role='dut' if result['direction']=='listener' else 'peer'
 what='state-5-1' if result['direction']=='listener' else 'state-5-8'
 state=next(r['response'] for r in states if r.get('role')==role and r.get('what')==what)
 assert state['status']==0 and state['conn_count']==1,'settled binding absent'
 assert state['stream_id']==result['stream_id'],'stream binding mismatch'
 if arr:
  assert arr[0]['dmac']==state['dmac'],'destination mismatch'
  assert arr[0]['src']==result['stream_id'][:12],'source mismatch'
  assert arr[0]['port']==(2 if result['direction']=='listener' else 3),'direction mismatch'
 result['settled_binding_matches']=True
 command=next(r for r in acmp if r['mt']==6 and r['seq']==result['seq'] and r['controller']==tx['response']['controller'])
 declarations=[e for e in events if e['stream_id']==result['stream_id'] and e['event'] in ('New','JoinIn','JoinMt') and e['ns']>=command['ns']]
 ready=next((e for e in declarations if e['type']=='Listener' and e['listener']==2),None)
 advert=next((e for e in declarations if e['type']=='TalkerAdvertise'),None)
 result['first_ready_since_connect_ns']=ready['ns'] if ready else None
 result['first_advertise_since_connect_ns']=advert['ns'] if advert else None
 result['response_to_ready_s']=(ready['ns']-ack['ns'])/1e9 if ready else None
 result['ready_to_first_avtp_s']=(arr[0]['ns']-ready['ns'])/1e9 if ready and arr else None
 result['ready_sender']=ready['sender'] if ready else None

 assert latency==result['latency_s'],'independent timing mismatch'
 result['first_sequence']=arr[0]['seq'] if arr else None
 result['first_timestamp']=arr[0]['timestamp'] if arr else None
 result['next_sequence']=arr[1]['seq'] if len(arr)>1 else None
 result['next_timestamp']=arr[1]['timestamp'] if len(arr)>1 else None
 if len(arr)>1:assert arr[1]['seq']==(arr[0]['seq']+1)%256 and arr[1]['timestamp']>arr[0]['timestamp'],'first pair progression'
start=min(r['tap_ns'] for r in raw);end=max(r['tap_ns'] for r in raw)
cut=result.get('disconnect_response_ns',result.get('response_ns',end));ack=result.get('response_ns',start)
windows={'before':(start,cut),'after':(ack,end),'whole':(start,end)}
if result.get('first_avtp_ns') is not None:windows['resumed']=(result['first_avtp_ns'],end)
counts={}
for window,(lo,hi) in windows.items():
 counts[window]={}
 for sender in ['DUT','bridge']:
  es=[e for e in events if e['sender']==sender and lo<=e['ns']<hi]
  ps=[e for e in pdus if e['sender']==sender and lo<=e['ns']<hi]
  counts[window][sender]=dict(seconds=(hi-lo)/1e9,pdus=len(ps),rate=len(ps)/((hi-lo)/1e9) if hi>lo else None,leaveall_vectors=sum(e['event']=='LeaveAll' for e in es),events=dict(collections.Counter(e['event'] for e in es)),types={t:dict(collections.Counter(e['event'] for e in es if e['type']==t)) for t in TYPES.values()},ready=sum(e['listener']==2 and e['event'] in ('New','JoinIn','JoinMt') for e in es),target_ready=sum(e['listener']==2 and e['stream_id']==result['stream_id'] and e['event'] in ('New','JoinIn','JoinMt') for e in es),target_talker=sum(e['type']=='TalkerAdvertise' and e['stream_id']==result['stream_id'] and e['event']!='LeaveAll' for e in es))
result.update(msrp=counts,msrp_parse_errors=malformed,msrp_sources={sender:sorted({x['source'] for x in pdus if x['sender']==sender}) for sender in ['DUT','bridge']},valid_avtp=sum(x['valid'] for x in avtp),acmp_wire_counts={sender:dict(collections.Counter(str(e['mt']) for e in acmp if e['sender']==sender)) for sender in ['DUT','bridge']})
with (dest/'msrp.tsv').open('w') as f:
 f.write('tap_ns\tsender\ttype\tevent\tstream_id\tlistener\tfirst_value\n')
 for e in events:f.write('\t'.join(str(e[k]) for k in ['ns','sender','type','event','stream_id','listener','first_value'])+'\n')
(dest/'analysis.json').write_text(json.dumps(result,indent=2)+'\n')
assert not malformed,malformed
print(name,result['status'],result.get('latency_s'),'MSRP PDUs',len(pdus),'parsed events',len(events))
