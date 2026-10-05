#!/usr/bin/env python3
"""Check the merge, source identity, and the public area table arithmetic."""
import argparse,hashlib,json,pathlib,subprocess
p=argparse.ArgumentParser();p.add_argument("--repo",type=pathlib.Path,required=True);p.add_argument("--packet",type=pathlib.Path,required=True);p.add_argument("--simulator",required=True);a=p.parse_args()
root=a.repo.resolve();packet=a.packet.resolve();scratch=packet/"scratch/identity";scratch.mkdir(exist_ok=True)
def git(*args):return subprocess.check_output(["git","-C",str(root),*args])
head="79571006b803a4ab4af65358f0d87bc3af73180e";base="054d01c79e59c3f80454ad9cdefd8e914b540bb4";c11="21c6f709";pre="e3c9f0b5"
print("HEAD",git("rev-parse","HEAD").decode().strip());print("TREE",git("rev-parse","HEAD^{tree}").decode().strip());print("PARENTS",git("show","-s","--format=%P",head).decode().strip())
assert git("rev-parse","HEAD").decode().strip()==head
assert git("rev-parse","HEAD^{tree}").decode().strip()=="be060640b23bb505b75debc192d7d36505fbe5dd"
for label,pairs in (("issue delta",((base,pre),(c11,head))),("C11 delta",((base,c11),(pre,head)))):
 ids=[subprocess.check_output(["git","patch-id","--stable"],input=git("diff",left,right)).decode().split()[0] for left,right in pairs]
 print(label,ids);assert ids[0]==ids[1]
sv=["hdl/packet_engine/KL_pp_side_port.sv","hdl/packet_engine/KL_pp_trace_ring.sv","hdl/packet_engine/KL_pp_tx_slots.sv"]
for path in sv+["tb/tx_slots/sim_main.cpp"]:
 outputs=[]
 for rev in (pre,head):
  f=scratch/(rev+"-"+pathlib.Path(path).name);f.write_bytes(git("show",rev+":"+path))
  cmd=[a.simulator,"-E","-P",str(f)] if path.endswith(".sv") else ["gcc","-fpreprocessed","-dD","-E","-P",str(f)]
  outputs.append(subprocess.check_output(cmd))
 assert outputs[0]==outputs[1],path
 print("C11 comment-stripped identical",path,hashlib.sha256(outputs[0]).hexdigest())
assert git("show",base+":hdl/aecp/KL_aecp_notify.sv")==git("show","5343cd7:hdl/aecp/KL_aecp_notify.sv")
print("red-first commit notify RTL equals source base")
# The table contains every changed direct child plus the own-logic row.
rows=[("u_notify",-1,-3),("u_tx_slots",121,0),("u_timer",44,0),("u_srp",30,0),("u_dispatch",19,0),("u_originator",14,0),("u_tx_arbiter",6,0),("u_listener",2,0),("u_prng",2,0),("u_aecp",-5,0),("u_talker",-5,0),("u_adp",-4,0),("u_nvm_shadow",-1,0),("u_ca_builder",-8,0),("u_trace",-10,0),("u_maap",-15,0),("u_rx_validator",-16,0),("u_scoreboard",-17,0),("u_normalizer",-27,0),("u_pp own",-79,-1)]
assert tuple(sum(row[i] for row in rows) for i in (1,2))==(50,-4)
print("public u_pp rows total +50 LUT / -4 FF; wrapper own 0 LUT / -2 FF; whole +50 LUT / -6 FF")
print("changed row -1 LUT / -3 FF; all unchanged rows together +51 LUT / -3 FF including wrapper own")
print("standalone changed module: 2471-2474 = -3 LUT; 1282-1280 = +2 FF")
print("Area arithmetic only; raw synthesis hierarchy is not distributed in the public evidence snapshot.")
# Full tracked-byte, mode and index audit; do not rely only on status/filter semantics.
entries=git("ls-tree","-rz",head).split(b"\0");n=0;links=[]
for entry in entries:
 if not entry:continue
 meta,path=entry.split(b"\t",1);mode,typ,oid=meta.decode().split();path=path.decode();f=root/path
 if mode=="160000":links.append((path,oid));continue
 data=f.readlink().as_posix().encode() if mode=="120000" else f.read_bytes()
 actual=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest();assert actual==oid,path
 if mode in ("100644","100755"):assert bool(f.stat().st_mode & 0o111)==(mode=="100755"),path
 n+=1
assert git("write-tree")==git("rev-parse",head+"^{tree}")
assert not git("status","--porcelain","--untracked-files=all")
print("TRACKED_BLOBS_MODES_OK",n,"INDEX_TREE_OK","SUBMODULE_GITLINKS",json.dumps(links))
