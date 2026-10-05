"""B12 foreground cycle runner; caller owns bench lock; children have deadlines."""
import hashlib,json,os,queue,select,signal,subprocess,sys,threading,time
from pathlib import Path
from wire import analyze,digest
E=os.environ;RAW=Path('/tmp/653-b12/raw');OUT=Path(E['B12_OUT']);SESSION=sys.argv[1]
PLAN=json.loads(Path(sys.argv[2]).read_text());SSH=['ssh','-o','BatchMode=yes','-o','ConnectTimeout=8']
DUT='020000fffe000001';PEER=E['PEER_EID']
logfile=RAW/(SESSION+'-driver.jsonl')
def log(**kw):
 kw=dict(t=time.time(),**kw)
 with logfile.open('a') as f:f.write(json.dumps(kw)+'\n')
 print(json.dumps(kw),flush=True)
def run(args,timeout=30):
 r=subprocess.run(args,capture_output=True,text=True,timeout=timeout)
 if r.returncode:raise RuntimeError(f'command failed rc={r.returncode}: '+r.stderr[-500:])
 return r.stdout
class Cap:
 def __init__(self,tag,kind,seconds):
  self.kind=kind;self.tag=tag
  self.host=E['CTL_HOST'] if kind=='observer' else E['TAP_HOST']
  iface=E['CTL_IFACE'] if kind=='observer' else E['TAP_IFACE']
  filt={'plain':'ether[40:2]=0x22f0','vlan':'ether[40:2]=0x8100 and ether[44:2]=0x22f0','observer':'(ether[12:2]=0x22f0 and (ether[14]=0xfb or ether[14]=0xfc)) or (ether[12:2]=0x8100 and ether[16:2]=0x22f0 and (ether[18]=0xfb or ether[18]=0xfc))'}[kind]
  self.name=f'653-b12-{SESSION}-{tag}-{kind}.pcap';self.remote='/tmp/'+self.name
  cmd=f'sudo -n timeout {seconds}s tcpdump -i {iface} -s 256 -U -w {self.remote} "{filt}"'
  self.p=subprocess.Popen(SSH+['-tt',self.host,cmd],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  self.buf=b'';deadline=time.monotonic()+12
  while time.monotonic()<deadline:
   if select.select([self.p.stdout],[],[],0.2)[0]:
    b=os.read(self.p.stdout.fileno(),4096)
    if not b:break
    self.buf+=b
    if b'listening on' in self.buf:break
  self.ok=b'listening on' in self.buf
  log(ev='capture_start',tag=tag,kind=kind,ok=self.ok)
 def stop(self):
  if self.p.poll() is None:
   self.p.stdin.write(b'\x03');self.p.stdin.flush()
  out,_=self.p.communicate(timeout=15)
  txt=(self.buf+out).decode(errors='replace').replace('\r','')
  (RAW/(self.name+'.log')).write_text(txt)
  log(ev='capture_stop',tag=self.tag,kind=self.kind,rc=self.p.returncode,summary=[x for x in txt.splitlines() if 'packet' in x])
 def collect(self):
  rh=run(SSH+[self.host,'timeout 30s sha256sum '+self.remote],40).split()[0]
  run(['scp','-q','-o','BatchMode=yes',self.host+':'+self.remote,str(RAW/self.name)],180)
  meta=digest(RAW/self.name);assert rh==meta['sha256']
  run(SSH+[self.host,'sudo -n timeout 10s rm -- '+self.remote],20)
  return RAW/self.name,self.kind!='observer'
class Probe:
 def __init__(self):
  self.events=[];self.q=queue.Queue();self.f=(RAW/(SESSION+'-probe.jsonl')).open('w');self.err=(RAW/(SESSION+'-probe.stderr')).open('w')
  cmd=f"sudo -n timeout 960s {E.get('B12_PROBE','/tmp/653-b12/probe')} {E['CTL_IFACE']} {DUT} {PEER} 3090 3091"
  self.p=subprocess.Popen(SSH+[E['CTL_HOST'],cmd],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=self.err,text=True,bufsize=1)
  self.thread=threading.Thread(target=self.read);self.thread.start()
 def read(self):
  for line in self.p.stdout:
   self.f.write(line);self.f.flush()
   try:e=json.loads(line)
   except ValueError:continue
   self.events.append(e);self.q.put(e)
  self.q.put(None)
 def send(self,s):self.p.stdin.write(s+'\n');self.p.stdin.flush()
 def wait(self,pred,seconds):
  end=time.monotonic()+seconds
  while time.monotonic()<end:
   try:e=self.q.get(timeout=max(.01,end-time.monotonic()))
   except queue.Empty:return None
   if e is None:return None
   if pred(e):return e
  return None
 def quit(self):
  if self.p.poll() is None:self.send('quit');self.p.stdin.close()
  self.p.wait(timeout=50);self.thread.join(timeout=5);self.f.close();self.err.close()
  log(ev='probe_exit',rc=self.p.returncode)
def handoff(row):
 p=OUT/'HANDOFF.md';s=p.read_text();mark='\n## Sequence windows'
 assert mark in s;s=s.replace(mark,'\n'+row+'\n'+mark);p.write_text(s)
def main():
 pr=Probe();caps=[];status=0
 try:
  ready=pr.wait(lambda e:e.get('ev')=='both_online',110)
  if not ready or not ready['ok']:raise RuntimeError('entities not online')
  ctl=next(e['session_eid'] for e in pr.events if e['ev']=='entities')
  for item in PLAN:
   tag,direction,ti,li,hold=item['tag'],item['direction'],item['ti'],item['li'],item['hold']
   log(ev='cycle_start',**item)
   caps=[Cap(tag,k,max(30,int(hold/1000)+25)) for k in ('plain','vlan','observer')]
   if not all(c.ok for c in caps):raise RuntimeError('capture failed to start')
   first=len(pr.events)
   handoff(f'| {tag} | {direction} | {hold} ms | {item.get("phase","exact")} | RUNNING | pending | pending | pending | {SESSION} |')
   pr.send(f'cycle {tag} {direction} {ti} {li} {hold} 1800 {item.get("poll",0)} {item.get("align",0)}')
   end=pr.wait(lambda e:e.get('ev')=='cycle_end' and e.get('tag')==tag,hold/1000+25)
   for c in caps:c.stop()
   paths=[c.collect() for c in caps];caps=[]
   listener=DUT if direction=='A' else PEER
   data=analyze(paths,listener,li,ctl);ev=pr.events[first:]
   data.update(plan=item,events=ev,result=end['result'] if end else 'NO_CYCLE_END')
   resultpath=RAW/(tag+'-result.json');resultpath.write_text(json.dumps(data,indent=1)+'\n')
   w=data['wire'] or {};incs={}
   for e in ev:
    if e.get('ev')=='hive_rule' and e.get('who')==('dut' if direction=='A' else 'peer') and e.get('idx')==li:
     for k,v in e['increments'].items():incs[k]=incs.get(k,0)+v
   mu=(w.get('unlock') or {}).get('counters',{}).get('MU')
   up=next((e for e in ev if e.get('ev')=='si_counters' and e.get('who')==('dut' if direction=='A' else 'peer') and e.get('idx')==li and e.get('counters',{}).get('MU')==mu),{})
   row=f'| {tag} | {direction} | {hold} ms | {item.get("phase","exact")} | {data["result"]}; status {w.get("status")} | {w.get("order")}; {w.get("response_unlock_us")} us | {up.get("lib_conn","unobserved")} | {json.dumps(incs,sort_keys=True)} | {resultpath.name} |'
   h=OUT/'HANDOFF.md';s=h.read_text();lines=s.splitlines();lines=[row if l.startswith('| '+tag+' |') else l for l in lines];h.write_text('\n'.join(lines)+'\n')
   log(ev='cycle_done',tag=tag,result=data['result'],wire_status=w.get('status'),order=w.get('order'),interval_us=w.get('response_unlock_us'),hive_increments=incs,stream_frames=sum(s['count'] for s in data['streams']),gaps=sum(s['gaps'] for s in data['streams']))
   if not end or data['result']!='OK':status=3;break
   if direction=='A' and (w.get('status') not in (None,0) or w.get('order')=='COUNTERS_FIRST'):
    log(ev='STOP',why='DUT response status or order',tag=tag);status=4;break
   if w.get('status') is None:log(ev='STOP',why='missing wire response',tag=tag);status=5;break
 finally:
  for c in caps:
   try:c.stop();c.collect()
   except Exception as ex:log(ev='cleanup_error',error=str(ex))
  pr.quit()
 return status
if __name__=='__main__':sys.exit(main())
