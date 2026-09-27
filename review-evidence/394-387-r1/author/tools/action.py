"""Joined foreground measurements for one locked bench action.
No process is detached. Captures and commands have explicit deadlines.
A cycle changes OUT4 only and returns it ON in the finally block.
"""
import concurrent.futures as cf
from pathlib import Path
import hashlib,json,os,re,shlex,signal,subprocess,sys,termios,time,tty
from console_poll import transact
name,duration,port,controller,interface,tap,tapif,strip=sys.argv[1:]
duration=int(duration);cycle=name.startswith("cycle")
root=Path("/tmp/a375")/name;root.mkdir(parents=True,exist_ok=False)
packet=Path(__file__).resolve().parent.parent
end=time.monotonic()+duration
stop=False;outlet_off=False;last_console=0
results={};events=[]
def event(kind,**kw):
 r=dict(t=time.time(),kind=kind,**kw);events.append(r)
 with (root/"events.jsonl").open("a") as f:f.write(json.dumps(r)+"\n")
 print(json.dumps(r),flush=True)
def run(args,limit,**kw):
 return subprocess.run(["rtk","proxy","timeout",str(limit)+"s",*args],timeout=limit+2,**kw)
def ssh(host,args,limit,**kw):
 return run(["ssh","-o","BatchMode=yes","-o","ConnectTimeout=5","-o","StrictHostKeyChecking=no",host,shlex.join(args)],limit,**kw)
def offset(host,role,tag):
 for i in range(3):
  t0=time.time();r=ssh(host,["timeout","5s","date","+%s.%N"],8,capture_output=True,text=True);t1=time.time()
  if r.returncode:raise RuntimeError("clock read failed: "+role)
  event("clock",role=role,tag=tag,t0=t0,t1=t1,remote=float(r.stdout))
def power(value):
 global outlet_off
 assert value in ("on","off")
 if value=="off":outlet_off=True
 event("power-command",value=value,outlet=4)
 r=ssh(strip,["timeout","8s","powerstrip",value,"4"],12,capture_output=True,text=True)
 event("power-result",value=value,rc=r.returncode,output=r.stdout+r.stderr)
 if r.returncode:raise RuntimeError("OUT4 command failed")
 if value=="on":outlet_off=False
 return time.monotonic()
def status(tag):
 r=ssh(strip,["timeout","8s","powerstrip","status"],12,capture_output=True,text=True)
 event("outlets",tag=tag,rc=r.returncode,output=r.stdout)
 assert r.returncode==0
 parsed=dict(re.findall(r"OUT([0-6])\s+(ON|OFF)",r.stdout))
 assert len(parsed)==7 and all(v=="ON" for k,v in parsed.items() if k!="4")
 return parsed
def capture(host,iface,role):
 with (root/(role+".pcap")).open("wb") as out:
  r=ssh(host,["sudo","-n","timeout","-s","INT",str(duration)+"s","tcpdump","-U","-n","-i",iface,"-w","-"],duration+8,stdout=out,stderr=subprocess.PIPE)
 log=r.stderr.decode(errors="replace").replace(iface,"<capture-interface>").replace(host,"<capture-host>")
 (root/(role+"-capture.txt")).write_text(log)
 assert r.returncode in (0,124),r.returncode
 assert (root/(role+".pcap")).stat().st_size>24
 return r.returncode
def watch():
 with (root/"controller.jsonl").open("wb") as out:
  r=ssh(controller,["sudo","-n","timeout",str(duration+3)+"s","python3","-B","/tmp/a375_controller.py",interface,"watch",str(duration)],duration+8,stdout=out,stderr=subprocess.PIPE)
 (root/"controller-errors.txt").write_bytes(r.stderr)
 assert r.returncode==0,r.returncode
 return r.returncode
def console():
 global last_console
 fd=os.open(port,os.O_RDWR|os.O_NOCTTY|os.O_NONBLOCK);saved=termios.tcgetattr(fd)
 try:
  tty.setraw(fd);attrs=termios.tcgetattr(fd);attrs[4]=attrs[5]=termios.B115200;termios.tcsetattr(fd,termios.TCSANOW,attrs)
  cmds=["milan_status","mem_read 0x900008f8 4","mem_read 0x90000720 4","mem_read 0x90000110 4","mem_read 0x90000750 4","mem_read 0x90000764 4","mem_read 0x90000780 4"]
  with (root/"console.jsonl").open("w",buffering=1) as out:
   while time.monotonic()<end and not stop:
    start=time.monotonic()
    for cmd in cmds:
     t0,t1,raw=transact(fd,cmd)
     out.write(json.dumps(dict(t=t0,end=t1,cmd=cmd,raw=raw))+"\n")
     assert "litex" in raw,"console prompt missing"
     if cmd=="milan_status":last_console=time.monotonic()
    time.sleep(max(0,min(.25-(time.monotonic()-start),end-time.monotonic())))
 finally:termios.tcsetattr(fd,termios.TCSANOW,saved);os.close(fd)
 return 0
def stopping(sig,frame):
 global stop
 stop=True
signal.signal(signal.SIGTERM,stopping);signal.signal(signal.SIGINT,stopping)
try:
 for host,role in [(controller,"controller"),(tap,"tap"),(strip,"power")]:offset(host,role,"before")
 initial=status("before")
 assert initial["4"]=="ON"
 end=time.monotonic()+duration
 with cf.ThreadPoolExecutor(max_workers=4) as pool:
  futures={pool.submit(console):"console",pool.submit(watch):"controller",pool.submit(capture,tap,tapif,"tap"):"tap",pool.submit(capture,controller,interface,"controller-wire"):"controller-wire"}
  if cycle:
   time.sleep(10)
   assert time.monotonic()-last_console<1,"console preflight failed"
   assert all(not f.done() for f in futures),"measurement exited before power action"
   assert (root/"tap.pcap").stat().st_size>24,"tap not recording"
   try:
    power("off");status("off")
    start=time.monotonic()
    while time.monotonic()-start<20 and not stop:
     if time.monotonic()-last_console>2:raise RuntimeError("DUT console lost during OUT4 proof")
     time.sleep(.1)
   finally:
    if outlet_off:power("on")
   status("on")
  for f in cf.as_completed(futures):results[futures[f]]=f.result()
 if stop:raise RuntimeError("action interrupted")
finally:
 if outlet_off:
  for attempt in range(3):
   try:power("on");break
   except Exception:event("restore-retry",attempt=attempt)
 event("finished",results=results,outlet_off=outlet_off)
 (root/"results.json").write_text(json.dumps(results,indent=2)+"\n")
for host,role in [(controller,"controller"),(tap,"tap"),(strip,"power")]:offset(host,role,"after")
for f in root.iterdir():
 if f.is_file() and f.stat().st_size<=200000:
  dest=packet/name;dest.mkdir(exist_ok=True);(dest/f.name).write_bytes(f.read_bytes())
print("ACTION_COMPLETE "+name,flush=True)
