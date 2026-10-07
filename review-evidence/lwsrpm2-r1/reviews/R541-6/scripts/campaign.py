# SPDX-License-Identifier: Apache-2.0
"""Sample published reversals in disposable copies; retain named failure receipts."""
import argparse, concurrent.futures, importlib.util, shutil
from common import *
p=argparse.ArgumentParser();p.add_argument("--jobs",type=int,default=2);a=p.parse_args()
spec=importlib.util.spec_from_file_location("published",SOURCE/"tests/check_reversals.py");m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
selected={"flush-snapshot-bypass","flush-snapshot-replaced","flush-snapshot-indication","flush-snapshot-policy","flush-timer-completion","flush-completion","pending-flush","flush-before-refresh","flush-retry","flush-deadline","flush-observer","replacement-leave-timer","receive-instance-stop","propagation-retention","registrar-recovery-indication","changed-in-only","stream-list-boundary","callback-order","application-decode-error","milan-delayed-in-leave","milan-restarted-lv-deadline"}
# Discover exact published labels for deadline, observer and LV replacement coverage.
selected.update(c[0] for c in m.CASES if any(k in c[0] for k in ("flush-observer","flush-retry-delay","replacement-lv")))
cases=[c for c in m.CASES if c[0] in selected]
(PACKET/"receipts/reversal-selection.json").write_text(json.dumps({"total_available":len(m.CASES),"selected":[c[0] for c in cases],"unmatched_requested":sorted(selected-{c[0] for c in cases})},indent=2)+"\n")
def profile(mode):
 src=SCRATCH/("mutations-"+mode)/"source";src.mkdir(parents=True,exist_ok=True)
 for name in ("src","tests"): shutil.copytree(SOURCE/name,src/name,dirs_exist_ok=True,ignore=shutil.ignore_patterns("__pycache__"))
 shutil.copy2(SOURCE/"CMakeLists.txt",src)
 b=src.parent/"build"
 run(mode+"-mut-configure",["cmake","-S",src,"-B",b,"-DCMAKE_BUILD_TYPE=Debug",f"-DCMAKE_PREFIX_PATH={PREFIX}","-DLWSRP_MILAN="+mode])
 build(mode+"-mut-baseline-build",b);run(mode+"-mut-baseline-units",[b/"unit_tests"])
 records=[]
 for label,name,old,new,kind in cases:
  assert kind=="unit";f=src/name;original=f.read_text();assert old in original,label
  f.write_text(original.replace(old,new))
  try:
   build(mode+"-mut-"+label+"-build",b)
   rc,out=run(mode+"-mut-"+label,[b/"unit_tests"],expected=None)
   required=m.REQUIRED_FAILURES.get(label,[])
   killed=rc!=0 and "Failure:" in out and all(n in out for n in required)
   records.append(dict(label=label,killed=killed,required=required,rc=rc))
   if not killed: raise RuntimeError("Surviving reversal "+mode+" "+label)
  finally: f.write_text(original)
 build(mode+"-mut-restored-build",b);run(mode+"-mut-restored-units",[b/"unit_tests"])
 (PACKET/"receipts"/(mode+"-reversal-results.json")).write_text(json.dumps(records,indent=2)+"\n")
 return mode,len(records)
with concurrent.futures.ThreadPoolExecutor(max_workers=min(a.jobs,2)) as ex:
 for r in ex.map(profile,["OFF","ON"]): print(r,flush=True)
