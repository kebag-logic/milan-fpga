#!/usr/bin/env python3
"""Foreground driver: independent chains, at most 16 compiler jobs combined.
Usage: REVIEW_VERILATOR=/path/to/verilator python3 run_focused.py SCRATCH_CLONE
All generated source/build trees are under this packet scratch directory.
"""
import concurrent.futures as cf
import os, pathlib, shlex, subprocess, sys
P=pathlib.Path(__file__).resolve().parent
R=pathlib.Path(sys.argv[1]).resolve()
V=os.environ.get("REVIEW_VERILATOR", "$VALIDATION_TOOLS/pinned-verilator-5.050/verilator")
S=P/"scratch"
RX=R/"tb/verilator/avtp_rxmon"
DP=R/"tb/verilator/milan_dp"
def run(name,cmd,cwd=R,expected=0):
    with (P/(name+".log")).open("w") as f:
        f.write(shlex.join(map(str,cmd))+"\n"); f.flush()
        q=subprocess.run(list(map(str,cmd)),cwd=cwd,stdout=f,stderr=subprocess.STDOUT)
    (P/(name+".rc")).write_text(str(q.returncode)+"\n")
    print(name, q.returncode, flush=True)
    if q.returncode!=expected: raise RuntimeError(name)
def recipe(target,opts,cpp=None):
    cmd=shlex.split(subprocess.check_output(["make","-n",target,"VERILATOR="+V,*opts],cwd=RX,text=True).strip())
    for i in range(len(cmd)-1):
        if cmd[i]=="-j": cmd[i+1]="4"
    if cpp:
        cmd=[str(cpp) if x in ["sim_fanout.cpp","sim_depkt.cpp"] else x for x in cmd]
    return cmd
def receiver():
    out=S/"obj_fanout"
    run("fanout-build",recipe("fanout-build",["FO_MDIR="+str(out)]),RX)
    run("fanout",[out/"Vavtp_rxmon_fanout"],RX)
    # Original 65-octet real-stack probe, now expected to be discarded whole.
    t=(RX/"sim_fanout.cpp").read_text().replace("kPayloadBytes = 192","kPayloadBytes = 65")
    start=t.index("        two_inputs_on_one_stream();")
    end=t.index("        std::printf",start)
    t=t[:start]+"        two_inputs_on_one_stream();\n"+t[end:]
    f=S/"stack_tail.cpp"; f.write_text(t)
    out=S/"obj_stack_tail"
    run("stack-tail-build",recipe("fanout-build",["FO_MDIR="+str(out)],f),RX)
    run("stack-tail",[out/"Vavtp_rxmon_fanout"],RX,1)
def direct():
    for lead in [0,16]:
        out=S/("obj_dt"+str(lead))
        run("depkt-build-"+str(lead),recipe("depkt-build",["DT_MDIR="+str(out),"DT_LEAD="+str(lead)]),RX)
        run("depkt-"+str(lead),[out/"Vdepkt"],RX)
    for name in ["tail","depkt"]:
        out=S/("obj_prior_"+name)
        cmd=[V,"--cc","--exe","--build","-j","4","-Wno-fatal","--top-module","KL_aaf_rx_depacketizer","-GN_STREAMS_P=8","-GPAY_LEAD_CYC_P=16","--Mdir",out,R/"hdl/ieee1722/aaf/KL_aaf_rx_depacketizer.sv",P/("probe_"+name+".cpp")]
        run("prior-"+name+"-build",cmd)
        run("prior-"+name,[out/"VKL_aaf_rx_depacketizer"])
def stop():
    plant=S/"probeB.sv"
    run("probeB-plant",[sys.executable,P/"probeB_make.py",R/"hdl/milan/milan_datapath.sv",plant])
    out=S/"obj_probeB"
    run("probeB-build",["make","-j16","build-nxn8","VERILATOR="+V,"VERILATOR_JOBS=8","NXN8_MDIR="+str(out),"DP_SRC="+str(plant)],DP)
    run("probeB",[out/"Vmilan_dp_nxn8"],DP,1)
    t=(P/"probeB.log").read_text()
    words=["[FAIL] [FAN] input 4 stopped: input 6 receives every PDU (its DEPKT tally)","[FAIL] [FAN] input 6 stopped: input 4 receives every PDU (its DEPKT tally)"]
    assert all(x in t for x in words)
    (P/"probeB-caught.txt").write_text("Shared gate caught by both named checks:\n"+"\n".join(words)+"\n")
with cf.ThreadPoolExecutor(max_workers=3) as pool:
    futures=[pool.submit(f) for f in [receiver,direct,stop]]
    for f in futures: f.result()
print("All focused chains complete")
