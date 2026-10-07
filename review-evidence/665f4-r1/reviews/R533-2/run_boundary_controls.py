#!/usr/bin/env python3
"""Replay the four previously escaped admission/licence regressions."""
import argparse, json, sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("source",type=Path);p.add_argument("--jobs",type=int,default=4);a=p.parse_args()
root=a.source.resolve();packet=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
sys.path.insert(0,str(root/"sw/firmware/ctrl/test"))
import srp_mutants
names={"tag-overhead-omitted","preamble-ifg-omitted","ninety-percent-ceiling","readyfailed-callback-stop"}
srp_mutants.DEFECTS=tuple(d for d in srp_mutants.DEFECTS if d.name in names)
assert len(srp_mutants.DEFECTS)==4
out=packet/"scratch/boundary-controls"
failed=srp_mutants.campaign(out,root/"third_party/lwSRP",a.jobs)
for n in names:(packet/"receipts"/(n+".log")).write_bytes((out/(n+".log")).read_bytes())
(packet/"receipts/boundary-controls.rc").write_text(str(int(failed))+"\n")
sys.exit(int(failed))
