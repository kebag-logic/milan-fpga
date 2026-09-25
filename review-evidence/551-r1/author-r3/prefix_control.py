import json, os, subprocess, sys, tempfile, time
from pathlib import Path
out=Path(__file__).resolve().parent
root=Path.cwd()
fixed="990f96526bb89356c963a260ebbdcf2a77e6623a"
old=subprocess.check_output(["git","-C","protocol-processor","rev-parse","a8f8ce810ddba1816cd129d0afcd71e6e02ade1b^1"],text=True).strip()
assert subprocess.check_output(["git","-C","protocol-processor","status","--porcelain"],text=True)==""
def logged(name, cmd, cwd=root):
 start=time.time()
 with (out/(name+".log")).open("w") as log:
  rc=subprocess.run(cmd,cwd=cwd,stdout=log,stderr=subprocess.STDOUT,timeout=14400).returncode
 record=dict(name=name,command=cmd,cwd=str(cwd),rc=rc,seconds=round(time.time()-start,2),log=name+".log")
 with (out/"gates.jsonl").open("a") as log: log.write(json.dumps(record)+"\n")
 print(json.dumps(record),flush=True)
 return rc
print("pre-fix control:",old,"restored pin:",fixed,flush=True)
try:
 subprocess.run(["git","update-index","--cacheinfo",f"160000,{old},protocol-processor"],check=True)
 subprocess.run(["git","submodule","update","--init","protocol-processor"],check=True)
 with tempfile.TemporaryDirectory(prefix="551-a312-prefix-") as td:
  cmd=["make","-C","tb/verilator/milan_dp","crflic-build","VERILATOR_JOBS=8",f"CRFLIC_MDIR={td}"]
  assert logged("prefix_build",cmd)==0
  rc=logged("prefix_fixture",[td+"/Vmilan_dp_crflic","--unwarmed-refusal"],root/"tb/verilator/milan_dp")
  assert rc==1, f"expected fixture verdict 1, got {rc}"
  log=(out/"prefix_fixture.log").read_text()
  failures=[]
  phase=""
  for line in log.splitlines():
   if line.startswith("[I] "): phase=line
   elif line.startswith(("[G] ","[H] ","[J] ")): phase=""
   if phase and "[FAIL]" in line: failures.append((phase,line))
  assert len(failures)==28, f"expected 28 unwarmed refusal failures, got {len(failures)}"
  summary="\n".join(f"{phase}: {line.strip()}" for phase,line in failures)+"\n"
  (out/"prefix-refusal-failures.txt").write_text(summary)
  print(summary,flush=True)
finally:
 subprocess.run(["git","update-index","--cacheinfo",f"160000,{fixed},protocol-processor"],check=True)
 subprocess.run(["git","submodule","update","--init","protocol-processor"],check=True)
 assert subprocess.check_output(["git","-C","protocol-processor","rev-parse","HEAD"],text=True).strip()==fixed
 assert subprocess.check_output(["git","-C","protocol-processor","status","--porcelain"],text=True)==""
 print("Restored merged gitlink, submodule HEAD and pristine bytes",flush=True)
