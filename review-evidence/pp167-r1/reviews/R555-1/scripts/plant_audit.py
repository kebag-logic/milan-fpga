#!/usr/bin/env python3
"""Read-only planting audit at both source revisions; no simulation bank."""
import collections, concurrent.futures, importlib.util, json, pathlib, subprocess, sys
sys.dont_write_bytecode=True
packet=pathlib.Path(__file__).resolve().parents[1]; root=pathlib.Path(sys.argv[1]).resolve()
base=packet/"scratch/plant-base"
subprocess.run(["git","clone","--quiet","--shared","--no-checkout",str(root),str(base)],check=True)
subprocess.run(["git","-C",str(base),"checkout","--quiet","--detach","ed340b9b85258194247334b85e62cf9c23d4d051"],check=True)
def module(tree,rel):
    name=tree.name+rel.replace("/","_").replace(".","_")
    spec=importlib.util.spec_from_file_location(name,tree/rel); mod=importlib.util.module_from_spec(spec)
    sys.modules[name]=mod; spec.loader.exec_module(mod); return mod
for label,tree in [("base",base),("head",root)]:
    records=[]
    def patch(p):
        r=subprocess.run(["git","apply","--check",str(p)],cwd=tree,capture_output=True,text=True)
        return {"kind":"patch","name":str(p.relative_to(tree)),"passed":r.returncode==0,"detail":r.stderr.strip()}
    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as pool:
        records+=list(pool.map(patch, sorted(tree.glob("tb/**/*.patch"))))
    for rel in ["tb/pp_top/notify_mutants.py","tb/pp_top/d3_mutants.py","tb/pp_top/acmp_mutants.py"]:
        mod=module(tree,rel)
        for m in mod.MUTANTS:
            contents={}; details=[]
            for path,old,new in m.edits:
                contents.setdefault(path,(tree/path).read_text())
                count=contents[path].count(old)
                if count!=1: details.append(f"{path}: expected 1 anchor, got {count}")
                contents[path]=contents[path].replace(old,new,1)
            records.append({"kind":"exact","name":rel+":"+m.name,"passed":not details,"detail":"; ".join(details)})
    mod=module(tree,"tb/acmp_talker/retry_mutants.py")
    for name in mod.MUTATIONS:
        try: mod.mutated_source((tree/mod.RTL).read_text(),name); problem=""
        except Exception as e: problem=str(e)
        records.append({"kind":"other","name":"retry:"+name,"passed":not problem,"detail":problem})
    mod=module(tree,"tb/pp_top/gsi_mutants.py")
    for name,path,old,new,count,_ in mod.mutations():
        got=(tree/path).read_text().count(old)
        records.append({"kind":"other","name":"gsi:"+name,"passed":got==count,"detail":f"expected {count}, got {got}"})
    mod=module(tree,"tb/srp_admission/mutants.py")
    for name,edits,_ in mod.MUTANTS:
        src=(tree/mod.ADMISSION).read_text(); ok=True
        for old,new,count in edits:
            ok &= src.count(old)==count;src=src.replace(old,new)
        records.append({"kind":"other","name":"admission:"+name,"passed":ok})
    anchor="  assign name_wr_o = d3_nchg_w;"
    records.append({"kind":"other","name":"name-write","passed":(tree/"hdl/aecp/KL_aecp_engine.sv").read_text().count(anchor)==1})
    cpp=(tree/"tb/acmp_talker/sim_main.cpp").read_text()
    for anchor in ["  ++checks;", "if (!(cond)) { ++fails;"]:
        records.append({"kind":"observation","name":anchor,"passed":cpp.count(anchor)==1})
    (packet/"receipts"/f"plant-{label}.json").write_text(json.dumps(records,indent=2)+"\n")
    print(label,len(records),dict(collections.Counter(r["kind"] for r in records)),"failed",[r for r in records if not r["passed"]])
    assert all(r["passed"] for r in records)
