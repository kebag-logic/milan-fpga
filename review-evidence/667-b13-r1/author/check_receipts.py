"""Offline counter, header, and complete-restoration adverse controls."""
import copy,importlib.util,json,os,sys,tempfile
from pathlib import Path
p=Path(sys.argv[1]);sys.path.insert(0,str(p))
os.environ.update(B13_OUT=str(p),PEER_EID='0'*16,PEER_MAC='0'*12,CTL_IFACE='unused')
from run_b13 import counter_errors,key
from compare_restore import compare
from decode_capture import signed_delta,header
results=[]
def record(name,passed):
 assert passed,name
 results.append({'control':name,'passed':True})
r=dict(role='dut',descriptor_type=5,descriptor_index=0,status='SUCCESS',valid_mask=4095,counters={str(n):0 for n in range(12)},response_ns=1,sequence=2)
record('zero error baseline',not counter_errors([r],{key(r):r}))
for i in (1,2,3,8,9,10):
 bad=copy.deepcopy(r);bad['counters'][str(i)]=1
 record('error bit '+str(i),len(counter_errors([bad],{key(r):r}))==1)
record('positive modulo rollover',signed_delta(0x0000fff0,0xfffffff0)==65536)
record('negative modulo rollover',signed_delta(0xfffffff0,0x0000fff0)==-65536)
record('B12 early step',signed_delta(0xd7ccf250,0xd9353fed)==-23612829)
record('B12 late step',signed_delta(0x3050f58d,0x113d7f85)==521369096)
h=bytearray(24);h[0]=2;h[1]=0x89;h[2]=255;h[3]=1;h[12:16]=(123456789).to_bytes(4,'big');h[22]=16
d=header(h);record('independent header bits',all(d[k]==v for k,v in {'sequence':255,'tv':1,'mr':1,'tu':1,'sp':1,'avtp_timestamp':123456789}.items()))
try:header(bytes(23));truncated=False
except ValueError:truncated=True
record('truncated header rejected',truncated)
start=p/'restore-start.jsonl';rows=[json.loads(x) for x in start.read_text().splitlines()]
record('complete restore equal success',compare(start,start)['result']=='PASS')
with tempfile.TemporaryDirectory(prefix='667-b13-controls-',dir='/tmp') as t:
 path=Path(t)/'end.jsonl'
 def rejects(name,values):
  path.write_text(''.join(json.dumps(x)+'\n' for x in values))
  try:compare(start,path);bad=False
  except (ValueError,KeyError,TypeError):bad=True
  record(name,bad)
 rejects('empty restoration',[])
 rejects('missing restoration row',rows[:-1])
 rejects('duplicate restoration row',rows+[rows[-1]])
 z=copy.deepcopy(rows);z[1]['status']='TIMEOUT';rejects('failed readback',z)
 z=copy.deepcopy(rows);z[1]['value']='00';rejects('truncated format',z)
 z=copy.deepcopy(rows);z[2]['connections']=1;rejects('binding remains',z)
 z=copy.deepcopy(rows);next(x for x in z if x['category']=='clock')['value']=2;rejects('changed source',z)
 z=copy.deepcopy(rows);next(x for x in z if x['category']=='map')['effective_sha256']='0'*64;rejects('changed map digest',z)
(p/'offline-controls.json').write_text(json.dumps(results,indent=2)+'\n')
print(len(results),'controls passed')
