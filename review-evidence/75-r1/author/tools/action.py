"""One locked foreground capture and controller action, with joined children."""
import concurrent.futures as cf
import hashlib,json,os,shlex,signal,struct,subprocess,sys,threading,time
from pathlib import Path
from wire_summary import decode
name,mode,direction,port,controller,interface,tap,tapif=sys.argv[1:]
packet=Path(__file__).resolve().parent.parent
root=Path('/tmp/a386')/name;root.mkdir(parents=True,exist_ok=False)
dest=packet/name;dest.mkdir(exist_ok=False)
events=[];wire=[];errors=[];first=None;capture=None
sid='3cc0c60102034000' if direction=='listener' else '0200000000010001'
wireport=2 if direction=='listener' else 3
stopping=False

def event(kind,**kw):
 r=dict(t=time.time(),kind=kind,**kw);events.append(r)
 with (dest/'events.jsonl').open('a') as f:f.write(json.dumps(r)+'\n')
 print(json.dumps(r),flush=True)
def run(args,limit,**kwargs):
 return subprocess.run(['rtk','proxy','timeout',str(limit)+'s',*args],timeout=limit+2,**kwargs)
def sshargs(host,args):
 return ['ssh','-o','BatchMode=yes','-o','ConnectTimeout=5',host,shlex.join(args)]
def controller_action(which):
 r=run(sshargs(controller,['sudo','-n','timeout','12s','python3','-B','/tmp/a386_reconnect.py',interface,which,direction]),15,capture_output=True,text=True)
 (dest/(which+'.jsonl')).write_text(r.stdout)
 (dest/(which+'-errors.txt')).write_text(r.stderr.replace(controller,'<controller-host>'))
 event('controller',action=which,rc=r.returncode)
 assert r.returncode==0,'controller action failed'
 return [json.loads(s) for s in r.stdout.splitlines()]
def console(which):
 cmds=['milan_status','mem_read 0x90000650 4','mem_read 0x9000069c 4','mem_read 0x900006b0 4','mem_read 0x90000930 4','mem_read 0x90000720 4']
 r=run(['python3',str(packet/'tools/console_read.py'),port,str(dest/('console-'+which+'.txt')),*cmds],10,capture_output=True,text=True)
 assert r.returncode==0,r.stderr
 text=(dest/('console-'+which+'.txt')).read_text()
 assert 'SYNC=1 ASCAPABLE=1 TU=0' in text,'DUT health changed'
def read_exact(stream,n):
 b=bytearray()
 while len(b)<n:
  v=stream.read(n-len(b))
  if not v:break
  b.extend(v)
 return bytes(b)
def reader():
 global first
 try:
  with (root/'tap.pcap').open('wb') as out:
   head=read_exact(capture.stdout,24);out.write(head);out.flush()
   assert len(head)==24 and head[:4] in (b'\xd4\xc3\xb2\xa1',b'\x4d\x3c\xb2\xa1'),'bad pcap header'
   nano=head[:4]==b'\x4d\x3c\xb2\xa1'
   while True:
    h=read_exact(capture.stdout,16)
    if not h:break
    assert len(h)==16,'truncated record'
    sec,frac,n,orig=struct.unpack('<4I',h);pkt=read_exact(capture.stdout,n)
    assert len(pkt)==n,'truncated frame'
    out.write(h+pkt);out.flush()
    if len(pkt)<42:continue
    tag,_,wp=struct.unpack('<3I',pkt[:12])
    if tag!=6 or wp not in (2,3):continue
    host=sec*10**9+frac*(1 if nano else 1000);lo=struct.unpack('<I',pkt[16:20])[0]
    if first is None:first=(host,lo)
    ns=lo-first[1]+round(((host-first[0])-(lo-first[1]))/(1<<32))*(1<<32)
    fr=pkt[28:];et=int.from_bytes(fr[12:14],'big');o=14;vlan=None
    if et==0x8100:
     tci=int.from_bytes(fr[14:16],'big');vlan=(tci>>13,tci&4095);et=int.from_bytes(fr[16:18],'big');o=18
    pl=fr[o:]
    r=dict(ns=ns,host_ns=host,port=wp,et=et,src=fr[6:12].hex(),seen=time.monotonic())
    if et==0x22f0 and len(pl)>=12:
     r['sub']=pl[0]
     if pl[0]==0xfc and len(pl)>=56:
      r.update(mt=pl[1]&15,status=pl[2]>>3,seq=int.from_bytes(pl[48:50],'big'),controller=pl[12:20].hex(),talker=pl[20:28].hex(),listener=pl[28:36].hex(),tuid=int.from_bytes(pl[36:38],'big'),luid=int.from_bytes(pl[38:40],'big'))
     if pl[0]==4:
      r.update(sid=pl[4:12].hex(),valid=(len(pl)>=28 and pl[1]&0xf0==0x80 and pl[3]==1 and int.from_bytes(pl[12:16],'big')==48000 and pl[16:20]==bytes.fromhex('00080060') and vlan==(3,2)))
    wire.append(r)
 except Exception as e:errors.append(str(e))
