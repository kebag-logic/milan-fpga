import pathlib,sys,types
root=pathlib.Path(sys.argv[1]).resolve()
sys.path.insert(0,str(root/"tb/verilator/ctrl_service_budget"))
import declaring_outputs as d,record_classes as r
for name,ok,detail in r.checks():
 print("PASS" if ok else "FAIL",name,detail)
 assert ok,name
# Independently delimit entries against record and retry spans at unequal clock rates.
# Only the entry at 110 is inside the first record (100..120 system cycles).
f=bytearray(90); f[14]=0xfb;f[15]=1;f[36:38]=(15).to_bytes(2,"big");f[38:40]=(6).to_bytes(2,"big")
log=types.SimpleNamespace(traced=[("SPAN","100","0","10","aecp_mbx:frame"),("SPAN","200","0","10","ctrl_loop:round_of")],entries=[(99,d.ENTRY),(110,d.ENTRY),(121,d.ENTRY),(210,d.ENTRY)],tx=[(115,4,0,bytes(f))])
assert d.records(log,200,100,4)==[(15,6,0,1)]
assert d.rounds_completing(log,200,100)==1
print("PASS independent record/retry span containment at 2:1 system/CPU clock ratio")
for status in (0,3,11):
 assert not d.record_findings("probe",[(14,6,status,1)])
 assert d.record_findings("probe",[(14,6,status,0)])
assert d.record_findings("probe",[(0x2d,15,0,1)])
print("PASS independent answered/refused/no-completion/brief-completion controls")
print("RESULT: PASS")
