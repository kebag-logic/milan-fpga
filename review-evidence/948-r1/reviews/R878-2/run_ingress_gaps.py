#!/usr/bin/env python3
"""Run the short-frame scoreboards with producer-valid gaps and consumer stalls.
Usage: REVIEW_VERILATOR=/path/to/verilator python3 run_ingress_gaps.py SCRATCH_CLONE
"""
import pathlib,sys,os,subprocess,shlex,concurrent.futures as cf
P=pathlib.Path(__file__).resolve().parent; R=pathlib.Path(sys.argv[1]).resolve(); S=P/"scratch"
RX=R/"tb/verilator/avtp_rxmon"
V=os.environ.get("REVIEW_VERILATOR","$VALIDATION_TOOLS/pinned-verilator-5.050/verilator")
def go(name,target,mdir,src):
 cmd=shlex.split(subprocess.check_output(["make","-n",target,"VERILATOR="+V,mdir+"="+str(S/("obj_"+name))],cwd=RX,text=True).strip())
 for i in range(len(cmd)-1):
  if cmd[i]=="-j":cmd[i+1]="4"
 cmd=[str(src) if x in ["sim_depkt.cpp","sim_fanout.cpp"] else x for x in cmd]
 with (S/(name+"-build.log")).open("w") as f:q=subprocess.run(cmd,cwd=RX,stdout=f,stderr=f)
 assert q.returncode==0
 exe="Vdepkt" if name=="depkt-gaps" else "Vavtp_rxmon_fanout"
 with (P/(name+".log")).open("w") as f:q=subprocess.run([str(S/("obj_"+name)/exe)],cwd=RX,stdout=f,stderr=f)
 (P/(name+".rc")).write_text(str(q.returncode)+"\n")
 assert q.returncode==0
 print(name,"PASS",flush=True)
t=(RX/"sim_depkt.cpp").read_text()
old="        for (size_t b = 0; b < beats; b++) {\n"
assert t.count(old)==1
t=t.replace(old,old+"            d->s_tvalid_i = 0;\n            for (unsigned gap = rng.below(5); gap; --gap) cycle();\n")
f=S/"depkt_gaps.cpp";f.write_text(t)
u=(RX/"sim_fanout.cpp").read_text()
old="            dut->s_tdata_i = d;\n"
assert u.count(old)==1
# Deterministic producer pauses before selected beats, including beat eight.
u=u.replace(old,"            dut->s_tvalid_i = 0;\n            cyc((b * 3 + 1) % 5);\n"+old)
# Keep only the delta-specific deterministic cases; dense overflow depends on line-rate stimulus.
start=u.index("        two_inputs_on_one_stream();");end=u.index("        std::printf",start)
u=u[:start]+"        two_inputs_on_one_stream();\n        a_pdu_off_its_inputs_frame_size_is_discarded_whole();\n        payload_tails_that_are_not_whole_beats();\n        frames_short_of_their_payload();\n        frames_of_eight_to_ten_beats();\n"+u[end:]
g=S/"fanout_gaps.cpp";g.write_text(u)
with cf.ThreadPoolExecutor(max_workers=2) as pool:
 fs=[pool.submit(go,"depkt-gaps","depkt-build","DT_MDIR",f),pool.submit(go,"fanout-gaps","fanout-build","FO_MDIR",g)]
 for f in fs:f.result()
