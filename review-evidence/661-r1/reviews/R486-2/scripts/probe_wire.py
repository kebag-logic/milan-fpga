#!/usr/bin/env python3
"""Independent wire vectors and three disposable exemption mutations."""
import argparse, json, os, shutil, struct, subprocess, sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("source",type=Path);p.add_argument("scratch",type=Path);p.add_argument("receipts",type=Path);a=p.parse_args()
sys.path.insert(0,str(a.source/"tb/tools"))
from avtp_wire_truth_checks import WireTruth

def frame(kind,index,eid=0x020000FFFE000002):
    pdu=bytearray(68);pdu[0]=0xfa;pdu[1]=0x80|kind
    struct.pack_into(">H",pdu,2,(31<<11)|56)
    struct.pack_into(">Q",pdu,4,eid);struct.pack_into(">I",pdu,36,index)
    return bytes.fromhex("91e0f001000002000000000222f0")+pdu
cases=[("complete-cycle",[(0,3),(0,4),(1,5),(0,0),(0,1)],"PASS"),
       ("depart-zero",[(1,0),(0,0),(0,1)],"PASS"),
       ("repeat-after-reset",[(1,5),(0,0),(0,0)],"FAIL"),
       ("nonzero-after-depart",[(0,4),(1,5),(0,5)],"FAIL"),
       ("ordinary-repeat",[(0,4),(0,4)],"FAIL"),
       ("wrap",[(0,0xffffffff),(0,0),(0,1)],"PASS"),
       ("repeated-cycles",[(1,0),(0,0),(0,1),(1,2),(0,0),(0,1)],"PASS")]
for label,seq,want in cases:
    wt=WireTruth()
    for kind,index in seq:wt.feed(0.0,frame(kind,index))
    v=[v for v in wt.check_adp_frame_rule() if "available-index" in v.check][0]
    assert v.verdict==want,(label,v)
    print(json.dumps({"case":label,"expected":want,"observed":v.verdict,"detail":v.detail}),flush=True)
wt=WireTruth()
for kind,index,eid in [(1,0,1),(0,4,2),(0,0,1),(0,4,2),(0,1,1)]:wt.feed(0.0,frame(kind,index,eid))
verdicts={v.check:v.verdict for v in wt.check_adp_frame_rule() if "available-index" in v.check}
assert sorted(verdicts.values())==["FAIL","PASS"],verdicts
print(json.dumps({"case":"entity-isolation","verdicts":verdicts}),flush=True)
anchor="if idx[i - 1][0] == ADP_ENTITY_DEPARTING\n                      and idx[i][1] == 0"
mutants={"any-value-after-depart":"if idx[i - 1][0] == ADP_ENTITY_DEPARTING",
         "any-zero":"if idx[i][1] == 0",
         "all-later-zero":"if any(t == ADP_ENTITY_DEPARTING for t, _ in idx[:i])\n                      and idx[i][1] == 0"}
runner="import unittest; from avtp_wire_truth_selftest import _ControlPlaneArms; C=type(\"ExemptionControl\",(_ControlPlaneArms,unittest.TestCase),{}); r=unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite([C(\"test_available_index_resets_after_departing\")])); raise SystemExit(not r.wasSuccessful())"
for label,replacement in [("control",None),*mutants.items()]:
    tree=a.scratch/label;shutil.copytree(a.source/"tb/tools",tree,ignore=shutil.ignore_patterns("__pycache__"),dirs_exist_ok=True)
    target=tree/"avtp_wire_truth_checks.py";text=target.read_text();assert text.count(anchor)==1
    if replacement:target.write_text(text.replace(anchor,replacement))
    r=subprocess.run([sys.executable,"-B","-c",runner],cwd=tree,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    (a.receipts/f"wire-{label}.log").write_text(r.stdout)
    (a.receipts/f"wire-{label}.rc").write_text(str(r.returncode)+"\n")
    if replacement:assert r.returncode==1 and "AssertionError" in r.stdout and "FAILED (failures=1)" in r.stdout,(label,r.stdout)
    else:assert r.returncode==0,r.stdout
    print(f"{label}: rc={r.returncode}; "+("killed by the committed four-arm test" if replacement else "committed four-arm test passes"),flush=True)
