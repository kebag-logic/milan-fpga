#!/usr/bin/env python3
"""Run focused baselines and independently plant the two refusal bypasses."""
import argparse, concurrent.futures, hashlib, json, os, re, shutil, subprocess, sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("--repo",type=Path,required=True);p.add_argument("--packet",type=Path,required=True);p.add_argument("--jobs",type=int,default=16);p.add_argument("--verilator",required=True)
a=p.parse_args();a.repo=a.repo.resolve();a.packet=a.packet.resolve()
assert 8 <= a.jobs <= 16
os.environ["PYTHONDONTWRITEBYTECODE"]="1";sys.dont_write_bytecode=True
os.environ["TMPDIR"]=str(a.packet/"scratch")
sys.path.insert(0,str(a.repo/"sw/firmware/ctrl/test"))
import ctrl_build, aecp_arms, fw_gtest
receipts=a.packet/"receipts";receipts.mkdir(exist_ok=True)
plants=[("X8-nosub-bypasses-running-only", "Core.S1_NoSubcommandSetOnRunningOutputIsRefused", "STREAM_IS_RUNNING for a no-sub-command SET",
    "\t\tif (info.running) {\n", "\t\tif ((wire_be32(in + 4) & 0xfaf80000u) == 0u && !aecp_foreign_lock(a)) {\n\t\t\twire_put_be(out + 4, flags & ~0x20000000u, 4);\n\t\t\treturn AECP_SUCCESS;\n\t\t}\n\t\tif (info.running) {\n"),
 ("X9-nosub-bypasses-input-refusal", "Core.S2_NoSubcommandSetOnInputIsNotSupported", "NOT_SUPPORTED for a no-sub-command SET to a STREAM_INPUT",
    "\t\tif (type == 5u) {\n\t\t\treturn AECP_NOT_SUPPORTED;\n\t\t}\n", "\t\tif (type == 5u && (wire_be32(in + 4) & 0xfaf80000u) != 0u) {\n\t\t\treturn AECP_NOT_SUPPORTED;\n\t\t}\n")]
def native(interfaces):
    root=a.packet/"scratch"/f"native-if{interfaces}"
    src=root/"ctrl";shutil.copytree(a.repo/"sw/firmware/ctrl",src,dirs_exist_ok=True,ignore=shutil.ignore_patterns("__pycache__"))
    tree=ctrl_build.Tree(src,root/"build",root/"reuse",fw_gtest.Build(jobs=max(1,(a.jobs-8)//2)))
    config=a.repo/"configs/endstation_ax7101_1x1_tdm8.yaml"
    output=[]
    def run(label, selected):
        result=aecp_arms.core_arm(tree,config,interfaces,"core",selected)
        tag=f"{label}-if{interfaces}"
        (receipts/(tag+".log")).write_text(result.log)
        (receipts/(tag+".rc")).write_text(str(result.rc)+"\n")
        return result
    baseline=run("baseline","Core.*")
    assert baseline.rc==0
    output.append({"interfaces":interfaces,"case":"baseline","rc":baseline.rc})
    path=src/"aecp/aecp_commands.c";original=path.read_text()
    for label,test,words,old,new in plants:
        assert original.count(old)==1
        path.write_text(original.replace(old,new))
        try:
            result=run(label,test)
            match=re.search(r"\[ RUN      \] "+re.escape(test)+r"\n(.*?)\[  FAILED  \] "+re.escape(test)+r" \(",result.log,re.S)
            assert result.rc==1 and match and words in match[1]
            assert "verdict: FAIL (its tallies report" in result.log
            output.append({"interfaces":interfaces,"case":label,"test":test,"diagnostic":words,"rc":result.rc,"completed_named_failure":True})
        finally:path.write_text(original)
    assert path.read_text()==original
    return output
def wire():
    outputs=[]
    for interfaces in (1,2):
        root=a.packet/"scratch"/f"wire-{interfaces}"
        reference=a.repo/"protocol-processor" if interfaces==1 else a.packet/"scratch/reference-two"
        cmd=[sys.executable,"-B",str(a.repo/"sw/firmware/ctrl/test/aecp_wire.py"),"--reference",str(reference),"--interfaces",str(interfaces),"--output",str(root),"--verilator",a.verilator]
        with (receipts/f"wire-{interfaces}.log").open("w") as log:
            r=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,timeout=1100)
        (receipts/f"wire-{interfaces}.rc").write_text(str(r.returncode)+"\n")
        assert r.returncode==0
        dest=receipts/f"wire-{interfaces}";dest.mkdir(exist_ok=True)
        for name in ["verdict.json","reference-sha256.json","aecp_entity_gen.h"]+[f"wire-if{i}.log" for i in range(interfaces)]:shutil.copy2(root/name,dest/name)
        outputs.append(json.loads((root/"verdict.json").read_text()))
    return outputs
version=subprocess.check_output([a.verilator,"--version"],text=True).strip()
assert "Verilator 5.050" in version
(receipts/"simulator-identity.json").write_text(json.dumps({"version":version,"sha256":hashlib.sha256(Path(a.verilator).read_bytes()).hexdigest()},indent=2)+"\n")
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    futures={pool.submit(native,1):"native-1",pool.submit(native,2):"native-2",pool.submit(wire):"wire"}
    results={}
    for f in concurrent.futures.as_completed(futures):
        name=futures[f]
        try:results[name]=f.result();print(name+" complete",flush=True)
        except Exception as e:results[name]={"error":repr(e)};print(name+" ERROR "+repr(e),flush=True)
        (receipts/"focused-results.json").write_text(json.dumps(results,indent=2)+"\n")
assert all(not isinstance(v,dict) or "error" not in v for v in results.values())
print("Focused baselines, four named mutation failures and wire controls PASS",flush=True)
