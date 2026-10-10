"""Lane B14 item 4 (#667): two-second talker starts, supervised in the foreground.

usage: start_b14.py <first> <last>      (the caller holds the bench lock for the invocation)

Lane B13's run_short.py with the parts of run_b13.py it imports (Probe, Capture, caps,
finish_caps, emit), unchanged in method: B13's probe (/tmp/608-b14/probe, B13's probe.cpp
rebuilt), per start `cycle start-NNN B 0 0 2000 1200 500` (the DUT's STREAM_OUTPUT 0 to the
peer's STREAM_INPUT 0, the binding rule inside the probe, a 2,000 ms hold from the bind
response, the peer's counters polled at 20, 100 and 250 ms and every 500 ms, then 1,200 ms after
the unbind), and B13's three captures around each start (the brief's untagged-AVTP filter and the
VLAN-tagged AVTP on the tap, the controller host's AVDECC control frames), copied back and removed
from the capturing host. Changes: B14's paths and names, the HANDOFF ledger replaced by
item4/ledger.tsv, and the invocation runs a range so two invocations stay inside the foreground
limit. Environment (private): B14_OUT, CTL_HOST, CTL_IFACE, PEER_EID, TAP_HOST, TAP_IFACE.
"""
import hashlib,json,os,queue,select,shlex,subprocess,sys,threading,time
from pathlib import Path
from datetime import datetime,timezone
E=os.environ;OUT=Path(E['B14_OUT'])/'item4';RAW=Path('/tmp/608-b14/raw/item4')
OUT.mkdir(parents=True,exist_ok=True);RAW.mkdir(parents=True,exist_ok=True)
SSH=['ssh','-o','BatchMode=yes','-o','ConnectTimeout=8']
DUT='020000fffe000001';PEER=E['PEER_EID']
def utc():return datetime.now(timezone.utc).isoformat()
def emit(**x):
 x={'utc':utc(),**x};print(json.dumps(x),flush=True)
 with (OUT/'run-events.jsonl').open('a') as f:f.write(json.dumps(x)+'\n')
def call(args,seconds=30):
 r=subprocess.run(['timeout','-k','3s',str(seconds)+'s']+args,capture_output=True,text=True,timeout=seconds+5)
 if r.returncode:raise RuntimeError('bounded command rc '+str(r.returncode))
 return r.stdout
def ledger(tag,elapsed,result):
 with (OUT/'ledger.tsv').open('a') as f:f.write(f'{tag}\t{utc()}\t{elapsed:.3f}\t{result}\n')

class Capture:
 def __init__(self,tag,kind,seconds=85):
  self.kind=kind;self.tag=tag;self.host=E['CTL_HOST'] if kind=='control' else E['TAP_HOST']
  iface=E['CTL_IFACE'] if kind=='control' else E['TAP_IFACE']
  filt={'plain':'ether[40:2]=0x22f0','vlan':'ether[40:2]=0x8100 and ether[44:2]=0x22f0','control':'(ether[12:2]=0x22f0 and (ether[14]=0xfb or ether[14]=0xfc)) or (ether[12:2]=0x8100 and ether[16:2]=0x22f0 and (ether[18]=0xfb or ether[18]=0xfc))'}[kind]
  self.name=f'608-b14-{tag}-{kind}.pcap';self.path='/tmp/'+self.name
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
 def __init__(self,stem):
  cmd=shlex.join(['sudo','-n','timeout','560s','/tmp/608-b14/probe',E['CTL_IFACE'],DUT,PEER,'3353','3354'])
  self.raw=(RAW/(stem+'-probe.jsonl')).open('w');self.err=(RAW/(stem+'-probe.stderr')).open('w');self.events=[];self.q=queue.Queue()
  self.p=subprocess.Popen(['timeout','-k','5s','580s']+SSH+[E['CTL_HOST'],cmd],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=self.err,text=True,bufsize=1)
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

def main():
 first,last=int(sys.argv[1]),int(sys.argv[2])
 pr=None;active=[];rows=[]
 try:
  pr=Probe(f'starts-{first:03d}-{last:03d}');ready=pr.wait(lambda r:r.get('ev')=='both_online',110)
  if not ready or not ready['ok']:raise RuntimeError('both entities not online')
  for n in range(first,last+1):
   tag=f'start-{n:03d}';active=caps(tag);begin=len(pr.events);t0=time.monotonic()
   pr.send(f'cycle {tag} B 0 0 2000 1200 500')
   result=pr.wait(lambda r:r.get('ev')=='cycle_end' and r.get('tag')==tag,18)
   elapsed=time.monotonic()-t0
   finish_caps(active);active=[]
   events=pr.events[begin:]
   polls=[r for r in events if r.get('ev')=='poll' and r.get('tag')==tag]
   # Listener counters reset at bind. The largest bound observation retains
   # a startup increment even when the application callback arrives later.
   post=[r for r in polls if r['phase']!='pre-bind']
   if any(not r['status'].startswith('Success') for r in polls):raise RuntimeError('counter read failed')
   early=max((r['counters'].get('EARLY',0) for r in post),default=None)
   late=max((r['counters'].get('LATE',0) for r in post),default=None)
   row={'cycle':tag,'result':result,'early':early,'late':late,'polls':polls,'formats':[r for r in events if r.get('ev') in ('formats','set_listener_format')],'bind_unbind':[r for r in events if r.get('ev') in ('bind','unbind')],'hive_rule':[r for r in events if r.get('ev')=='hive_rule']}
   (OUT/(tag+'.json')).write_text(json.dumps(row,indent=2)+'\n');rows.append({'cycle':tag,'early':early,'late':late,'result':result})
   ledger(tag,elapsed,f'EARLY {early}; LATE {late}');emit(event='short_cycle',cycle=tag,early=early,late=late,result=result and result.get('result'))
   if not result or result['result']!='OK':raise RuntimeError('short cycle failed')
 finally:
  try:
   if pr:pr.quit()
  finally:
   if active:finish_caps(active)
  (OUT/f'short-summary-{first:03d}-{last:03d}.json').write_text(json.dumps(rows,indent=2)+'\n')
 return 0
if __name__=='__main__':sys.exit(main())
