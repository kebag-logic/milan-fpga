#!/usr/bin/env python3
"""Run two bounded focused suites on an exact-head disposable export."""
import concurrent.futures, hashlib, io, json, os, pathlib, subprocess, sys, tarfile
P=pathlib.Path(__file__).resolve().parent
clone=pathlib.Path(sys.argv[1]).resolve()
head="4865184c9ba88dd85aba3fc8036a6b74bcdb7073"
assert subprocess.check_output(["git","-C",str(clone),"rev-parse","HEAD"],text=True).strip()==head
scratch=P/"scratch"; scratch.mkdir(exist_ok=True)
tree=scratch/"focused-source"; tree.mkdir(exist_ok=True)
archive=subprocess.check_output(["git","-C",str(clone),"archive",head])
with tarfile.open(fileobj=io.BytesIO(archive)) as t: t.extractall(tree,filter="data")
sim=pathlib.Path(os.environ.get("REVIEW_SIM","$VALIDATION_TOOLS/pinned-verilator-5.050/verilator"))
identity=subprocess.check_output([str(sim),"--version"],text=True)
assert "5.050" in identity
(P/"simulator-identity.txt").write_text(identity+"launcher sha256 "+hashlib.sha256(sim.read_bytes()).hexdigest()+"\n")
wrapper=scratch/"bounded-simulator.py"
wrapper.write_text("#!/usr/bin/env python3\nimport os, sys\na=sys.argv[1:]\nfor i in range(len(a)-1):\n if a[i]=='-j': a[i+1]='8'\nos.execv("+repr(str(sim))+", ["+repr(str(sim))+"]+a)\n")
wrapper.chmod(0o755)
env=os.environ.copy();env["TMPDIR"]=str(scratch)
def run(name):
    cmd=["make","-j16",f"VERILATOR={wrapper}"]
    log=P/(name+"-spotcheck.log")
    with log.open("w") as f:
        rc=subprocess.run(cmd,cwd=tree/"tb"/name,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=540).returncode
    (P/(name+"-spotcheck.rc")).write_text(str(rc)+"\n")
    # Portable public receipt paths; only path prefixes are replaced.
    text=log.read_text().replace(str(tree),"$SOURCE").replace(str(scratch),"$SCRATCH")
    log.write_text(text)
    return {"suite":name,"rc":rc,"head":head,"compile_jobs":8}
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    results=list(pool.map(run,["aecp_notify","ucpu"]))
(P/"focused-results.json").write_text(json.dumps(results,indent=2)+"\n")
print(json.dumps(results))
assert all(r["rc"]==0 for r in results)
