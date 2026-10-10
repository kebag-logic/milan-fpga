"""Lane B14 items 5-7: one chunk of the two-hour soak, supervised in the foreground.

usage: soak_b14.py <chunk_seconds>      (the caller holds the bench lock for the chunk)

Lane B13's run_b13.py soak, unchanged in what it reads: read_state.py `counters` (the DUT's
ENTITY, AVB_INTERFACE, CLOCK_DOMAIN, STREAM_INPUT 0-1 and STREAM_OUTPUT 0-1, the peer's
STREAM_INPUT 0 and 8) and `timing` (GET_AVB_INFO and GET_AS_PATH on both entities), B13's
counter_errors() rule, B13's probe as an observer of unsolicited counter notifications (its
application error rule), and B13's three rolling captures (the brief's untagged-AVTP filter and
the VLAN-tagged AVTP on the tap, AVDECC control frames on the controller host). Changes:
  * the soak runs in chunks under the foreground limit; the four bindings stay in the devices
    between chunks (made and released by bindops_b14.py, outside this file); state.json carries the
    soak start, the poll index and the previous counters across chunks;
  * the cadence is the assignment's: counters every 60 s, AVB info and AS path every 5 minutes
    (every fifth poll), a capture rotated at every poll;
  * every fifth poll also reads the DUT console, read-only: milan_status, MAC_STATUS (0x110),
    the RMON window as found (0x200-0x230, never armed: STATS_CTRL is not written), the MAAP words
    (0x6CC-0x6D4), the slip words (0x8D4-0x8DC) and the servo (0x8F8);
  * the error rule also counts the talkers' STREAM_STOP, MEDIA_RESET and TIMESTAMP_UNCERTAIN, and
    a finding does not stop the soak (the assignment: record it and continue).
Environment (private): B14_OUT, DUT_CONSOLE, CTL_HOST, CTL_IFACE, PEER_EID, PEER_MAC, TAP_HOST, TAP_IFACE.
"""
import hashlib,json,os,queue,select,shlex,subprocess,sys,threading,time
from pathlib import Path
from datetime import datetime,timezone
E=os.environ;OUT=Path(E['B14_OUT'])/'soak';RAW=Path('$VALIDATION_STORAGE/608-b14-raw/soak');STATE=RAW/'state.json'
TOOLS=Path(__file__).resolve().parent
OUT.mkdir(parents=True,exist_ok=True);RAW.mkdir(parents=True,exist_ok=True)
SSH=['ssh','-o','BatchMode=yes','-o','ConnectTimeout=8']
DUT='020000fffe000001';PEER=E['PEER_EID']
ENDPOINTS=[E['CTL_IFACE'],PEER,E['PEER_MAC']]
SOAK_S,POLL_S,TIMING_EVERY=7200,60,5
CONSOLE=['milan_status','mem_read 0x90000110 4','mem_read 0x90000200 52','mem_read 0x900006cc 12','mem_read 0x900008d4 12','mem_read 0x900008f8 4']
def utc():return datetime.now(timezone.utc).isoformat()
def emit(**x):
 x={'utc':utc(),**x};print(json.dumps(x),flush=True)
 with (OUT/'run-events.jsonl').open('a') as f:f.write(json.dumps(x)+'\n')
def call(args,seconds=30):
 r=subprocess.run(['timeout','-k','3s',str(seconds)+'s']+args,capture_output=True,text=True,timeout=seconds+5)
 if r.returncode:raise RuntimeError('bounded command rc '+str(r.returncode))
 return r.stdout
def state(mode,tag):
 cmd=['sudo','-n','timeout','25s','python3','-B','/tmp/608-b14/read_state.py',mode]+ENDPOINTS
 txt=call(SSH+[E['CTL_HOST'],shlex.join(cmd)],32)
 rows=[json.loads(x) for x in txt.splitlines()]
 (RAW/(tag+'.jsonl')).write_text(txt)
 return rows
