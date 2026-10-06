"""Role-safe protocol readbacks. Caller owns the action lock."""
import hashlib,json,struct,sys,time
import avdecc_ro as ro
ro.READ_ONLY_AEM.update({0x2b:"GET_AUDIO_MAP",0x08:"SET_STREAM_FORMAT",0x16:"SET_CLOCK_SOURCE"})
mode,iface,peer,mac=sys.argv[1:5]
a=ro.Aecp(iface)
entities={"dut":(bytes.fromhex("020000fffe000001"),bytes.fromhex("020000000001")),"peer":(bytes.fromhex(peer),bytes.fromhex(mac.replace(":","")))}
def request(role,cmd,payload):
 start=time.time_ns();r=a.aem(*entities[role],cmd,payload,timeout=1.5)
 return dict(role=role,command=r["cmd"],sequence=r.get("seq"),status=r["status"],request_ns=start,response_ns=time.time_ns()),bytes.fromhex(r.get("payload",""))
def get(role,cmd,dt,idx):
 row,b=request(role,cmd,struct.pack(">HH",dt,idx));row.update(descriptor_type=dt,descriptor_index=idx);return row,b
def emit(r):print(json.dumps(r,separators=(",",":")),flush=True)
def require(row,b,n):
 if row["status"]!="SUCCESS" or len(b)<n:raise RuntimeError("incomplete "+row["command"]+" "+row["role"])
def snapshot():
 for role in entities:
  row,b=request(role,4,bytes(8));require(row,b,316);cfg=int.from_bytes(b[314:316],"big")
  row,b=request(role,4,struct.pack(">4H",cfg,0,1,cfg));require(row,b,78);d=b[4:];n,off=struct.unpack(">HH",d[70:74]);counts=dict(struct.unpack(">HH",d[off+4*i:off+4*i+4]) for i in range(n));emit(dict(role=role,category="inventory",configuration=cfg,counts=counts))
  for dt in (5,6):
   for idx in range(counts.get(dt,0)):
    row,b=get(role,9,dt,idx);require(row,b,12);row.update(category="format",value=b[4:12].hex());emit(row)
    eid=entities[role][0];r=a.acmp(10 if dt==5 else 4,bytes(8) if dt==5 else eid,0 if dt==5 else idx,eid if dt==5 else bytes(8),idx if dt==5 else 0)
    emit(dict(role=role,category="binding",descriptor_type=dt,descriptor_index=idx,status=r["status"],connections=r.get("conn_count"),observed_ns=time.time_ns()))
  for idx in range(counts.get(36,0)):
   row,b=get(role,0x17,36,idx);require(row,b,8);row.update(category="clock",value=int.from_bytes(b[4:6],"big"));emit(row)
  for dt in (14,15):
   row,b=request(role,0x2b,struct.pack(">4H",dt,0,0,0));require(row,b,12);page,pages,num=struct.unpack(">HHH",b[4:10]);assert page==0 and pages==1 and len(b)==12+8*num
   row.update(category="map",descriptor_type=dt,descriptor_index=0,mapping_count=num,effective_sha256=hashlib.sha256(b).hexdigest());emit(row)
def counters():
 for role,items in (("dut",[(0,0),(9,0),(36,0),(5,0),(5,1),(6,0),(6,1)]),("peer",[(5,0),(5,8)])):
  for dt,idx in items:
   row,b=get(role,0x29,dt,idx)
   if row["status"]=="SUCCESS":
    require(row,b,136);assert struct.unpack(">HH",b[:4])==(dt,idx)
    mask=int.from_bytes(b[4:8],"big");values=list(struct.unpack(">32I",b[8:136]));row.update(valid_mask=mask,counters={str(i):v for i,v in enumerate(values) if mask&(1<<i)},payload=b.hex())
   emit(row)
def timing():
 for role in entities:
  row,b=get(role,0x27,9,0);require(row,b,20)
  row.update(gm_fingerprint=hashlib.sha256(b[4:12]).hexdigest(),pdelay_ns=int.from_bytes(b[12:16],"big"),domain=b[16],as_capable=bool(b[17]&1),flags=b[17]);emit(row)
  row,b=request(role,0x28,bytes(4));require(row,b,4);n=int.from_bytes(b[2:4],"big");assert len(b)==4+8*n
  row.update(path_count=n,path_fingerprint=hashlib.sha256(b[4:]).hexdigest());emit(row)
try:
 if mode=="snapshot":snapshot()
 elif mode=="counters":counters()
 elif mode=="timing":timing()
 elif mode=="setfmt":
  role,idx,fmt=sys.argv[5:];row,b=request(role,8,struct.pack(">HH",5,int(idx))+bytes.fromhex(fmt));emit(row);require(row,b,12);row,b=get(role,9,5,int(idx));require(row,b,12);row["format"]=b[4:12].hex();emit(row);assert row["format"]==fmt
 elif mode=="setclock":
  role,src=sys.argv[5:];row,b=request(role,0x16,struct.pack(">4H",36,0,int(src),0));emit(row);require(row,b,8);row,b=get(role,0x17,36,0);require(row,b,8);row["source"]=int.from_bytes(b[4:6],"big");emit(row);assert row["source"]==int(src)
 else:raise ValueError("unknown operation")
finally:a.sock.close()
