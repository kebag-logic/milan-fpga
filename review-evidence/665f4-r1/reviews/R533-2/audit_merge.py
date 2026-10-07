#!/usr/bin/env python3
"""Record inherited-path equality and the exact eight conflict resolutions."""
import argparse, hashlib, json, subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("source",type=Path);a=p.parse_args();root=a.source.resolve();packet=Path(__file__).resolve().parent
base="db9aa8c9b135b34ff3d070a979dee70440b37cc6";dev="d51b373ad7e8e8381af2797be3ebb8ee45c62e3c";old="50d492c12789e1d80bf11f547e7fe53e02b4bdb9";merge="8b43aed6126c39483ce20e37f0644d34f6f30696"
def git(*args):return subprocess.check_output(["git",*args],cwd=root)
def changed(a,b):return set(git("diff","--name-only",a,b).decode().splitlines())
def entry(ref,path):return git("ls-tree",ref,"--",path).decode().strip()
ours=changed(base,old);theirs=changed(base,dev)
untouched=sorted(theirs-ours)
assert all(entry(merge,n)==entry(dev,n) for n in untouched)
followups={n for n in untouched if entry("HEAD",n)!=entry(dev,n)}
assert followups=={"sw/firmware/ctrl/mbx/mbx.h"}
header_delta=git("diff","--unified=0",dev,"HEAD","--","sw/firmware/ctrl/mbx/mbx.h").decode()
assert not any(l.startswith("-") and not l.startswith("---") for l in header_delta.splitlines())
conflicts=[".github/workflows/rtl-fast.yml","scripts/ci_events.py","sw/firmware/ctrl/README.md","sw/firmware/ctrl/test/ctrl_build.py","sw/firmware/ctrl/test/ctrl_mutants.py","sw/firmware/ctrl/test/test_ctrl_firmware.py","sw/firmware/gtest/fw_rv32.py","sw/firmware/gtest/fw_rv32_selftest.py"]
records=[]
for path in conflicts:records.append({"path":path,"dev":entry(dev,path),"old_f4":entry(old,path),"merge":entry(merge,path),"head":entry("HEAD",path)})
remerge=git("show","--remerge-diff","--format=",merge,"--",*conflicts)
(packet/"receipts/merge-resolution.diff").write_bytes(remerge)
result={"base":base,"dev":dev,"old_f4":old,"merge":merge,"parents":git("show","-s","--format=%P",merge).decode().strip(),"dev_only_paths_equal_at_merge":untouched,"head_additive_followup":header_delta,"conflicts":records,
"head_vs_dev_rtl":git("diff","--name-only",dev,"HEAD","--","hdl").decode().splitlines(),"size_inputs_changed_since_measurement":git("diff","--name-status","181e3e1ac","HEAD").decode().splitlines()}
(packet/"receipts/merge-audit.json").write_text(json.dumps(result,indent=2)+"\n")
print(len(untouched),"dev-only paths retained exactly;",len(conflicts),"conflict resolutions recorded")