def stop_capture():
 if capture is None:return
 if capture.poll() is None:
  try:capture.stdin.write(b'stop\n');capture.stdin.flush()
  except BrokenPipeError:pass
 capture.wait(timeout=8)
 thread.join(timeout=3)
 assert not thread.is_alive(),'capture reader did not exit'
 capture.stdin.close();capture.stdout.close()
def signal_stop(signum,frame):
 global stopping
 stopping=True
signal.signal(signal.SIGTERM,signal_stop);signal.signal(signal.SIGINT,signal_stop)
result=dict(name=name,mode=mode,direction=direction,stream_id=sid,status='INCOMPLETE')
try:
 console('before');controller_action('snapshot');(dest/'snapshot-before.jsonl').write_text((dest/'snapshot.jsonl').read_text())
 err=(dest/'capture.txt').open('wb')
 args=sshargs(tap,['sudo','-n','timeout','-k','3s','45s','python3','-B','/tmp/a386_capture.py',tapif,'40'])
 capture=subprocess.Popen(['rtk','proxy','timeout','-k','3s','49s',*args],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=err)
 thread=threading.Thread(target=reader);thread.start()
 end=time.monotonic()+3
 while time.monotonic()<end:
  assert not errors,errors
  if stopping:raise RuntimeError('interrupted')
  time.sleep(.1)
 assert wire,'no tapped frames'
 if mode=='baseline':time.sleep(2)
 else:
  if mode=='cycle':
   assert any(r.get('valid') and r.get('sid')==sid and r['port']==wireport and time.monotonic()-r['seen']<1 for r in wire),'stream not flowing before cycle'
  rows=controller_action(mode)
  if mode in ('bind','cycle'):
   tx=next(r for r in rows if r.get('kind')=='transaction' and r['mt']==6)
   seq=tx['seq'];result['seq']=seq
   end=time.monotonic()+30
   seen_first=None
   while time.monotonic()<end:
    assert not errors,errors
    if stopping:raise RuntimeError('interrupted')
    ack=next((r for r in wire if r.get('mt')==7 and r.get('seq')==seq and r.get('controller')==tx['response']['controller'] and r.get('status')==0),None)
    av=next((r for r in wire if ack and r.get('valid') and r.get('sid')==sid and r['port']==wireport and r['ns']>=ack['ns']),None)
    if av and seen_first is None:seen_first=time.monotonic()
    if seen_first is not None and time.monotonic()-seen_first>=3:break
    time.sleep(.05)
   result['response_ns']=ack['ns'] if ack else None
   result['first_avtp_ns']=av['ns'] if av else None
   result['latency_s']=(av['ns']-ack['ns'])/1e9 if ack and av else None
   result['status']='PASS' if result['latency_s'] is not None and result['latency_s']<1 else 'FAIL'
   result['observation_s']=(wire[-1]['ns']-ack['ns'])/1e9 if ack else None
   assert ack,'successful response absent from tap'
   if mode=='cycle':
    dis=next(r for r in rows if r.get('kind')=='transaction' and r['mt']==8)
    dr=next(r for r in wire if r.get('mt')==9 and r.get('seq')==dis['seq'] and r.get('controller')==dis['response']['controller'])
    cc=next(r for r in wire if r.get('mt')==6 and r.get('seq')==seq and r.get('controller')==tx['response']['controller'])
    result['disconnect_response_ns']=dr['ns'];result['connect_command_ns']=cc['ns']
    result['disconnect_hold_s']=(cc['ns']-dr['ns'])/1e9
    result['frames_last_half_second_disconnected']=sum(r.get('valid',False) and r.get('sid')==sid and cc['ns']-500000000<r['ns']<cc['ns'] for r in wire)
  else:time.sleep(3);result['status']='DONE'
 console('after')
 # A distinct suffix preserves both counter endpoints.
 rows=controller_action('snapshot');(dest/'snapshot-after.jsonl').write_text((dest/'snapshot.jsonl').read_text())
 if mode=='baseline':result['status']='DONE'
finally:
 try:stop_capture()
 finally:
  if 'err' in globals():err.close()
  result['capture_rc']=capture.returncode if capture else None;result['errors']=errors
  (dest/'result.json').write_text(json.dumps(result,indent=2)+'\n')
  if (root/'tap.pcap').exists():
   b=(root/'tap.pcap').read_bytes()
   (dest/'raw-artifacts.json').write_text(json.dumps([dict(path=str(root/'tap.pcap'),size=len(b),sha256=hashlib.sha256(b).hexdigest())],indent=2)+'\n')
  if mode=='cycle':
   with (packet/'HANDOFF.md').open('a') as f:
    f.write('\n| '+direction+' | '+name+' | '+str(result.get('disconnect_response_ns'))+' | '+str(result.get('response_ns'))+' | '+str(result.get('first_avtp_ns'))+' | '+str(result.get('latency_s'))+' | pending analysis | '+name+'/tap.pcap | '+result['status']+' |\n')
 event('complete',**result)
assert not errors,errors
assert result['capture_rc']==0,result
