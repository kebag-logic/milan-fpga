# SPDX-License-Identifier: Apache-2.0
import argparse,concurrent.futures,shutil
from common import *
p=argparse.ArgumentParser();p.add_argument("--jobs",type=int,default=2);a=p.parse_args()
def profile(mode):
 for san in [False,True]:
  label=mode+"-storage"+("-san" if san else "");exe=SCRATCH/label
  flags=["-fsanitize=address,undefined","-fno-omit-frame-pointer","-fno-pie","-no-pie"] if san else []
  run(label+"-build",["cc","-std=c11","-O1","-g",*flags,"-DLWSRP_MILAN="+("1" if mode=="ON" else "0"),"-Isrc/include","-Isrc","-Itests/unit",PACKET/"scripts/storage_probe.c","src/core/mrp_pdu.c","src/modules/msrp.c","src/ports/timer.c","tests/unit/fault_alloc.c","-o",exe])
  run(label,[exe])
with concurrent.futures.ThreadPoolExecutor(max_workers=min(a.jobs,2)) as ex:
 list(ex.map(profile,["OFF","ON"]))
