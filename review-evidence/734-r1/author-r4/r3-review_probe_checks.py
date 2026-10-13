"""Rerun published probes unchanged, then grade actual shipping bodies for Round 3 equality."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

shipping=Path(sys.argv[1]).resolve()
probes=Path(sys.argv[2]).resolve()
work=Path(sys.argv[3]).resolve()
work.mkdir(parents=True,exist_ok=True)
probe=probes/"probe_r632_2.py"
spec=importlib.util.spec_from_file_location("review_probe",probe)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
result=subprocess.run([sys.executable,str(probe),str(shipping),str(work/"unchanged")],capture_output=True,text=True)
(work/"unchanged.log").write_text(result.stdout+result.stderr)
misses=[line for line in result.stdout.splitlines() if line.startswith("MISS")]
assert result.returncode==1 and len(misses)==3 and all("identical-on-dev" in line and "hosted=false" in line and "replay=false" in line for line in misses), result.stdout+result.stderr
print("PASS unchanged published probe: only its three old divergence expectations differ")
print("Published probe SHA-256:",hashlib.sha256(probe.read_bytes()).hexdigest())
root=work/"equality"; root.mkdir()
repo=m.Repo(root,shipping)
cases=m.build(repo)
rows=[]
for wf,job,sid in m.SCOPES:
 body=m.step_body(shipping,wf,job,sid)
 for label,(recorded,live,head,want) in cases.items():
  expected=want[0] if isinstance(want,tuple) else want
  hosted=m.hosted(repo,body,recorded,live,head)
  replay=m.replay(repo,body,recorded,live,head)
  assert hosted==replay and hosted[0]==expected,(wf,label,hosted,replay,expected)
  rows.append(dict(workflow=wf,case=label,hosted=hosted,replay=replay))
rename=work/"rename"; rename.mkdir()
script=probes/"rename_divergence_r632_2.sh"
result=subprocess.run(["bash",str(script),str(shipping),str(rename)],capture_output=True,text=True)
(work/"rename-unchanged.log").write_text(result.stdout+result.stderr)
assert result.returncode==0,result.stderr
assert "hosted files: docs/reference/REGISTER_MAP.md -> rtl=true" in result.stdout
assert "replay files: docs/page.md -> rtl=false" in result.stdout
print("PASS unchanged rename probe reproduces the old formula discrepancy")
print("Published rename probe SHA-256:",hashlib.sha256(script.read_bytes()).hexdigest())
class Holder(m.Repo):
 def __init__(self,root): self.root=root
repo=Holder(rename)
head=m.git(rename,"rev-parse","HEAD")
recorded=m.git(rename,"rev-parse","HEAD^1")
live=m.git(rename,"rev-parse","master")
for wf,job,sid in m.SCOPES:
 body=m.step_body(shipping,wf,job,sid)
 hosted=m.hosted(repo,body,recorded,live,head)
 replay=m.replay(repo,body,recorded,live,head)
 assert hosted==replay==("true",["docs/reference/REGISTER_MAP.md"]),(wf,hosted,replay)
 rows.append(dict(workflow=wf,case="base-side rename",hosted=hosted,replay=replay))
print(json.dumps(rows,indent=2))
print(f"review probes: PASS {len(rows)} paired equality cases")