def console(tag):
 r=subprocess.run(['timeout','-k','3s','60s','python3','-B',str(TOOLS/'console_read.py'),E['DUT_CONSOLE'],str(OUT/(tag+'.txt')),*CONSOLE],capture_output=True,text=True,timeout=65)
 return r.returncode
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
  with (OUT/'capture-receipts.jsonl').open('a') as f:f.write(json.dumps({'capture':self.name,'rc':self.p.returncode,'summary':summary})+'\n')
 def collect(self):
  expected=call(SSH+[self.host,'timeout 25s sha256sum '+self.path],30).split()[0]
  call(['scp','-q','-o','BatchMode=yes',self.host+':'+self.path,str(RAW/self.name)],90)
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
  cmd=shlex.join(['sudo','-n','timeout','590s','/tmp/608-b14/probe',E['CTL_IFACE'],DUT,PEER,'3353','3354'])
  self.raw=(RAW/(stem+'-probe.jsonl')).open('w');self.err=(RAW/(stem+'-probe.stderr')).open('w');self.events=[];self.q=queue.Queue()
  self.p=subprocess.Popen(['timeout','-k','5s','600s']+SSH+[E['CTL_HOST'],cmd],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=self.err,text=True,bufsize=1)
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
TALKER_ERR={1:'STREAM_STOP',2:'MEDIA_RESET',3:'TIMESTAMP_UNCERTAIN'}
def key(r):return (r['role'],r['descriptor_type'],r['descriptor_index'])
def counter_errors(rows,previous):
 errors=[]
 for r in rows:
  k=key(r);old=previous.get('|'.join(map(str,k)))
  if k==('dut',0,0) and r['status']=='NOT_SUPPORTED':continue
  if r['status']!='SUCCESS':errors.append({'descriptor':k,'error':'counter read failed'});continue
  if old and r.get('valid_mask')!=old.get('valid_mask'):errors.append({'descriptor':k,'error':'valid mask changed'})
  for bit,v in r['counters'].items():
   bit=int(bit);before=old.get('counters',{}).get(str(bit),0) if old else v
   if r['descriptor_type']==5:
    if bit not in ERR_NAMES:continue
    name=ERR_NAMES[bit]
   elif r['descriptor_type']==6 and bit in TALKER_ERR:name=TALKER_ERR[bit]
   elif r['descriptor_type']==9 and bit in (1,4,5):name={1:'LINK_DOWN',4:'RX_CRC_ERROR',5:'GPTP_GM_CHANGED'}[bit]
   elif r['descriptor_type']==36 and bit==1:name='CLOCK_UNLOCKED'
   else:continue
   if v>before:errors.append({'descriptor':k,'counter':name,'before':before,'after':v,'delta':v-before,'response_ns':r['response_ns']})
 return errors

def check_timing(rows,baseline):
 errors=[]
 for r,b in zip(rows,baseline):
  if r['status']!='SUCCESS':errors.append({'error':'timing read failed'})
  for k in ('gm_fingerprint','as_capable','path_fingerprint'):
   if k in b and r.get(k)!=b[k]:errors.append({'role':r['role'],'error':k+' changed','response_ns':r['response_ns']})
 return errors

def save(st):STATE.write_text(json.dumps(st)+'\n')

def main():
 chunk_s=float(sys.argv[1]);t_chunk=time.monotonic()
 st=json.loads(STATE.read_text())
 pr=None;active=[]
 if st.get('done'):raise SystemExit('soak already complete')
 try:
  stem=f"chunk-{st['chunks']:02d}"
  pr=Probe(stem);ready=pr.wait(lambda r:r.get('ev')=='both_online',110)
  emit(event='chunk_start',chunk=st['chunks'],both_online=bool(ready and ready['ok']))
  if not ready or not ready['ok']:raise RuntimeError('both entities not online')
  while True:
   k=st['poll'];tag=f'soak-{k:03d}'
   due=st['t0']+k*POLL_S
   # the poll is due at t0 + 60 k (wall clock); a chunk ends before a poll it cannot finish
   if time.monotonic()-t_chunk+max(0,due-time.time())+25>chunk_s:break
   if not active:active=caps(tag)
   while time.time()<due:time.sleep(min(.25,due-time.time()))
   rows=state('counters','counters-'+tag)
   prev=st['previous'];errors=counter_errors(rows,prev);st['previous']={'|'.join(map(str,key(r))):r for r in rows}
   timing=None;crc=None
   if k%TIMING_EVERY==0:
    timing=state('timing','timing-'+tag);errors+=check_timing(timing,st['timing0'])
    crc=console('console-'+tag)
   elapsed=time.time()-st['t0']
   hive=[e for e in pr.events if e.get('ev')=='hive_rule' and any(e.get('increments',{}).values())]
   emit(event='soak_poll',cycle=tag,elapsed_s=round(elapsed,3),errors=errors,timing=timing is not None,console_rc=crc,hive_increments=len(hive))
   ledger(tag,elapsed,('FINDING '+json.dumps(errors)) if errors else 'CLEAN')
   if errors:st.setdefault('findings',[]).append({'cycle':tag,'elapsed_s':elapsed,'errors':errors})
   st['poll']=k+1;save(st)
   if elapsed>=SOAK_S:
    st['done']=True;save(st);break
   nxt=f"soak-{k+1:03d}"
   if time.monotonic()-t_chunk+max(0,st['t0']+(k+1)*POLL_S-time.time())+25<=chunk_s:
    new=caps(nxt);old=active;active=new;finish_caps(old)
   else:
    finish_caps(active);active=[];break
 finally:
  try:
   if active:finish_caps(active)
  finally:
   if pr:
    hive=[e for e in pr.events if e.get('ev')=='hive_rule']
    pr.quit()
    with (OUT/'hive-events.jsonl').open('a') as f:
     for e in hive:f.write(json.dumps(e)+'\n')
   st['chunks']+=1;save(st)
   emit(event='chunk_end',chunk=st['chunks']-1,next_poll=st['poll'],done=bool(st.get('done')))
 return 0
if __name__=='__main__':sys.exit(main())
