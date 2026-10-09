#!/usr/bin/env python3
"""Epoch-only clean leg at head, then with only the #657 boot dwell removed; tree restored after."""
import argparse,json,os,pathlib,re,subprocess,time
p=argparse.ArgumentParser();p.add_argument("--tree",type=pathlib.Path,required=True);p.add_argument("--compiler",required=True);p.add_argument("--cpus",default="0,1");a=p.parse_args()
packet=pathlib.Path(__file__).resolve().parents[1];root=a.tree.resolve()
head="62c261c2d1b899a9cf90c901b25b5a85846dfef6"
assert subprocess.check_output(["git","-C",str(root),"rev-parse","HEAD"],text=True).strip()==head
assert subprocess.check_output(["git","-C",str(root),"status","--porcelain"],text=True)==""
suite=root/"tb/verilator/milan_dp_render";cpp=suite/"sim_tdm8_render.cpp";original=cpp.read_bytes()
env=os.environ.copy()
for key in ("MAKEFLAGS","MFLAGS","MAKELEVEL"):env.pop(key,None)
env.update(VERILATOR=a.compiler,VERILATOR_JOBS="2",TMPDIR=str(packet/"scratch"),PYTHONDONTWRITEBYTECODE="1")
results=[]
try:
    for name in ("head","no-dwell"):
        cpp.write_bytes(original)
        if name=="no-dwell":
            old=b"    if (epoch_only) run_fed(kBootPullInCycles);\n";assert original.count(old)==1
            cpp.write_bytes(original.replace(old,b""))
        start=time.monotonic()
        with (packet/"receipts"/f"epoch-{name}-build.log").open("w") as log:
            r=subprocess.run(["taskset","-c",a.cpus,"make","-j2","-C",str(suite),"tdm8render-build"],env=env,stdout=log,stderr=subprocess.STDOUT)
        assert r.returncode==0,(name,"build",r.returncode)
        r=subprocess.run(["taskset","-c",a.cpus,str(suite/"obj_tdm8r/Vmilan_dp_tdm8r"),"--epoch-only"],cwd=suite,env=env,capture_output=True,text=True)
        (packet/"receipts"/f"epoch-{name}.log").write_text(r.stdout+r.stderr)
        lines=r.stdout.splitlines()
        results.append({"probe":name,"mode":"--epoch-only","rc":r.returncode,
            "pass_lines":sum(l.strip().startswith("[PASS]") for l in lines),
            "fail_lines":[l.strip() for l in lines if l.strip().startswith("[FAIL]")],
            "summary":[l.strip() for l in lines if re.search(r"checks|passed|failed",l,re.I)][-3:],
            "seconds":time.monotonic()-start})
        print(json.dumps(results[-1]),flush=True)
finally:
    cpp.write_bytes(original)
    (packet/"receipts/epoch-probe-results.json").write_text(json.dumps(results,indent=2)+"\n")
subprocess.run(["python3",str(packet/"scripts/verify_tree.py"),str(root)],stdout=(packet/"receipts/epoch-probe-tree-restored.json").open("w"),check=True)
