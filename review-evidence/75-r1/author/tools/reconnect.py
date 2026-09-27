"""One bounded controller transaction sequence; caller owns the lock."""
import sys,time,json,struct
import a386_controller as c
mode,direction=sys.argv[2:4]
pair=c.PAIRS[1 if direction=="listener" else 0]
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
  r=c.pair_state(a,*pair)
  if r.get("conn_count"):change(8)
  r=c.pair_state(a,*pair);assert r.get("status")==0 and r.get("conn_count")==0,r
 elif mode=="snapshot":c.snapshot(a)
 else:raise RuntimeError("unknown action")
finally:a.sock.close()
