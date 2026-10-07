# SPDX-License-Identifier: Apache-2.0
"""Independent mutations, compiled before their ownership oracle runs."""
import argparse, concurrent.futures, shutil
from common import *
p=argparse.ArgumentParser();p.add_argument("--jobs",type=int,default=2);a=p.parse_args()
mutations=[
 ("snapshot-copies-only-identity","memcpy(ai->flush_value, ai->attr_val, attr_store_len(app->ops, ai->attr_type));","memcpy(ai->flush_value, ai->attr_val, 8);"),
 ("queue-reserves-current-value","map_reserve(app, ai->attr_type, ind_value,","map_reserve(app, ai->attr_type, ai->attr_val,"),
 ("pending-freezes-applicant","    if (a) {\n        /*\n         * Refresh the stored value:","    if (a) {\n        if (a->flush_pending) { return a; }\n        /*\n         * Refresh the stored value:"),
 ("replacement-ignores-pending","if (old != ai && old->reg != MRP_REG_STATE_MT &&","if (old != ai && !old->flush_pending && old->reg != MRP_REG_STATE_MT &&"),
]
def profile(mode):
 src=SCRATCH/("own-mut-"+mode);src.mkdir(exist_ok=True)
 for d in ("src","tests"):shutil.copytree(SOURCE/d,src/d,dirs_exist_ok=True,ignore=shutil.ignore_patterns("__pycache__"))
 f=src/"src/core/mrp_mad.c"; original=f.read_text();results=[]
 for label,old,new in mutations:
  assert old in original,label;f.write_text(original.replace(old,new));exe=src/label
  try:
   run(mode+"-own-"+label+"-build",["cc","-std=c11","-O1","-g","-DLWSRP_MILAN="+("1" if mode=="ON" else "0"),"-Isrc/include","-Isrc","-Itests/unit",PACKET/"scripts/storage_probe.c","src/core/mrp_pdu.c","src/modules/msrp.c","src/ports/timer.c","tests/unit/fault_alloc.c","-o",exe],cwd=src)
   rc,out=run(mode+"-own-"+label,[exe],cwd=src,expected=None)
   killed=rc==1 and "FAIL case=" in out;assert killed,(mode,label)
   results.append(dict(label=label,killed=killed,rc=rc,evidence=out.strip()))
  finally:f.write_text(original)
 (PACKET/"receipts"/(mode+"-own-mutations.json")).write_text(json.dumps(results,indent=2)+"\n")
with concurrent.futures.ThreadPoolExecutor(max_workers=min(a.jobs,2)) as ex:list(ex.map(profile,["OFF","ON"]))
