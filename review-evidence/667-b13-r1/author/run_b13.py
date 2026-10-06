"""Foreground supervised B13 run. The caller holds the shared action lock."""
import hashlib,json,os,queue,select,shlex,subprocess,sys,threading,time
from pathlib import Path
from datetime import datetime,timezone
E=os.environ;OUT=Path(E['B13_OUT']);RAW=Path('/tmp/667-b13/raw')
SSH=['ssh','-o','BatchMode=yes','-o','ConnectTimeout=8']
DUT='020000fffe000001';PEER=E['PEER_EID']
ENDPOINTS=[E['CTL_IFACE'],PEER,E['PEER_MAC']]
BINDINGS=[('A-AAF','A',0,0),('A-CRF','A',2,1),('B-AAF','B',0,0),('B-CRF','B',1,8)]
def utc():return datetime.now(timezone.utc).isoformat()
def emit(**x):
 x={'utc':utc(),**x};print(json.dumps(x),flush=True)
 with (OUT/'run-events.jsonl').open('a') as f:f.write(json.dumps(x)+'\n')
def call(args,seconds=30):
 r=subprocess.run(['timeout','-k','3s',str(seconds)+'s']+args,capture_output=True,text=True,timeout=seconds+5)
 if r.returncode:raise RuntimeError('bounded command rc '+str(r.returncode))
 return r.stdout

def state(mode,tag,*args):
 cmd=['sudo','-n','timeout','25s','python3','-B','/tmp/667-b13/read_state.py',mode]+ENDPOINTS+list(map(str,args))
 txt=call(SSH+[E['CTL_HOST'],shlex.join(cmd)],32)
 rows=[json.loads(x) for x in txt.splitlines()]
 (OUT/(tag+'.jsonl')).write_text(txt)
 return rows

def ledger(tag,elapsed,result):
 p=OUT/'HANDOFF.md';s=p.read_text();row=f'| {tag} | {utc()} | {elapsed:.3f} s | {result} | {tag} captures | {result} |'
 lines=s.splitlines();old=next((i for i,l in enumerate(lines) if l.startswith('| '+tag+' |')),None)
 if old is not None:lines[old]=row
 else:
  k=lines.index('## Restoration');lines[k:k]=[row,'']
 p.write_text('\n'.join(lines)+'\n')

