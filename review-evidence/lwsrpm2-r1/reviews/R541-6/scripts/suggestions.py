# SPDX-License-Identifier: Apache-2.0
"""Recheck inherited optional coverage observations at this head."""
import argparse, concurrent.futures
from common import *
p=argparse.ArgumentParser();p.add_argument("--jobs",type=int,default=2);a=p.parse_args()
def profile(mode):
 src=SCRATCH/("mutations-"+mode)/"source";b=src.parent/"build";f=src/"src/core/mrp_mad.c";original=f.read_text()
 mutations=[("suggestion-pending-replacement","if (old != ai && old->reg != MRP_REG_STATE_MT &&","if (old != ai && !old->flush_pending && old->reg != MRP_REG_STATE_MT &&"),("suggestion-flush-leaveall","    if (flush)\n        la_event", "    if (false && flush)\n        la_event")]
 records=[]
 for label,old,new in mutations:
  assert old in original;f.write_text(original.replace(old,new))
  try:
   build(mode+"-"+label+"-build",b);rc,out=run(mode+"-"+label,[b/"unit_tests"],expected=None)
   records.append(dict(label=label,rc=rc,survives=rc==0))
  finally:f.write_text(original)
 build(mode+"-suggestions-restored-build",b);run(mode+"-suggestions-restored-units",[b/"unit_tests"])
 (PACKET/"receipts"/(mode+"-suggestion-results.json")).write_text(json.dumps(records,indent=2)+"\n")
with concurrent.futures.ThreadPoolExecutor(max_workers=min(a.jobs,2)) as ex:list(ex.map(profile,["OFF","ON"]))
