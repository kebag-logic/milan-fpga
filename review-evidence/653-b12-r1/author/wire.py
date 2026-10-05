"""B12 raw-byte capture reader. Tap timestamps use high-word then low-word LE32."""
import hashlib,json,struct
from pathlib import Path

def records(path,tap=True):
 with open(path,'rb') as f:
  h=f.read(24)
  assert len(h)==24 and h[:4]==bytes.fromhex('d4c3b2a1'),h.hex()
  i=0
  while True:
   h=f.read(16)
   if not h:break
   assert len(h)==16
   sec,usec,n,orig=struct.unpack('<4I',h);p=f.read(n);assert len(p)==n
   i+=1
   if tap:
    assert len(p)>=28
    port,hi,lo=struct.unpack('<III',p[8:20]);tns=(hi<<32)|lo; frame=p[28:]
   else:port=0;tns=sec*10**9+usec*1000;frame=p
   if len(frame)<14:continue
   offset=14;et=frame[12:14]
   if et in (b'\x81\x00',b'\x88\xa8'):
    et=frame[16:18];offset=18
   if et!=b'\x22\xf0':continue
   a=frame[offset:]
   if len(a)<4:continue
   r=dict(i=i,tns=tns,pcap_ns=sec*10**9+usec*1000,port=port,sub=a[0],mt=a[1]&15,status=a[2]>>3)
   if a[0]==0xfc and len(a)>=54:
    r.update(kind='acmp',ctl=a[12:20].hex(),talker=a[20:28].hex(),listener=a[28:36].hex(),tuid=int.from_bytes(a[36:38],'big'),luid=int.from_bytes(a[38:40],'big'),seq=int.from_bytes(a[48:50],'big'),cc=int.from_bytes(a[46:48],'big'),raw=a.hex())
   elif a[0]==0xfb and len(a)>=24:
    ct=int.from_bytes(a[22:24],'big')
    r.update(kind='aecp',target=a[4:12].hex(),ctl=a[12:20].hex(),seq=int.from_bytes(a[20:22],'big'),cmd=ct&32767,u=bool(ct&32768),raw=a.hex())
    if ct&32767==0x29 and r['mt']==1 and len(a)>=80:
     names=('ML','MU','SI','SEQ','MRST','TU','TSV','TSNV','UF','LATE','EARLY','FRX')
     r.update(desc=list(struct.unpack('>HH',a[24:28])),valid=int.from_bytes(a[28:32],'big'),counters=dict(zip(names,struct.unpack('>12I',a[32:80]))))
   elif a[0] in (2,4) and len(a)>=12:
    r.update(kind='stream',seq=a[2],stream=a[4:12].hex())
   else:r['kind']='other'
   yield r

def digest(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  while b:=f.read(2**20):h.update(b)
 return dict(path=str(path),bytes=Path(path).stat().st_size,sha256=h.hexdigest())

def analyze(paths,listener,idx,controller):
 controls=[]; streams={};badtime=0;gaps=[];total=0
 for path,tap in paths:
  last=-1
  for r in records(path,tap):
   total+=1
   if r['tns']<last:badtime+=1
   last=r['tns']
   if r['kind'] in ('acmp','aecp'):r['capture']=Path(path).name;controls.append(r)
   if r['kind']=='stream':
    key=(r['port'],r['stream'],r['sub']);v=streams.setdefault(key,dict(count=0,first=[],last=[],gaps=0,previous=None))
    item={k:r[k] for k in ('i','tns','seq')}
    if v['previous'] is not None and r['seq']!=(v['previous']['seq']+1)%256:
     v['gaps']+=1
     if len(gaps)<200:gaps.append(dict(stream=r['stream'],port=r['port'],before=v['previous'],after=item))
    v['previous']=item;v['count']+=1
    if len(v['first'])<12:v['first'].append(item)
    v['last']=(v['last']+[item])[-12:]
 def relevant(r):return r['kind']=='acmp' and r['listener']==listener and r['luid']==idx and r['ctl']==controller
 commands=[r for r in controls if relevant(r) and r['mt']==8]
 responses=[r for r in controls if relevant(r) and r['mt']==9]
 pushes=[r for r in controls if r['kind']=='aecp' and r['target']==listener and r['ctl']==controller and r['mt']==1 and r['cmd']==0x29 and r['u'] and r.get('desc')==[5,idx]]
 # Never compare timestamps from different capture clocks. Prefer the tap.
 selected=None
 for cap in [Path(p).name for p,tap in paths]:
  cs=[r for r in commands if r['capture']==cap];rs=[r for r in responses if r['capture']==cap];ps=[r for r in pushes if r['capture']==cap]
  if not cs or not rs:continue
  c=cs[0];r=next((r for r in rs if r['seq']==c['seq']),None)
  if r is None:continue
  # Inspect every increase, including ones before the command. A legitimate earlier
  # unlock must not disappear merely because the unbind follows it.
  inc=[];prev=None
  for p in sorted(ps,key=lambda p:p['i']):
   mu=p['counters']['MU']
   if prev is not None and mu>prev:inc.append(p)
   prev=mu
  observations=[p for p in controls if p['capture']==cap and p['kind']=='aecp' and p.get('target')==listener and p.get('desc')==[5,idx] and p['mt']==1 and p['status']==0 and p['i']<c['i']]
  observations.sort(key=lambda p:p['i'])
  before_mu=observations[-1]['counters']['MU'] if observations else None
  later=[p for p in ps if p['i']>c['i'] and before_mu is not None and p['counters']['MU']>before_mu]
  u=later[0] if later else None
  g=dict(capture=cap,command=c,response=r,unlock=u,earlier_increases=[p for p in inc if p['i']<c['i']],pushes=ps,status=r['status'],command_response_us=(r['tns']-c['tns'])/1000,order='NO_UNLOCK_PUSH',response_unlock_us=None)
  if u:g.update(order='RESPONSE_FIRST' if r['i']<u['i'] else 'COUNTERS_FIRST',response_unlock_us=(u['tns']-r['tns'])/1000)
  if selected is None or u is not None:selected=g
  if u is not None:break
 return dict(wire=selected,controls=controls,streams=[dict(port=k[0],stream=k[1],sub=k[2],**v) for k,v in streams.items()],gaps=gaps,nonmonotonic=badtime,total=total,artifacts=[digest(p) for p,t in paths])
