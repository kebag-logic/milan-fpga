"""One bounded controller transaction sequence for lane B2; caller owns the lock.

Derived from the #75 reconnect.py (import renamed; unbind and bind report their
transactions like cycle does). Only the DUT-talker pair is used:
DUT Stream Output 1 -> reference peer Stream Input 8.
usage: b2_reconnect.py <iface> cycle|bind|unbind|snapshot|states talker
"""
import sys,time,json,struct
import b2a440_controller as c
mode,direction=sys.argv[2:4]
assert direction=="talker"
pair=c.PAIRS[0]
a=c.ro.Aecp(sys.argv[1])
def change(mt):
 start=time.time();r=c.change_pair(a,mt,pair)
 c.ro.emit(dict(kind="transaction",mt=mt,seq=a.seq,start=start,end=time.time(),response=r))
 assert r.get("status")==0,r
 return r
try:
 if mode=="cycle":
  r=c.pair_state(a,*pair);assert r.get("status")==0 and r.get("conn_count")==1,r
  change(8);time.sleep(2);change(6)
 elif mode=="bind":
  r=c.pair_state(a,*pair);assert r.get("status")==0 and r.get("conn_count")==0,r
  change(6)
 elif mode=="unbind":
  r=c.pair_state(a,*pair);assert r.get("status")==0 and r.get("conn_count")==1,r
  change(8)
  r=c.pair_state(a,*pair);assert r.get("status")==0 and r.get("conn_count")==0,r
 elif mode=="snapshot":c.snapshot(a)
 elif mode=="states":
  for p in c.PAIRS:c.pair_state(a,*p)
 else:raise RuntimeError("unknown action")
finally:a.sock.close()
