#!/usr/bin/env python3
"""Compare production RTL independently of the submitted guard inventory."""
import argparse, hashlib, json, re, subprocess
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument("root",type=Path);a=ap.parse_args();r=a.root.resolve()
def git(*args):return subprocess.check_output(["git","-C",str(r),*args]).decode()
base="2cbed0a987c1e68402658d69459ab7e5aa571adc"
paths=git("ls-files","hdl").splitlines(); n=0; sites=[]
def strip(s):return re.sub(r"/\*.*?\*/|//[^\n]*", "",s,flags=re.S)
for path in paths:
 if not path.endswith(".sv"):continue
 before=git("show",base+":"+path);after=(r/path).read_text();n+=1
 # Sole structural change: existing listener time-zero conditional becomes a generate guard.
 if path=="hdl/acmp/KL_pp_acmp_listener.sv":
  before=before.replace("initial begin : parameter_checks\n    if (STRM_TIMEOUT_CYC_P == 0)","if (STRM_TIMEOUT_CYC_P == 0) begin : g_strm_tmo_check")
 def norm(s):
  s=re.sub(r"\$fatal\(1,\s*", "$diagnostic(",strip(s))
  s=re.sub(r"\$error\(","$diagnostic(",s)
  return re.sub(r"\s+"," ",s).strip()
 assert norm(before)==norm(after),path
 clean=strip(after)
 assert not re.search(r"\$(?:error|warning|info|stop|finish)\b|\bassert\s*\(",clean),path
 for m in re.finditer(r"\$fatal\(",after):
  # Ignore diagnostics cited in comments using the corresponding source line.
  line=after[:m.start()].count("\n")+1
  if after.splitlines()[line-1].lstrip().startswith("//"):continue
  sites.append({"path":path,"line":line})
assert len(sites)==31,len(sites)
print(json.dumps({"rtl_files_compared":n,"fatal_sites":sites,"guard_count":len(sites),"result":"PASS: predicates, messages, and remaining production RTL match base after only accepted severity/scope normalization"},indent=2))
