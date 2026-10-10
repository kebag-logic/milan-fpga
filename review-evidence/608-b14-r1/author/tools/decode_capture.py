"""Stream a tap pcap into bounded role-safe header and sequence receipts."""
import collections,hashlib,json,statistics,struct,sys
from pathlib import Path

def signed_delta(new,old):return (new-old+(1<<31))%(1<<32)-(1<<31)
def records(path):
 with Path(path).open('rb') as f:
  h=f.read(24)
  if h[:4]!=bytes.fromhex('d4c3b2a1'):raise ValueError('unsupported pcap encoding')
  n=0
  while True:
   h=f.read(16)
   if not h:return
   if len(h)!=16:raise ValueError('truncated record')
   sec,usec,size,orig=struct.unpack('<4I',h);b=f.read(size);n+=1
   if len(b)!=size or len(b)<42:raise ValueError('truncated packet')
   port,hi,lo=struct.unpack('<3I',b[8:20]);tap=(hi<<32)|lo
   frame=b[28:];off=14;et=frame[12:14]
   if et==bytes.fromhex('8100'):et=frame[16:18];off=18
   if et!=bytes.fromhex('22f0'):continue
   yield n,tap,port,frame[off:]
def header(a):
 if len(a)<24:raise ValueError('truncated stream header')
 b=bytearray(a[:24]);b[4:12]=bytes(8)
 r=dict(sequence=a[2],mr=(a[1]>>3)&1,tu=a[3]&1,header=b.hex())
 if a[0]==2:r.update(tv=a[1]&1,sp=(a[22]>>4)&1,avtp_timestamp=int.from_bytes(a[12:16],'big'))
 return r

def analyze(paths):
 streams={};controls=[];nonmonotonic=0
 for path in paths:
  prev=-1
  for n,t,port,a in records(path):
   if t<prev:nonmonotonic+=1
   prev=t
   if len(a)<24:continue
   role='dut' if port==3 else 'peer' if port==2 else 'unknown'
   if a[0] in (2,4):
    sid=a[4:12].hex();k=(role,a[0],sid)
    v=streams.setdefault(k,dict(role=role,subtype=a[0],stream_unique_id=int.from_bytes(a[10:12],'big'),count=0,first=[],last=[],gaps=0,gap_examples=[],mr_toggles=[],tu_toggles=[],timestamp_steps=[],previous=None))
    x=dict(capture=Path(path).name,record=n,tap_ns=t,port=port,**header(a));previous=v['previous']
    if previous:
     if x['sequence']!=(previous['sequence']+1)%256:
      v['gaps']+=1
      if len(v['gap_examples'])<20:v['gap_examples'].append(dict(before=previous,after=x))
     for field in ('mr','tu'):
      if previous[field]!=x[field] and len(v[field+'_toggles'])<20:v[field+'_toggles'].append(dict(before=previous,after=x))
     if a[0]==2 and v['count']<100:v['timestamp_steps'].append(signed_delta(x['avtp_timestamp'],previous['avtp_timestamp']))
    if len(v['first'])<10:v['first'].append(x)
    v['last']=(v['last']+[x])[-10:];v['previous']=x;v['count']+=1
   elif a[0]==0xfb and len(a)>=32 and int.from_bytes(a[22:24],'big')&32767==0x29:
    b=bytearray(a[:160]);b[4:20]=bytes(16)
    controls.append(dict(capture=Path(path).name,record=n,tap_ns=t,port=port,role=role,message_type=a[1]&15,status=a[2]>>3,sequence=int.from_bytes(a[20:22],'big'),unsolicited=bool(a[22]&128),descriptor_type=int.from_bytes(a[24:26],'big'),descriptor_index=int.from_bytes(a[26:28],'big'),raw=b.hex()))
 for v in streams.values():
  v.pop('previous')
  if v['subtype']==2 and len(v['first'])==10:
   steps=v.pop('timestamp_steps');steady=statistics.median(steps[9:]) if len(steps)>9 else statistics.median(steps[1:]);v['steady_period_ns']=steady;v['first_step_ns']=steps[0]
   v['first_offset_from_steady_ns']=steady-steps[0]
   v['first_ten_timestamp_steps_ns']=steps[:9]
   v['steady_step_range_ns']=[min(steps[9:]),max(steps[9:])] if len(steps)>9 else None
   for i,x in enumerate(v['first']):x['relative_to_tenth_pdu_trend_ns']=signed_delta(x['avtp_timestamp'],v['first'][9]['avtp_timestamp'])-(i-9)*steady
  else:v.pop('timestamp_steps')
 return dict(streams=list(streams.values()),counter_wire=controls,nonmonotonic_records=nonmonotonic)
if __name__=='__main__':
 result=analyze(sys.argv[2:]);Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='counter_wire'},separators=(',',':'))[:1600])
