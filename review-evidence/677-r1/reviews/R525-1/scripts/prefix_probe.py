#!/usr/bin/env python3
"""Replay the standing exact-prefix case and its three boundary mutants.
Usage: prefix_probe.py REPO WORK [--jobs N]
"""
import argparse,pathlib,sys
ap=argparse.ArgumentParser();ap.add_argument("repo",type=pathlib.Path);ap.add_argument("work",type=pathlib.Path);ap.add_argument("--jobs",type=int,default=2);a=ap.parse_args()
repo=a.repo.resolve(); work=a.work.resolve(); work.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(repo/"sw/firmware/ctrl_nvm/test"))
import test_ctrl_nvm as gate
import nvm_bench,nvm_mutants,fw_gtest
shape=gate.prepare(repo/"configs/endstation_ax7101_1x1_tdm8.yaml",work/"shape")
binary=next(b for b in nvm_bench.UNITS if b.name=="prefix")
build=fw_gtest.Build(jobs=a.jobs)
mutants=[m for m in nvm_mutants.MUTANTS if m.name.startswith("erased_payload_")]
for m in [None,*mutants]:
    name=m.name if m else "control"
    tree=work/name/"tree" if m else nvm_bench.TREE
    if m:nvm_mutants.plant(m,tree)
    exe=nvm_bench.build_suite(shape.inputs,work/name/"build",build,binary,tree)
    ok,log=nvm_bench.run_suite(exe,shape.fixture)
    print("CASE",name,flush=True); print(log,flush=True)
    if m:
        assert not ok,name
        assert "[FAIL] NvmCodec.codec_erased_loaded_prefix" in log,name
        if m.name!="erased_payload_guard_early":assert "AddressSanitizer: heap-buffer-overflow" in log,name
    else:assert ok
print("Exact-size control passes; old end bound and both one-byte boundary defects fail the named case.")
