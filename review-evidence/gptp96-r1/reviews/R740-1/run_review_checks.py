#!/usr/bin/env python3
"""Run focused read-only gates and isolated documentation fault probes."""
import concurrent.futures, hashlib, json, os, pathlib, subprocess, sys, tarfile, io
root=pathlib.Path(sys.argv[1]).resolve()
out=pathlib.Path(__file__).resolve().parent
scratch=out/"scratch"
(scratch/"tmp").mkdir(parents=True,exist_ok=True)
env=dict(os.environ,TMPDIR=str(scratch/"tmp"),PYTHONDONTWRITEBYTECODE="1")
env["PATH"]=env.get("REVIEW_LINT_DIR","$VALIDATION_TOOLS/pinned-verilator-5.050")+":"+env["PATH"]
def run(name,cmd,cwd=root):
 p=subprocess.run(cmd,cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=240)
 (out/(name+".log")).write_text(p.stdout)
 (out/(name+".rc")).write_text(str(p.returncode)+"\n")
 return name,p.returncode
jobs=[("docs",["make","-j16","docs"]),("lint",["make","-j16","lint"]),("contract",["make","-j16","contract"]),("ooc-clock-selftest",["python3","syn/ooc/check_ooc_clock.py","--selftest"])]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
 for result in ex.map(lambda pair:run(*pair),jobs): print(*result,flush=True)
probe=scratch/"probe"
probe.mkdir(exist_ok=True)
data=subprocess.check_output(["git","archive","HEAD"],cwd=root)
with tarfile.open(fileobj=io.BytesIO(data)) as t: t.extractall(probe,filter="data")
mutations=[
("control",None,None,None),
("stale-constant","docs/INTEGRATION.md","| `SYNC_RTO_MS_C` | 375 |","| `SYNC_RTO_MS_C` | 376 |"),
("stale-rom","docs/MANAGER.md","1,022 of 1,024","1,021 of 1,024"),
("missing-status","docs/README.md","| `docs/GLOSSARY.md` | Every reader | Defined terms and their clauses | Current |\n",""),
("formatted-stale-constant","docs/INTEGRATION.md","| `SYNC_RTO_MS_C` | 375 |","| `SYNC_RTO_MS_C` | **376** |"),
("negative-stale-constant","docs/INTEGRATION.md","| `SYNC_RTO_MS_C` | 375 |","| `SYNC_RTO_MS_C` | -1 |"),
("duplicate-rom","docs/MANAGER.md","| Shipping | 1,022 of 1,024 | 2 |","| Shipping | 1,022 of 1,024 | 2 |\n| Shipping | 1,022 of 1,024 | 2 |"),
("duplicate-prose-drift","docs/INTEGRATION.md","| Link-up | 20 us | 20 us |","| Link-up | 21 us | 21 us |")]
results=[]
for name,rel,old,new in mutations:
 path=probe/rel if rel else None
 original=path.read_bytes() if path else None
 try:
  if path:
   text=original.decode(); assert old in text,name
   path.write_text(text.replace(old,new,1))
  result=run("probe-"+name,["python3","scripts/check_docs.py"],probe)
  results.append(dict(name=name,rc=result[1],file=rel,old=old,new=new)); print(*result,flush=True)
 finally:
  if path:path.write_bytes(original)
(out/"probe-results.json").write_text(json.dumps(results,indent=2)+"\n")

# Exercise the escaped row through the complete documentation target.
p=probe/"docs/INTEGRATION.md"
original=p.read_bytes()
try:
 p.write_text(original.decode().replace("| `SYNC_RTO_MS_C` | 375 |","| `SYNC_RTO_MS_C` | **376** |",1))
 print(*run("probe-full-formatted-stale",["make","-j16","docs"],probe),flush=True)
finally:
 p.write_bytes(original)
