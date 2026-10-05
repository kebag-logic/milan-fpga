#!/usr/bin/env python3
"""Run independent lightweight checks concurrently; no full banks."""
import argparse, concurrent.futures, os, subprocess, sys, time
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("source",type=Path);p.add_argument("receipts",type=Path);a=p.parse_args();source=a.source.resolve();out=a.receipts.resolve()
jobs={
 "source-lists":[sys.executable,"scripts/check_rtl_source_lists.py"],
 "source-list-controls":[sys.executable,"scripts/check_rtl_source_lists.py","--selftest"],
 "processor-sources":[sys.executable,"scripts/pp_srcs.py","--check","--selftest"],
 "capture":[sys.executable,"scripts/check_nvm_capture.py"],
 "resource-baseline":[sys.executable,"syn/ooc/pp_resource_gate.py","check-baseline"],
 "allocation":[sys.executable,"scripts/check_nvm_record_space.py","--self-test"],
 "resmap-sweep-controls":[sys.executable,"syn/resmap/yosys_sweep.py","--selftest"],
 "resmap-model-controls":[sys.executable,"syn/resmap/resmap_models.py","--selftest"],
 "resmap-table-controls":[sys.executable,"syn/resmap/resmap_tables.py","--selftest"],
 "submodule-docs":[sys.executable,"scripts/check_submodule_docs.py"],
 "port-contracts":[sys.executable,"scripts/check_port_contracts.py"],
 "naming":[sys.executable,"scripts/measure_naming.py","--check"],
 "test-evidence":[sys.executable,"scripts/measure_test_evidence.py","--check"],
 "builder-focused":[sys.executable,"-c","import sys;sys.path.insert(0,\"sw/builder\");import test_builder as t;[getattr(t,n)() for n in (\"test_name_count_fits_the_nvm_name_block\",\"test_shipping_image_contract\",\"test_soc_shipping_image_contract\",\"test_shipping_image_contract_presence\")]"],
}
def run(item):
 name,cmd=item;start=time.monotonic()
 with (out/f"{name}.log").open("wb") as log:
  r=subprocess.run(cmd,cwd=source,stdout=log,stderr=subprocess.STDOUT)
 (out/f"{name}.rc").write_text(str(r.returncode)+"\n")
 print(f"{name}: rc={r.returncode} seconds={time.monotonic()-start:.1f}",flush=True)
 return r.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:rcs=list(pool.map(run,jobs.items()))
raise SystemExit(any(rcs))
