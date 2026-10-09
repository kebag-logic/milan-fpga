#!/usr/bin/env python3
"""Run changed shape controls sequentially, plus real guard examples."""
import argparse, hashlib, os, subprocess, sys, urllib.request, zipfile
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument("--repo",type=Path,required=True);ap.add_argument("--packet",type=Path,required=True);ap.add_argument("--mode",choices=("shape","guards"),required=True);a=ap.parse_args()
root=a.repo.resolve();p=a.packet.resolve();w=p/"scratch"/("source-"+a.mode);w.mkdir(parents=True,exist_ok=True)
env=dict(os.environ,TMPDIR=str(w),PYTHONDONTWRITEBYTECODE="1",MAKEFLAGS="-j16")
def run(label,cmd,e,expected=0,marker=None):
 r=subprocess.run(cmd,cwd=root,env=e,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=540)
 (p/"receipts"/(label+".log")).write_bytes(r.stdout);(p/"receipts"/(label+".rc")).write_text(str(r.returncode)+"\n")
 assert r.returncode==expected,(label,r.returncode,r.stdout[-1200:])
 if marker:assert marker.encode() in r.stdout,(label,marker)
 print(label,"rc="+str(r.returncode),"PASS",flush=True)
if a.mode=="shape":
 for label,directory in (("shape441",Path("/usr/bin")),("shape43",p/"scratch/make43-build/make-4.3")):
  run(label,[sys.executable,"scripts/check_entity_shape.py","--self-test"],dict(env,PATH=str(directory)+os.pathsep+env["PATH"]),marker="checks: 228   failures: 0")
else:
 archive=w/"sv2v-Linux.zip"
 urllib.request.urlretrieve("https://github.com/zachjs/sv2v/releases/download/v0.0.12/sv2v-Linux.zip",archive)
 assert hashlib.sha256(archive.read_bytes()).hexdigest()=="ff8c9eea5bc029b372fb4953427625cddb7cf7e58c1240623ac9f260818d5a00"
 with zipfile.ZipFile(archive) as z:z.extractall(w)
 sv12=next(x for x in w.rglob("sv2v") if x.is_file());sv12.chmod(0o755)
 for label,binary in (("sv12",str(sv12)),("sv13",subprocess.check_output(["sh","-c","command -v sv2v"],text=True).strip())):
  print(label,subprocess.check_output([binary,"--version"],text=True).strip(),"sha256="+hashlib.sha256(Path(binary).read_bytes()).hexdigest(),flush=True)
  for width,expected in ((52,1),(64,0)):
   cmd=["bash","-c",'sv2v() { "$REVIEW_SV2V" "$@"; }; export -f sv2v; bash syn/yosys/ooc.sh rx_mac_filter']
   e=dict(env,REVIEW_SV2V=binary,OOC_TMP=str(w/(label+str(width))),OOC_CHPARAM="TDATA_WIDTH="+str(width))
   marker=("TDATA_WIDTH=%0d is not a whole number of bytes" if label=="sv12" else "$error") if expected else "rx_mac_filter"
   run("ooc-"+label+"-width"+str(width),cmd,e,expected,marker)
 print("guard examples: four expected outcomes",flush=True)
