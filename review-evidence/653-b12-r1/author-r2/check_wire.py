"""Offline raw-byte controls for the B12 capture selector."""
import json,struct,sys
from pathlib import Path
from wire import analyze
src=Path('/tmp/653-b12/raw/653-b12-pilot-A0300-1-plain.pcap').read_bytes();head=src[:24];off=24;pkts={};i=0
while off<len(src):
 sec,us,n,orig=struct.unpack('<4I',src[off:off+16]);p=src[off+16:off+16+n];off+=16+n;i+=1;pkts[i]=p
r=json.loads(Path('/tmp/653-b12/raw/A0300-1-result.json').read_text());w=r['wire']
zero=next(p for p in w['pushes'] if p['counters']['MU']==0)
base=[pkts[zero['i']],pkts[w['command']['i']],pkts[w['response']['i']],pkts[w['unlock']['i']]]
out=[]
def test(name,order,expect,mutate=None):
 frames=[bytearray(base[i]) for i in order]
 if mutate:mutate(frames)
 blob=head
 for i,p in enumerate(frames):
  t=10000000000+i*1000;struct.pack_into('<II',p,12,t>>32,t&0xffffffff)
  blob+=struct.pack('<4I',10,i,len(p),len(p))+p
 path=Path('/tmp/653-b12/raw/control-'+name+'.pcap');path.write_bytes(blob)
 a=analyze([(path,True)],w['command']['listener'],w['command']['luid'],w['command']['ctl'])
 g=a['wire'];got=g['order'] if g else 'NO_MATCH'
 assert got==expect,(name,got,expect)
 out.append(dict(control=name,expected=expect,result=got))
test('response-first',[0,1,2,3],'RESPONSE_FIRST')
test('reversed',[0,1,3,2],'COUNTERS_FIRST')
test('missing-push',[0,1,2],'NO_UNLOCK_PUSH')
test('prior-unlock',[0,3,1,2],'NO_UNLOCK_PUSH')
def wrong_controller(fs):fs[-1][28+14+12]^=1
test('foreign-controller',[0,1,2,3],'NO_UNLOCK_PUSH',wrong_controller)
def wrong_input(fs):fs[-1][28+14+27]^=1
test('foreign-input',[0,1,2,3],'NO_UNLOCK_PUSH',wrong_input)
def wrong_sequence(fs):fs[2][28+14+49]^=1
test('foreign-response-sequence',[0,1,2,3],'NO_MATCH',wrong_sequence)
# A peer can suppress its reset push. A live solicited zero still establishes
# the baseline for the session's later unsolicited unlock notification.
peer=Path('/tmp/653-b12/raw/653-b12-B-AAF-BAAF0300-1-observer.pcap')
from wire import records
rr=list(records(peer,False));cs=[r for r in rr if r['kind']=='acmp' and r['mt']==8];c=cs[0]
ans=next(r for r in rr if r['kind']=='acmp' and r['mt']==9 and r['seq']==c['seq'])
ps=[r for r in rr if r['kind']=='aecp' and r.get('desc')==[5,0] and r.get('target')==c['listener']]
assert not any(r.get('u') and r['counters']['MU']==0 for r in ps)
assert any(not r.get('u') and r['i']<c['i'] and r['counters']['MU']==0 for r in ps)
a=analyze([(peer,False)],c['listener'],c['luid'],c['ctl'])
assert a['wire']['order']=='RESPONSE_FIRST'
out.append(dict(control='solicited-zero-before-first-push',expected='RESPONSE_FIRST',result=a['wire']['order']))
print(json.dumps(out,indent=2))
