#!/usr/bin/env python3
"""Re-run unchanged public probe and grade its unchanged functions at the new head."""
import contextlib, hashlib, importlib.util, io, json, pathlib, subprocess, sys
probe,repo,work=sys.argv[1:]; spec=importlib.util.spec_from_file_location("prior_probe",probe); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
print("Unchanged public probe sha256="+hashlib.sha256(pathlib.Path(probe).read_bytes()).hexdigest(),flush=True)
subprocess.run([sys.executable,probe,repo,work+"-unchanged"],check=True)
m.PARENT=m.HEAD; m.HEAD="33ac35b54648ef919227c5dd8b9abc97fa6bedbd"; sys.argv=[probe,repo,work+"-current"]
buf=io.StringIO()
with contextlib.redirect_stdout(buf): assert m.main()==0
raw=buf.getvalue(); print(raw,end=""); rows=[json.loads(l) for l in raw.splitlines()]; n=0
for row in rows:
 if row.get("bodies")!="head": continue
 assert row["rc"]==0,row
 if row["case"].startswith("B16"): assert row["rtl"]=="false" and row["n"]==2,row
 else: assert row["rtl"]=="true" and "hdl/x.sv" in row["files"],row
 n+=1
assert n==9,n
print("PASS: nine current-head outcomes; historical probe is observational and always exits zero")
