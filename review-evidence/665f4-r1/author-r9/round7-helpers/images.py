import os,json,hashlib,subprocess,sys
from pathlib import Path
r=Path(os.environ["SCRATCH"])
runtime=Path(os.environ["RUNTIME"])
for item in json.loads((runtime/"provenance.json").read_text())["files"]:
 assert hashlib.sha256(Path(os.path.expandvars(item["path"])).read_bytes()).hexdigest()==item["sha256"]
reports=[]
for version in ("lane-base","round5","head"):
 for shape in ("endstation_ax7101_1x1_tdm8","endstation_ax7101_8x8"):
  for n in (1,2):
   out=r/f"image-{version}-{shape}-if{n}"
   command=[sys.executable,str(Path(__file__).resolve().parent/"historical_image.py") if version!="head" else "sw/firmware/ctrl/test/ctrl_image.py",
    "--config",f"configs/{shape}.yaml","--interfaces",str(n),"--output",str(out),
    "--libc",str(runtime/"libc.a"),"--compiler-runtime",str(runtime/"libcompiler_rt.a")]
   if version=="lane-base": command += ["--without-srp","--ctrl-source",str(r/"lane-base/sw/firmware/ctrl")]
   if version=="round5": command += ["--ctrl-source",str(r/"round5/sw/firmware/ctrl")]
   subprocess.run(command,check=True,timeout=120)
   report=json.loads((out/"size.json").read_text()); report["version"]=version
   reports.append(report)
(r/"image-results.json").write_text(json.dumps(reports,indent=2)+"\n")
