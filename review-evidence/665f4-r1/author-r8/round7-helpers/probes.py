import os,sys,concurrent.futures
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/"sw/firmware/ctrl/test"))
from ctrl_build import CTRL,Tree
import srp_arms,fw_gtest
root=Path(os.environ["SCRATCH"])
packet=Path(os.environ["REVIEW_PACKET"])/"scripts"
build=fw_gtest.Build(jobs=2)
def run(item):
 name,n=item
 test=str(packet/name) if name.startswith("r5") else name
 r=srp_arms.arm_srp(Tree(CTRL,root/"probe-build",root/"reuse",build),Path.cwd()/"third_party/lwSRP",n,test=test)
 print(r.arm,r.rc,r.log,flush=True)
 return r.rc
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 results=list(pool.map(run,[(name,n) for name in ("r532_hol_probe.cpp","r532_flood_probe.cpp","r533_5_independent.cpp","r532_retry_probes.cpp","srp_rx_retry.cpp","srp_latency.cpp") for n in (1,2)]))
raise SystemExit(any(results))
