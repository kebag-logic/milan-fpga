#!/usr/bin/env python3
"""Independent clean, absent-stimulus and doubled-counter fault probes."""
import argparse,json,os,pathlib,subprocess,time
p=argparse.ArgumentParser();p.add_argument("--source",type=pathlib.Path,required=True);p.add_argument("--compiler",required=True);a=p.parse_args()
packet=pathlib.Path(__file__).resolve().parents[1];root=packet/"scratch/underrun-probes"
head="62c261c2d1b899a9cf90c901b25b5a85846dfef6"
with (packet/"receipts/probe-setup.log").open("w") as log:
    def setup(cmd): subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,check=True)
    setup(["git","clone","--shared","--no-checkout",str(a.source),str(root)])
    setup(["git","-C",str(root),"checkout","--detach",head])
    for sub in ("protocol-processor","gptp-processor","third_party/verilog-axis"):
        setup(["git","-C",str(root),"-c","protocol.file.allow=always","submodule","update","--init","--reference",str(a.source/sub),"--",sub])
suite=root/"tb/verilator/milan_dp_render";cpp=suite/"sim_tdm8_render.cpp";rtl=root/"hdl/ieee1722/aaf/KL_tdm_render_master.sv"
original_cpp=cpp.read_bytes();original_rtl=rtl.read_bytes()
env=os.environ.copy()
for key in ("MAKEFLAGS","MFLAGS","MAKELEVEL"):env.pop(key,None)
env.update(VERILATOR=a.compiler,VERILATOR_JOBS="4",TMPDIR=str(packet/"scratch"),PYTHONDONTWRITEBYTECODE="1")
cpus=sorted(os.sched_getaffinity(0)); affinity=",".join(map(str,cpus[-4:]))
results=[]
try:
    for name in ("clean","no-burst","double-count"):
        cpp.write_bytes(original_cpp);rtl.write_bytes(original_rtl)
        if name=="no-burst":
            old=b"    tdm_double_rate = true;";assert cpp.read_bytes().count(old)==1
            cpp.write_bytes(cpp.read_bytes().replace(old,b"    tdm_double_rate = false;"))
        if name=="double-count":
            old=b"else unders_b_r <= (&unders_b_r) ? unders_b_r : unders_b_r + 16'd1;"
            assert rtl.read_bytes().count(old)==1
            rtl.write_bytes(rtl.read_bytes().replace(old,old.replace(b"16'd1",b"16'd2")))
        start=time.monotonic()
        with (packet/"receipts"/f"probe-{name}-build.log").open("w") as log:
            r=subprocess.run(["taskset","-c",affinity,"make","-j16","-C",str(suite),"tdm8render-build"],env=env,stdout=log,stderr=subprocess.STDOUT)
        assert r.returncode==0,(name,"build",r.returncode)
        r=subprocess.run(["taskset","-c",affinity,str(suite/"obj_tdm8r/Vmilan_dp_tdm8r"),"--serial-only"],cwd=suite,env=env,capture_output=True,text=True)
        (packet/"receipts"/f"probe-{name}.log").write_text(r.stdout+r.stderr)
        (packet/"receipts"/f"probe-{name}.rc").write_text(str(r.returncode)+"\n")
        failures=[line.strip() for line in r.stdout.splitlines() if line.strip().startswith("[FAIL]")]
        expected=0 if name=="clean" else 1
        assert r.returncode==expected,(name,r.returncode)
        if name=="no-burst":assert len(failures)==1 and "the faster serial clock forced repeated frames" in failures[0],failures
        if name=="double-count":assert len(failures)==1 and "every forced repeat is a counted underrun" in failures[0],failures
        results.append({"probe":name,"mode":"--serial-only","rc":r.returncode,"failures":failures,"seconds":time.monotonic()-start})
        print(json.dumps(results[-1]),flush=True)
finally:
    cpp.write_bytes(original_cpp);rtl.write_bytes(original_rtl)
    (packet/"receipts/probe-results.json").write_text(json.dumps(results,indent=2)+"\n")
subprocess.run(["python3",str(packet/"scripts/verify_tree.py"),str(root)],stdout=(packet/"receipts/probe-tree-restored.json").open("w"),check=True)
