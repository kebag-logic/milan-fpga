"""Bounded bench controller actions; caller holds the bench lock."""
import sys, struct, json, time, signal, threading
from pathlib import Path
import b2a440_avdecc_ro as ro
D=bytes.fromhex("020000fffe000001"); DM=bytes.fromhex("020000000001")
P=bytes.fromhex("3cc0c60102030000"); PM=bytes.fromhex("3cc0c6010203")
Z=bytes(8)
def emit(role,what,r):
 ro.emit(dict(role=role,what=what,response=r))
def aem(a,role,cmd,payload,what):
 target,mac=(D,DM) if role=="dut" else (P,PM)
 r=a.aem(target,mac,cmd,payload,timeout=.8)
 if cmd==0x29 and r.get("status")=="SUCCESS":
  b=bytes.fromhex(r["payload"]);valid=int.from_bytes(b[4:8],"big");v=struct.unpack(">32I",b[8:136]);r["counters"]={str(i):v[i] for i in range(32) if valid>>i&1};r["valid"]=hex(valid)
 if cmd==0x27 and r.get("status")=="SUCCESS":r["decoded"]=ro.decode_avb_info(r["payload"])
 emit(role,what,r);return r
def state(a,role,kind,i):
 e=D if role=="dut" else P
 r=a.acmp(10,Z,0,e,i,timeout=.8) if kind==5 else a.acmp(4,e,i,Z,0,timeout=.8)
 emit(role,f"state-{kind}-{i}",r);return r
def census(a):
 for role,ni,no in [("dut",2,2),("peer",10,4)]:
  for i in range(ni):state(a,role,5,i)
  for i in range(no):state(a,role,6,i)
  for cmd,payload,what in [(0x17,"00240000","clock"),(7,"00000000","config"),(0x15,"00020000","sample-rate"),(0x27,"00090000","avb")]:aem(a,role,cmd,bytes.fromhex(payload),what)
  for kind,inds in [(5,range(ni)),(6,range(no)),(0x24,[0]),(0xa,range(2 if role=="dut" else 5))]:
   for i in inds:aem(a,role,4,struct.pack(">4H",0,0,kind,i),f"desc-{kind}-{i}")
  for kind,inds in [(9,[0]),(5,range(ni)),(6,range(no)),(0x24,[0])]:
   for i in inds:aem(a,role,0x29,struct.pack(">HH",kind,i),f"counter-{kind}-{i}")
PAIRS=[(D,1,P,8),(P,2,D,1)]
def pair_state(a,t,ti,l,li):
 r=a.acmp(10,Z,0,l,li,timeout=.8);emit("dut" if l==D else "peer",f"state-5-{li}",r);return r
def change_pair(a,mt,pair):
 t,ti,l,li=pair
 r=a.acmp(mt,t,ti,l,li,timeout=4);emit("dut" if l==D else "peer",f"acmp-{mt}",r);return r
def setclock(a,index):
 assert index in (0,1)
 ro.READ_ONLY_AEM[0x16]="SET_CLOCK_SOURCE"
 r=aem(a,"dut",0x16,struct.pack(">4H",0x24,0,index,0),"set-clock")
 assert r.get("status")=="SUCCESS",r
 return aem(a,"dut",0x17,bytes.fromhex("00240000"),"clock")
def snapshot(a):
 for role in ["dut","peer"]:
  aem(a,role,0x27,bytes.fromhex("00090000"),"avb")
  for kind,i in [(9,0),(5,1 if role=="dut" else 8),(6,1 if role=="dut" else 2),(0x24,0)]:
   aem(a,role,0x29,struct.pack(">HH",kind,i),f"counter-{kind}-{i}")
 for pair in PAIRS:pair_state(a,*pair)
def main():
 a=ro.Aecp(sys.argv[1]);mode=sys.argv[2]
 try:
  if mode=="census":census(a)
  elif mode=="snapshot":snapshot(a)
  elif mode=="setup":
   for pair in PAIRS:
    r=pair_state(a,*pair);assert r.get("status")==0 and r.get("conn_count")==0,r
   for pair in PAIRS:
    r=change_pair(a,6,pair);assert r.get("status")==0,r
   setclock(a,1)
   snapshot(a)
  elif mode=="restore":
   setclock(a,0)
   for pair in PAIRS:
    for attempt in range(3):
     r=pair_state(a,*pair)
     if r.get("status")==0 and r.get("conn_count")==0:break
     change_pair(a,8,pair)
    r=pair_state(a,*pair);assert r.get("status")==0 and r.get("conn_count")==0,r
  elif mode=="watch":
   end=time.monotonic()+float(sys.argv[3]);done=threading.Event()
   def carrier_watch():
    prev=None
    while time.monotonic()<end and not done.is_set():
     value=int(Path("/sys/class/net/"+sys.argv[1]+"/carrier").read_text())
     if value!=prev:ro.emit(dict(type="carrier",value=value));prev=value
     done.wait(.1)
   thread=threading.Thread(target=carrier_watch);thread.start()
   try:
    while time.monotonic()<end:
     t=time.monotonic()
     carrier=int(Path("/sys/class/net/"+sys.argv[1]+"/carrier").read_text())
     if carrier:snapshot(a)
     while time.monotonic()<min(t+1,end):
      for fr in ro.frames(a.sock,min(t+1,end,time.monotonic()+.1)):
       e=ro.parse_adp(fr)
       if e:ro.emit(dict(type="adp",**e))
   finally:done.set();thread.join()
  elif mode=="aem":aem(a,sys.argv[3],int(sys.argv[4],0),bytes.fromhex(sys.argv[5]),sys.argv[6])
  elif mode=="states":
   for role in ["dut","peer"]:
    for kind,idx in [(5,0),(5,1 if role=="dut" else 8),(6,0),(6,1 if role=="dut" else 2)]:state(a,role,kind,idx)
 finally:a.sock.close()
if __name__=="__main__":main()