class Capture:
 def __init__(self,tag,kind,seconds=85):
  self.kind=kind;self.tag=tag;self.host=E['CTL_HOST'] if kind=='control' else E['TAP_HOST']
  iface=E['CTL_IFACE'] if kind=='control' else E['TAP_IFACE']
  filt={'plain':'ether[40:2]=0x22f0','vlan':'ether[40:2]=0x8100 and ether[44:2]=0x22f0','control':'(ether[12:2]=0x22f0 and (ether[14]=0xfb or ether[14]=0xfc)) or (ether[12:2]=0x8100 and ether[16:2]=0x22f0 and (ether[18]=0xfb or ether[18]=0xfc))'}[kind]
  self.name=f'667-b13-{tag}-{kind}.pcap';self.path='/tmp/'+self.name
  cmd=shlex.join(['sudo','-n','timeout',str(seconds)+'s','tcpdump','-i',iface,'-s','256','-U','-w',self.path,filt])
  self.p=subprocess.Popen(['timeout','-k','3s',str(seconds+15)+'s']+SSH+['-tt',self.host,cmd],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  self.buf=b'';end=time.monotonic()+12
  while time.monotonic()<end:
   if select.select([self.p.stdout],[],[],.2)[0]:
    b=os.read(self.p.stdout.fileno(),4096)
    if not b:break
    self.buf+=b
    if b'listening on' in self.buf:break
  self.ok=b'listening on' in self.buf
  if not self.ok:self.stop();raise RuntimeError('capture did not start')
 def alive(self):return self.p.poll() is None
 def stop(self):
  if self.p.poll() is None:
   self.p.stdin.write(b'\x03');self.p.stdin.flush()
  b,_=self.p.communicate(timeout=15);self.buf+=b
  summary=[s for s in self.buf.decode(errors='replace').replace('\r','').splitlines() if 'packet' in s]
  (OUT/(self.name+'.json')).write_text(json.dumps({'capture':self.name,'rc':self.p.returncode,'summary':summary},indent=2)+'\n')
 def collect(self):
  expected=call(SSH+[self.host,'timeout 25s sha256sum '+self.path],30).split()[0]
  call(['scp','-q','-o','BatchMode=yes',self.host+':'+self.path,str(RAW/self.name)],50)
  p=RAW/self.name;h=hashlib.file_digest(p.open('rb'),'sha256').hexdigest();assert h==expected
  with (OUT/'capture-artifacts.jsonl').open('a') as f:f.write(json.dumps({'file':str(p),'bytes':p.stat().st_size,'sha256':h,'remote_hash_matches':True})+'\n')
  call(SSH+[self.host,'sudo -n timeout 10s rm -- '+self.path],15)

def caps(tag):
 result=[]
 try:
  for k in ('plain','vlan','control'):result.append(Capture(tag,k))
  return result
 except BaseException:
  for c in result:c.stop();c.collect()
  raise

def finish_caps(items):
 for c in items:c.stop()
 for c in items:c.collect()

class Probe:
 def __init__(self):
  cmd=shlex.join(['sudo','-n','timeout','8200s','/tmp/667-b13/probe',E['CTL_IFACE'],DUT,PEER,'3353','3354'])
  self.raw=(RAW/'probe.jsonl').open('w');self.err=(RAW/'probe.stderr').open('w');self.events=[];self.q=queue.Queue()
  self.p=subprocess.Popen(['timeout','-k','5s','8230s']+SSH+[E['CTL_HOST'],cmd],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=self.err,text=True,bufsize=1)
  self.thread=threading.Thread(target=self.read);self.thread.start()
 def read(self):
  for line in self.p.stdout:
   self.raw.write(line);self.raw.flush()
   try:r=json.loads(line)
   except ValueError:continue
   self.events.append(r);self.q.put(r)
  self.q.put(None)
 def send(self,line):self.p.stdin.write(line+'\n');self.p.stdin.flush()
 def wait(self,pred,seconds):
  end=time.monotonic()+seconds
  while time.monotonic()<end:
   try:r=self.q.get(timeout=max(.01,end-time.monotonic()))
   except queue.Empty:return None
   if r is None:return None
   if pred(r):return r
  return None
 def quit(self):
  if self.p.poll() is None:self.send('quit');self.p.stdin.close()
  self.p.wait(timeout=45);self.thread.join(timeout=5);self.raw.close();self.err.close()
  emit(event='probe_exit',rc=self.p.returncode)

ERR_NAMES={1:'MEDIA_UNLOCKED',2:'STREAM_INTERRUPTED',3:'SEQ_NUM_MISMATCH',8:'UNSUPPORTED_FORMAT',9:'LATE_TIMESTAMP',10:'EARLY_TIMESTAMP'}
def key(r):return (r['role'],r['descriptor_type'],r['descriptor_index'])
def counter_errors(rows,previous,first=False):
 errors=[]
 for r in rows:
  k=key(r);old=previous.get(k)
  if k==('dut',0,0) and r['status']=='NOT_SUPPORTED':continue
  if r['status']!='SUCCESS':errors.append({'descriptor':k,'error':'counter read failed'});continue
  if old and r.get('valid_mask')!=old.get('valid_mask'):errors.append({'descriptor':k,'error':'valid mask changed'})
  for bit,v in r['counters'].items():
   bit=int(bit);before=old.get('counters',{}).get(str(bit),0) if old else 0
   if r['descriptor_type']==5:
    if bit not in ERR_NAMES:continue
    if first:before=0
    name=ERR_NAMES[bit]
   elif r['descriptor_type']==9 and bit in (1,4,5):name={1:'LINK_DOWN',4:'RX_CRC_ERROR',5:'GPTP_GM_CHANGED'}[bit]
   elif r['descriptor_type']==36 and bit==1:name='CLOCK_UNLOCKED'
   else:continue
   if v>before:errors.append({'descriptor':k,'counter':name,'before':before,'after':v,'delta':v-before,'response_ns':r['response_ns'],'sequence':r.get('sequence')})
 return errors

def check_timing(rows,baseline):
 errors=[]
 for r,b in zip(rows,baseline):
  if r['status']!='SUCCESS':errors.append({'error':'timing read failed'})
  for k in ('gm_fingerprint','as_capable','path_fingerprint'):
   if k in b and r.get(k)!=b[k]:errors.append({'role':r['role'],'error':k+' changed','response_ns':r['response_ns']})
 return errors

def main():
 pr=None;active=[];bound=[];stopped=None;t0=None
 try:
  pr=Probe();ready=pr.wait(lambda r:r.get('ev')=='both_online',110)
  if not ready or not ready['ok']:raise RuntimeError('both entities not online')
  emit(event='both_online')
  timing0=state('timing','timing-prebind')
  baseline=state('counters','counters-prebind')
  previous={key(r):r for r in baseline}
  active=caps('soak-000');ledger('soak-000',0,'RUNNING')
  for tag,direction,ti,li in BINDINGS:
   bound.append((tag,direction,ti,li))
   pr.send(f'holdbind {tag} {direction} {ti} {li} 0 0 0')
   result=pr.wait(lambda r:r.get('ev')=='cycle_end' and r.get('tag')==tag,15)
   emit(event='soak_bind',tag=tag,result=result)
   if not result or result['result']!='HELD':raise RuntimeError('soak bind failed')
  t0=time.monotonic();emit(event='soak_start')
  poll=0
  while True:
   tag=f'soak-{poll:03d}';rows=state('counters','counters-'+tag)
   errors=counter_errors(rows,previous,first=poll==0);previous={key(r):r for r in rows}
   # Five-minute requirements are exceeded by reading both timing queries per poll.
   timing=state('timing','timing-'+tag);errors+=check_timing(timing,timing0)
   elapsed=time.monotonic()-t0
   emit(event='soak_poll',cycle=tag,elapsed_s=elapsed,errors=errors)
   ledger(tag,elapsed,'STOP' if errors else 'CLEAN')
   if errors:
    stopped={'cycle':tag,'elapsed_s':elapsed,'errors':errors};(OUT/'STOP-TRACE.json').write_text(json.dumps(stopped,indent=2)+'\n');break
   if elapsed>=7200:break
   next_at=min(7200,(poll+1)*50)
   while time.monotonic()-t0<next_at:
    if not all(c.alive() for c in active):raise RuntimeError('rolling capture ended unexpectedly')
    # Observe application errors between scheduled reads without treating unbind cleanup as soak.
    for e in pr.events:
     if e.get('ev')=='hive_rule' and e.get('t',0)>rows[0]['request_ns']//1000 and any(e.get('increments',{}).values()):
      # Confirm with direct reads at once. A fresh poll creates the trace.
      next_at=0;break
    if next_at==0:break
    time.sleep(min(.25,max(0,next_at-(time.monotonic()-t0))))
   new=caps(f'soak-{poll+1:03d}')
   old=active;active=new;finish_caps(old)
   poll+=1
  emit(event='soak_end',elapsed_s=time.monotonic()-t0,stopped=bool(stopped))
 finally:
  if pr:
   for tag,direction,ti,li in reversed(bound):
    try:
     pr.send(f'release {tag} {direction} {ti} {li} 0 0 0')
     r=pr.wait(lambda r:r.get('ev')=='release' and r.get('tag')==tag,8)
     emit(event='restore_unbind',tag=tag,result=r)
    except Exception as ex:emit(event='restore_error',step='unbind',error=type(ex).__name__)
   pr.quit()
  if active:finish_caps(active)
  emit(event='capture_cleanup_complete')
 if stopped:return 3
 return 0
if __name__=='__main__':
 try:sys.exit(main())
 except Exception as ex:
  emit(event='STOP',reason=str(ex));sys.exit(4)
