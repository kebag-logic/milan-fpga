"""Bounded bench controller actions for lane B14 item 3; caller holds the bench lock.

Lane B2's b2_controller.py (sha256 in ORIGIN-B2.sha256), changed only as this lane's as-found
state requires:
  * the peer's entity ID and MAC are read from peer.txt beside this file (private, staged on the
    controller host only), so this file names neither;
  * setup: the peer's clock domain is set to INTERNAL when found following an input stream (B2 ran
    with it at INTERNAL; as found it follows the DUT's CRF, which with the DUT following the peer's
    CRF would be a clock loop), and B2's first pair (the DUT's Stream Output 1 to the peer's Stream
    Input 8) is kept when found bound to that talker instead of asserting it unbound; the binding
    rule is applied before each bind (read both formats; on a difference set the LISTENER's to
    the talker's and read it back);
  * restore: the DUT's clock source 0, B2's second pair unbound, the first pair left bound as found
    (re-bound if a cycle left it unbound), the peer's clock source restored, each read back.
The census, snapshot, states, watch and aem modes are B2's.
"""
import sys, struct, json, time, signal, threading
from pathlib import Path
import avdecc_ro as ro
D=bytes.fromhex("020000fffe000001"); DM=bytes.fromhex("020000000001")
_peer=(Path(__file__).resolve().parent/"peer.txt").read_text().split()
P=bytes.fromhex(_peer[0]); PM=bytes.fromhex(_peer[1].replace(":",""))
Z=bytes(8)
ASFOUND=Path(__file__).resolve().parent/"item3-asfound.json"
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
def clock_of(a,role):
 r=aem(a,role,0x17,bytes.fromhex("00240000"),"clock")
 return int(r["payload"][8:12],16) if r.get("status")=="SUCCESS" else None
def setclock(a,index,role="dut"):
 assert index in (0,1)
 ro.READ_ONLY_AEM[0x16]="SET_CLOCK_SOURCE"
 r=aem(a,role,0x16,struct.pack(">4H",0x24,0,index,0),"set-clock")
 assert r.get("status")=="SUCCESS",r
 return aem(a,role,0x17,bytes.fromhex("00240000"),"clock")
def fmt(a,role,kind,i):
 r=aem(a,role,0x09,struct.pack(">HH",kind,i),f"format-{kind}-{i}")
 return r["payload"][8:24] if r.get("status")=="SUCCESS" else None
def binding_rule(a,pair):
 t,ti,l,li=pair
 tr,lr=("dut" if t==D else "peer"),("dut" if l==D else "peer")
 tf,lf=fmt(a,tr,6,ti),fmt(a,lr,5,li)
 assert tf and lf,"format read failed"
 rec=dict(kind="format-check",talker=f"{tr}-out-{ti}",listener=f"{lr}-in-{li}",talker_fmt=tf,listener_fmt=lf,set=False)
 if tf!=lf:
  ro.READ_ONLY_AEM[0x08]="SET_STREAM_FORMAT"
  aem(a,lr,0x08,struct.pack(">HH",5,li)+bytes.fromhex(tf),"set-format")
  rec.update(set=True,listener_after=fmt(a,lr,5,li))
  assert rec["listener_after"]==tf,"STOP: the listener did not take the talker's format"
 ro.emit(rec)
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
   assert not ASFOUND.exists(),"setup already recorded"
   r0=pair_state(a,*PAIRS[0]);r1=pair_state(a,*PAIRS[1])
   found=dict(peer_clock=clock_of(a,"peer"),dut_clock=clock_of(a,"dut"),pair0=dict(conn_count=r0.get("conn_count"),talker_uid=r0.get("talker_uid"),flags=r0.get("flags"),talker_is_dut=r0.get("talker")==D.hex()),pair1_conn=r1.get("conn_count"))
   ro.emit(dict(kind="as-found",**found))
   assert r1.get("status")==0 and r1.get("conn_count")==0,r1
   assert found["dut_clock"]==0,found
   assert r0.get("status")==0 and (r0.get("conn_count")==0 or (found["pair0"]["talker_is_dut"] and r0.get("talker_uid")==1)),r0
   ASFOUND.write_text(json.dumps(found)+"\n")
   if found["peer_clock"]!=0:setclock(a,0,"peer")
   if r0.get("conn_count")==0:
    binding_rule(a,PAIRS[0]);r=change_pair(a,6,PAIRS[0]);assert r.get("status")==0,r
   else:ro.emit(dict(kind="pair-kept",pair=0))
   binding_rule(a,PAIRS[1]);r=change_pair(a,6,PAIRS[1]);assert r.get("status")==0,r
   setclock(a,1)
   snapshot(a)
  elif mode=="restore":
   found=json.loads(ASFOUND.read_text())
   setclock(a,0)
   for attempt in range(3):
    r=pair_state(a,*PAIRS[1])
    if r.get("status")==0 and r.get("conn_count")==0:break
    change_pair(a,8,PAIRS[1])
   r=pair_state(a,*PAIRS[1]);assert r.get("status")==0 and r.get("conn_count")==0,r
   r=pair_state(a,*PAIRS[0])
   if found["pair0"]["conn_count"] and not r.get("conn_count"):
    binding_rule(a,PAIRS[0]);change_pair(a,6,PAIRS[0]);r=pair_state(a,*PAIRS[0])
   if found["peer_clock"]!=0:setclock(a,found["peer_clock"],"peer")
   final=dict(peer_clock=clock_of(a,"peer"),dut_clock=clock_of(a,"dut"),pair0=dict(conn_count=r.get("conn_count"),talker_uid=r.get("talker_uid"),flags=r.get("flags")),pair1_conn=pair_state(a,*PAIRS[1]).get("conn_count"))
   ro.emit(dict(kind="restore-compare",as_found=found,final=final))
   ASFOUND.rename(ASFOUND.with_name("item3-asfound-restored.json"))
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
